#!/usr/bin/env node
/**
 * Ruff MCP Server
 * 提供 Python 代码检查和格式化能力，供对抗性审查 skill 调用
 * 通过 subprocess 调用 ruff CLI
 */

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import { execFile } from "child_process";
import { promisify } from "util";

const execFileAsync = promisify(execFile);

// 智能查找 ruff 命令
async function findRuffCommand() {
  // 先尝试直接调用 ruff
  try {
    await execFileAsync("ruff", ["--version"]);
    return { cmd: "ruff", args: [] };
  } catch {
    // 失败则尝试 python -m ruff
    try {
      await execFileAsync("python", ["-m", "ruff", "--version"]);
      return { cmd: "python", args: ["-m", "ruff"] };
    } catch {
      // 再尝试 python3
      try {
        await execFileAsync("python3", ["-m", "ruff", "--version"]);
        return { cmd: "python3", args: ["-m", "ruff"] };
      } catch {
        throw new Error(
          "未找到 ruff，请先安装：pip install ruff"
        );
      }
    }
  }
}

let ruffCmd = null;
async function getRuffCmd() {
  if (!ruffCmd) {
    ruffCmd = await findRuffCommand();
  }
  return ruffCmd;
}

// 执行 ruff 命令
async function runRuff(subArgs) {
  const { cmd, args: prefixArgs } = await getRuffCmd();
  const fullArgs = [...prefixArgs, ...subArgs];
  try {
    return await execFileAsync(cmd, fullArgs, {
      maxBuffer: 10 * 1024 * 1024,
    });
  } catch (error) {
    // ruff 在发现问题时返回非零退出码，这是正常的
    // 只要有 stdout 就认为成功
    if (error.stdout) {
      return { stdout: error.stdout, stderr: error.stderr };
    }
    throw error;
  }
}

// 创建 MCP 服务器
const server = new Server(
  {
    name: "ruff-mcp",
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
        name: "ruff_check",
        description: "对 Python 文件或目录执行 ruff lint 检查，返回错误和警告列表",
        inputSchema: {
          type: "object",
          properties: {
            path: {
              type: "string",
              description: "要检查的文件或目录的绝对路径",
            },
            select: {
              type: "array",
              items: { type: "string" },
              description: "指定要启用的规则集（如 E, F, W, I, N, etc.），不指定则使用默认配置",
            },
            ignore: {
              type: "array",
              items: { type: "string" },
              description: "指定要忽略的规则",
            },
          },
          required: ["path"],
        },
      },
      {
        name: "ruff_format_check",
        description: "检查 Python 文件的格式是否符合 ruff 规范（不修改文件）",
        inputSchema: {
          type: "object",
          properties: {
            path: {
              type: "string",
              description: "要检查的文件或目录的绝对路径",
            },
          },
          required: ["path"],
        },
      },
      {
        name: "ruff_fix",
        description: "自动修复 Python 文件中可修复的 lint 问题",
        inputSchema: {
          type: "object",
          properties: {
            path: {
              type: "string",
              description: "要修复的文件或目录的绝对路径",
            },
            select: {
              type: "array",
              items: { type: "string" },
              description: "指定要修复的规则集",
            },
          },
          required: ["path"],
        },
      },
      {
        name: "ruff_format",
        description: "格式化 Python 文件（自动修改文件）",
        inputSchema: {
          type: "object",
          properties: {
            path: {
              type: "string",
              description: "要格式化的文件或目录的绝对路径",
            },
          },
          required: ["path"],
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
      case "ruff_check":
        return await ruffCheck(args.path, args.select, args.ignore);
      case "ruff_format_check":
        return await ruffFormatCheck(args.path);
      case "ruff_fix":
        return await ruffFix(args.path, args.select);
      case "ruff_format":
        return await ruffFormat(args.path);
      default:
        throw new Error(`未知工具: ${name}`);
    }
  } catch (error) {
    return {
      content: [
        {
          type: "text",
          text: `Ruff 执行出错: ${error.message}`,
        },
      ],
      isError: true,
    };
  }
});

// 执行 ruff check
async function ruffCheck(targetPath, select, ignore) {
  const args = ["check", targetPath, "--output-format", "json"];

  if (select && select.length > 0) {
    args.push("--select", ...select);
  }
  if (ignore && ignore.length > 0) {
    args.push("--ignore", ...ignore);
  }

  const { stdout } = await runRuff(args);
  const diagnostics = JSON.parse(stdout || "[]");
  return formatCheckResult(targetPath, diagnostics);
}

// 格式化 ruff check 结果
function formatCheckResult(targetPath, diagnostics) {
  const issues = diagnostics.map((d) => ({
    file: d.filename,
    line: d.location.row,
    column: d.location.column,
    end_line: d.end_location?.row,
    end_column: d.end_location?.column,
    code: d.code,
    message: d.message,
    severity: mapSeverity(d.code),
    fixable: d.fix ? true : false,
  }));

  const errorCount = issues.filter((i) => i.severity === "error").length;
  const warningCount = issues.filter((i) => i.severity === "warning").length;
  const fixableCount = issues.filter((i) => i.fixable).length;

  // 按文件分组
  const byFile = {};
  for (const issue of issues) {
    if (!byFile[issue.file]) byFile[issue.file] = [];
    byFile[issue.file].push(issue);
  }

  return {
    content: [
      {
        type: "text",
        text: JSON.stringify(
          {
            path: targetPath,
            files_with_issues: Object.keys(byFile).length,
            total_issues: issues.length,
            errors: errorCount,
            warnings: warningCount,
            fixable: fixableCount,
            issues_by_file: byFile,
          },
          null,
          2
        ),
      },
    ],
  };
}

// 根据规则代码映射严重程度
function mapSeverity(code) {
  // F = 语法错误/致命错误
  // E = 错误
  // W = 警告
  // 其他规则类别默认 warning
  if (code?.startsWith("F") || code?.startsWith("E9")) return "error";
  return "warning";
}

// 执行 ruff format --check
async function ruffFormatCheck(targetPath) {
  try {
    const { stdout } = await runRuff(["format", "--check", targetPath]);
    return {
      content: [
        {
          type: "text",
          text: JSON.stringify(
            {
              path: targetPath,
              formatted: true,
              message: "所有文件格式正确",
            },
            null,
            2
          ),
        },
      ],
    };
  } catch (error) {
    // 格式不正确时返回非零退出码
    return {
      content: [
        {
          type: "text",
          text: JSON.stringify(
            {
              path: targetPath,
              formatted: false,
              message: "存在格式问题，可运行 ruff_format 自动修复",
              details: error.stdout || error.stderr || error.message,
            },
            null,
            2
          ),
        },
      ],
    };
  }
}

// 执行 ruff check --fix
async function ruffFix(targetPath, select) {
  const args = ["check", "--fix", targetPath, "--output-format", "json"];
  if (select && select.length > 0) {
    args.push("--select", ...select);
  }

  const { stdout } = await runRuff(args);
  try {
    const diagnostics = JSON.parse(stdout || "[]");
    return formatFixResult(targetPath, diagnostics, true);
  } catch {
    return formatFixResult(targetPath, [], false);
  }
}

function formatFixResult(targetPath, diagnostics, allFixed) {
  const remaining = diagnostics.filter((d) => !d.fix);
  return {
    content: [
      {
        type: "text",
        text: JSON.stringify(
          {
            path: targetPath,
            fixed: diagnostics.length - remaining.length,
            remaining_issues: remaining.length,
            message: allFixed
              ? "已修复所有可自动修复的问题"
              : "已修复可自动修复的问题，仍有剩余问题需手动处理",
          },
          null,
          2
        ),
      },
    ],
  };
}

// 执行 ruff format
async function ruffFormat(targetPath) {
  const { stdout } = await runRuff(["format", targetPath]);
  return {
    content: [
      {
        type: "text",
        text: JSON.stringify(
          {
            path: targetPath,
            formatted: true,
            message: "格式化完成",
            details: stdout.trim(),
          },
          null,
          2
        ),
      },
    ],
  };
}

// 启动服务器
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Ruff MCP Server 已启动 (stdio)");
}

main().catch((error) => {
  console.error("Ruff MCP Server 启动失败:", error);
  process.exit(1);
});
