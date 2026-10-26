#!/usr/bin/env node
/**
 * ESLint MCP Server
 * 提供 ESLint 代码检查能力，供对抗性审查 skill 调用
 */

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import { ESLint } from "eslint";
import { fileURLToPath } from "url";
import path from "path";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// 创建 MCP 服务器
const server = new Server(
  {
    name: "eslint-mcp",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// 工具定义
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "eslint_lint_file",
        description: "对单个 JavaScript/TypeScript 文件执行 ESLint 检查，返回错误和警告列表",
        inputSchema: {
          type: "object",
          properties: {
            file_path: {
              type: "string",
              description: "要检查的文件的绝对路径",
            },
            cwd: {
              type: "string",
              description: "工作目录（用于查找 ESLint 配置文件），默认为文件所在目录",
            },
          },
          required: ["file_path"],
        },
      },
      {
        name: "eslint_lint_directory",
        description: "对目录执行 ESLint 检查，返回所有文件的错误和警告汇总",
        inputSchema: {
          type: "object",
          properties: {
            directory: {
              type: "string",
              description: "要检查的目录的绝对路径",
            },
            extensions: {
              type: "array",
              items: { type: "string" },
              description: "要检查的文件扩展名，默认为 [.js, .jsx, .ts, .tsx, .mjs, .cjs]",
            },
          },
          required: ["directory"],
        },
      },
      {
        name: "eslint_fix_file",
        description: "自动修复单个文件中可修复的 ESLint 问题，返回修复结果",
        inputSchema: {
          type: "object",
          properties: {
            file_path: {
              type: "string",
              description: "要修复的文件的绝对路径",
            },
          },
          required: ["file_path"],
        },
      },
      {
        name: "eslint_get_config",
        description: "获取指定文件的 ESLint 配置信息",
        inputSchema: {
          type: "object",
          properties: {
            file_path: {
              type: "string",
              description: "要查询配置的文件路径",
            },
          },
          required: ["file_path"],
        },
      },
    ],
  };
});

// 工具调用处理
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    switch (name) {
      case "eslint_lint_file":
        return await lintFile(args.file_path, args.cwd);
      case "eslint_lint_directory":
        return await lintDirectory(args.directory, args.extensions);
      case "eslint_fix_file":
        return await fixFile(args.file_path);
      case "eslint_get_config":
        return await getConfig(args.file_path);
      default:
        throw new Error(`未知工具: ${name}`);
    }
  } catch (error) {
    return {
      content: [
        {
          type: "text",
          text: `ESLint 执行出错: ${error.message}`,
        },
      ],
      isError: true,
    };
  }
});

// 检查单个文件
async function lintFile(filePath, cwd) {
  const workingDir = cwd || path.dirname(filePath);
  const eslint = new ESLint({ cwd: workingDir });

  const results = await eslint.lintFiles([filePath]);
  const formatter = await eslint.loadFormatter("stylish");
  const formatted = await formatter.format(results);

  const summary = summarizeResults(results);

  return {
    content: [
      {
        type: "text",
        text: JSON.stringify(
          {
            file: filePath,
            summary,
            issues: results[0]?.messages.map((msg) => ({
              line: msg.line,
              column: msg.column,
              severity: msg.severity === 2 ? "error" : "warning",
              rule: msg.ruleId,
              message: msg.message,
              suggestion: msg.suggestions?.[0]?.desc || null,
            })) || [],
            formatted_output: formatted.trim(),
          },
          null,
          2
        ),
      },
    ],
  };
}

// 检查目录
async function lintDirectory(directory, extensions) {
  const ext = extensions || [".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs"];
  const eslint = new ESLint({ cwd: directory, extensions: ext });

  const results = await eslint.lintFiles([directory]);
  const formatter = await eslint.loadFormatter("stylish");
  const formatted = await formatter.format(results);

  const summary = summarizeResults(results);
  const fileCount = results.filter((r) => r.messages.length > 0).length;

  return {
    content: [
      {
        type: "text",
        text: JSON.stringify(
          {
            directory,
            files_scanned: results.length,
            files_with_issues: fileCount,
            summary,
            formatted_output: formatted.trim(),
          },
          null,
          2
        ),
      },
    ],
  };
}

// 自动修复文件
async function fixFile(filePath) {
  const cwd = path.dirname(filePath);
  const eslint = new ESLint({ cwd, fix: true });

  const results = await eslint.lintFiles([filePath]);
  await ESLint.outputFixes(results);

  const fixedCount = results[0]?.output ? 1 : 0;
  const remainingIssues = results[0]?.messages.filter(
    (m) => !m.fix
  ).length || 0;

  return {
    content: [
      {
        type: "text",
        text: JSON.stringify(
          {
            file: filePath,
            fixed: fixedCount > 0,
            remaining_errors: remainingIssues,
            message: fixedCount > 0
              ? "已自动修复可修复的问题"
              : "没有可自动修复的问题",
          },
          null,
          2
        ),
      },
    ],
  };
}

// 获取配置
async function getConfig(filePath) {
  const cwd = path.dirname(filePath);
  const eslint = new ESLint({ cwd });

  const config = await eslint.calculateConfigForFile(filePath);

  return {
    content: [
      {
        type: "text",
        text: JSON.stringify(
          {
            file: filePath,
            rules_count: Object.keys(config.rules || {}).length,
            parser: config.parser || "默认",
            plugins: config.plugins || [],
            env: config.env || {},
          },
          null,
          2
        ),
      },
    ],
  };
}

// 汇总结果
function summarizeResults(results) {
  let errorCount = 0;
  let warningCount = 0;
  let fixableErrorCount = 0;
  let fixableWarningCount = 0;

  for (const result of results) {
    errorCount += result.errorCount || 0;
    warningCount += result.warningCount || 0;
    fixableErrorCount += result.fixableErrorCount || 0;
    fixableWarningCount += result.fixableWarningCount || 0;
  }

  return {
    errors: errorCount,
    warnings: warningCount,
    fixable_errors: fixableErrorCount,
    fixable_warnings: fixableWarningCount,
    total: errorCount + warningCount,
  };
}

// 启动服务器
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("ESLint MCP Server 已启动 (stdio)");
}

main().catch((error) => {
  console.error("ESLint MCP Server 启动失败:", error);
  process.exit(1);
});
