#!/usr/bin/env node

/*
 * Extract a conservative PageSchema draft from Framelink Figma MCP,
 * Figma MCP/API JSON, or low-confidence YAML-like text.
 * This script intentionally avoids generating business field names,
 * API contracts, permission codes, lovCode, lookupCode, or component props.
 */

const fs = require('fs');

const args = process.argv.slice(2);

if (args.includes('--help') || args.includes('-h')) {
  printUsage();
  process.exit(0);
}

function printUsage() {
  process.stderr.write(`Usage: node extract-page-schema.js [--input figma.json] [--url figma-url] [--pretty]\n\n`);
  process.stderr.write(`Input may be Framelink get_figma_data JSON, a raw Figma node, a Figma MCP/API response, or YAML-like text from stdin.\n`);
}

function readInput() {
  const inputIndex = args.indexOf('--input');
  if (inputIndex !== -1) {
    const filePath = args[inputIndex + 1];
    if (!filePath) {
      throw new Error('--input requires a file path');
    }
    return fs.readFileSync(filePath, 'utf8');
  }

  if (process.stdin.isTTY) {
    printUsage();
    process.exit(1);
  }

  return fs.readFileSync(0, 'utf8');
}

function parseInput(text) {
  try {
    const json = JSON.parse(text);
    const embedded = extractEmbeddedFramelinkText(json);
    if (embedded) {
      const parsed = parseYamlLikeText(embedded, new Error('Framelink JSON wrapper contains YAML-like tool text'));
      parsed.metadata = {
        ...(parsed.metadata || {}),
        ...(json.metadata || {}),
      };
      parsed._parseWarning = 'Framelink JSON wrapper parsed from embedded YAML-like tool text.';
      parsed._framelinkWrapper = true;
      return { input: parsed, rawInputFormat: 'framelinkJsonWrapper' };
    }
    return { input: json, rawInputFormat: 'json' };
  } catch (error) {
    return { input: parseYamlLikeText(text, error), rawInputFormat: 'yamlLike' };
  }
}

function extractEmbeddedFramelinkText(json) {
  if (!json || typeof json !== 'object') return '';
  const data = Array.isArray(json.data) ? json.data : [];
  const textItem = data.find((item) => item && item.type === 'text' && typeof item.text === 'string');
  if (!textItem) return '';
  return /(^|\n)nodes:\n/.test(textItem.text) || /(^|\n)metadata:\n/.test(textItem.text) ? textItem.text : '';
}

function parseScalar(value) {
  const trimmed = String(value || '').trim();
  if (!trimmed) return '';
  if ((trimmed.startsWith('"') && trimmed.endsWith('"')) || (trimmed.startsWith("'") && trimmed.endsWith("'"))) {
    return trimmed.slice(1, -1);
  }
  if (trimmed === 'true') return true;
  if (trimmed === 'false') return false;
  return trimmed;
}

function parseYamlLikeText(text, jsonError) {
  const metadata = {};
  const nodes = [];
  const stack = [{ indent: -1, node: { children: nodes } }];
  let currentSection = '';
  let rootName = 'Framelink YAML-like input';
  const lines = String(text || '').split(/\r?\n/);

  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith('#')) continue;

    const indent = line.match(/^\s*/)[0].length;
    if (/^metadata:\s*$/.test(trimmed)) {
      currentSection = 'metadata';
      continue;
    }
    if (/^nodes:\s*$/.test(trimmed)) {
      currentSection = 'nodes';
      continue;
    }
    if (/^[A-Za-z0-9_-]+:\s*$/.test(trimmed) && !trimmed.startsWith('-')) {
      currentSection = currentSection === 'nodes' ? 'nodes' : currentSection;
    }

    const keyValue = trimmed.match(/^(?:-\s+)?([^:]+):\s*(.*)$/);
    if (!keyValue) continue;
    const key = keyValue[1].trim();
    const value = parseScalar(keyValue[2]);

    if (currentSection === 'metadata' && indent <= 2 && ['name', 'fileKey', 'nodeId'].includes(key)) {
      metadata[key] = value;
      if (key === 'name') rootName = value;
      continue;
    }

    if (currentSection !== 'nodes') continue;

    if (trimmed.startsWith('- ')) {
      while (stack.length > 1 && stack[stack.length - 1].indent >= indent) stack.pop();
      const parent = stack[stack.length - 1].node;
      const node = { type: 'UNKNOWN', children: [] };
      node[key] = key === 'id' ? normalizeNodeId(value) : value;
      if (!parent.children) parent.children = [];
      parent.children.push(node);
      stack.push({ indent, node });
      continue;
    }

    const current = stack[stack.length - 1].node;
    if (!current || current === stack[0].node) continue;

    if (key === 'id') {
      current.id = normalizeNodeId(value);
      continue;
    }
    if (key === 'children') {
      continue;
    }
    if (key === 'componentProperties' || key === 'componentPropertyReferences') {
      current[key] = current[key] || {};
      continue;
    }
    if (current.componentProperties && !['name', 'type', 'text', 'characters', 'layout', 'fills', 'strokes', 'componentId'].includes(key)) {
      current.componentProperties[key] = value;
    }
    if (current.componentPropertyReferences && !['name', 'type', 'text', 'characters', 'layout', 'fills', 'strokes', 'componentId'].includes(key)) {
      current.componentPropertyReferences[key] = value;
    }
    current[key] = value;
  }

  return {
    metadata,
    nodes,
    name: rootName,
    type: 'DOCUMENT',
    children: nodes,
    _parseWarning: `Parsed YAML-like text with low confidence after JSON parse failed: ${jsonError.message}`,
  };
}

function getArgValue(name) {
  const index = args.indexOf(name);
  return index === -1 ? undefined : args[index + 1];
}

function normalizeNodeId(nodeId) {
  if (!nodeId) return undefined;
  return decodeURIComponent(String(nodeId)).replace(/^(node-id=)/, '').replace(/^(node_id=)/, '').replace(/-/g, ':');
}

function parseFigmaUrl(url) {
  if (!url) return {};
  try {
    const parsed = new URL(url);
    const parts = parsed.pathname.split('/').filter(Boolean);
    const modeIndex = parts.findIndex((part) => ['design', 'file', 'proto'].includes(part));
    const fileKey = modeIndex !== -1 ? parts[modeIndex + 1] : undefined;
    const nodeId = normalizeNodeId(parsed.searchParams.get('node-id'));
    return { fileKey, nodeId };
  } catch (_error) {
    return {};
  }
}

function asArray(value) {
  return Array.isArray(value) ? value : [];
}

function textOf(node) {
  if (!node || typeof node !== 'object') return '';
  if (typeof node.text === 'string') return node.text.trim();
  if (typeof node.characters === 'string') return node.characters.trim();
  return '';
}

function nodeName(node) {
  return String((node && node.name) || '').trim();
}

function componentName(node, componentMap) {
  const id = node && node.componentId;
  const component = id && componentMap && componentMap[id];
  return String((component && component.name) || node?.componentName || node?.component || '').trim();
}

function walk(node, visitor, parent) {
  if (!node || typeof node !== 'object') return;
  visitor(node, parent);
  for (const child of asArray(node.children)) {
    walk(child, visitor, node);
  }
}

function resolveRoot(input) {
  if (Array.isArray(input)) return input[0] || {};
  if (Array.isArray(input.nodes)) return input.nodes[0] || {};
  if (input.nodes && typeof input.nodes === 'object') {
    const first = Object.values(input.nodes)[0];
    if (first && first.document) return first.document;
    if (first) return first;
  }
  return input.document || input.node || input.data || input;
}

function collect(root, componentMap) {
  const items = [];
  walk(root, (node, parent) => {
    const name = nodeName(node);
    const text = textOf(node);
    const component = componentName(node, componentMap);
    const properties = node.componentProperties || {};
    items.push({ node, parent, name, text, component, properties });
  });
  return items;
}

function includesAny(value, keywords) {
  const lower = String(value || '').toLowerCase();
  return keywords.some((keyword) => lower.includes(String(keyword).toLowerCase()));
}

function isPlaceholder(value) {
  return ['label', 'button', 'table title', 'table text', 'please enter', 'page title'].includes(String(value || '').trim().toLowerCase());
}

function evidenceForText(value) {
  if (!value) return 'missing';
  return isPlaceholder(value) ? 'inferred' : 'confirmed';
}

function actionRole(item) {
  const combined = `${item.name} ${item.component}`;
  if (includesAny(combined, ['主按钮', 'primary'])) return 'primary';
  if (includesAny(combined, ['文本按钮'])) return 'link';
  if (includesAny(combined, ['纯icon', 'icon'])) return 'icon';
  if (includesAny(combined, ['线框', 'secondary'])) return 'secondary';
  return 'unknown';
}

function candidateType(item) {
  const combined = `${item.name} ${item.component} ${item.text}`;
  if (includesAny(combined, ['lov'])) return 'lov';
  if (includesAny(combined, ['时间段', 'date range', 'start date', 'ending date'])) return 'dateRange';
  if (includesAny(combined, ['时间', '日期', 'date', 'calendar'])) return 'date';
  if (includesAny(combined, ['下拉', 'select', 'dropdown'])) return 'lookup';
  if (includesAny(combined, ['附件', 'upload', 'attachment'])) return 'attachment';
  if (includesAny(combined, ['文本输入框', '输入框', 'search', '模糊搜索'])) return 'string';
  return 'unknown';
}

function isRequired(item) {
  const value = item.properties && (item.properties['必输'] || item.properties['必填'] || item.properties.required);
  if (value === true || value === 'true') return true;
  let foundStar = false;
  walk(item.node, (node) => {
    if (textOf(node) === '*') foundStar = true;
  });
  return foundStar;
}

function findTitle(items, rootName) {
  const titleTexts = items
    .filter((item) => item.node.type === 'TEXT' && item.text)
    .map((item) => item.text);
  const nonPlaceholder = titleTexts.find((text) => text && !isPlaceholder(text) && text !== '*');
  if (rootName && !isPlaceholder(rootName) && rootName !== 'Framelink YAML-like input') return rootName;
  return nonPlaceholder || titleTexts.find((text) => /page title/i.test(text)) || titleTexts[0] || 'Untitled Page';
}

function extractActions(items) {
  return items
    .filter((item) => includesAny(`${item.name} ${item.component}`, ['按钮', 'button']))
    .slice(0, 20)
    .map((item) => ({
      label: item.text || (actionRole(item) === 'icon' ? 'icon' : 'Button'),
      role: actionRole(item),
      scope: 'page',
      permission: 'missing',
      behavior: 'missing',
      notes: [`figmaNodeId: ${item.node.id || 'unknown'}`],
    }));
}

function extractTabs(items) {
  const tabItems = items.filter((item) => includesAny(`${item.name} ${item.component}`, ['一级tab', 'tab']));
  return tabItems.map((item) => {
    let label = '';
    walk(item.node, (node) => {
      const text = textOf(node);
      if (!label && text && text !== '*') label = text;
    });
    return {
      label: label || 'Tab',
      evidence: evidenceForText(label),
      notes: [`figmaNodeId: ${item.node.id || 'unknown'}`],
    };
  });
}

function extractFields(items) {
  return items
    .filter((item) => includesAny(`${item.name} ${item.component}`, ['表单', '文本输入框', '输入框']))
    .filter((item) => item.node.type === 'INSTANCE')
    .slice(0, 60)
    .map((item) => {
      let label = '';
      walk(item.node, (node) => {
        const text = textOf(node);
        if (!label && text && !['*', 'Please enter'].includes(text)) label = text;
      });
      return {
        label: label || 'Label',
        candidateType: candidateType(item),
        required: isRequired(item),
        layout: includesAny(`${item.name} ${item.component}`, ['上下结构', '紧凑']) ? 'verticalCompact' : 'unknown',
        evidence: evidenceForText(label || 'Label'),
        notes: [`figmaNodeId: ${item.node.id || 'unknown'}`],
      };
    });
}

function extractFilterFields(items) {
  return items
    .filter((item) => !includesAny(`${item.name} ${item.component}`, ['icon/', 'filter2']))
    .filter((item) => includesAny(`${item.name} ${item.component}`, ['筛选项', '模糊搜索', 'filter field', 'search', '查询']))
    .slice(0, 30)
    .map((item) => {
      let label = item.text;
      walk(item.node, (node) => {
        const text = textOf(node);
        if (!label && text) label = text;
      });
      return {
        label: label || 'filter',
        candidateType: candidateType(item),
        evidence: evidenceForText(label || 'filter'),
        notes: [`figmaNodeId: ${item.node.id || 'unknown'}`],
      };
    });
}

function extractColumns(items) {
  return items
    .filter((item) => includesAny(`${item.name} ${item.component}`, ['表头', 'table title']))
    .filter((item) => item.node.type === 'INSTANCE' || /table title/i.test(item.text))
    .slice(0, 80)
    .map((item) => {
      let label = item.text;
      walk(item.node, (node) => {
        const text = textOf(node);
        if (!label && text) label = text;
      });
      return {
        label: label || 'Table title',
        candidateType: 'unknown',
        evidence: evidenceForText(label || 'Table title'),
        notes: [`figmaNodeId: ${item.node.id || 'unknown'}`],
      };
    });
}

function collectImageRefs(items) {
  const refs = [];
  for (const item of items) {
    const combined = `${item.name} ${item.component} ${item.node.type || ''}`;
    const hasImage =
      item.node.imageRef ||
      item.node.imageHash ||
      item.node.svg ||
      includesAny(combined, ['image', '图片', 'svg', 'icon', '图标']);

    if (!hasImage) continue;

    refs.push({
      nodeId: item.node.id,
      name: item.name || item.component || 'asset',
      type: item.node.svg ? 'svg' : includesAny(combined, ['icon', '图标']) ? 'icon' : includesAny(combined, ['image', '图片']) ? 'image' : 'unknown',
      status: item.node.imageRef || item.node.imageHash || item.node.svg ? 'referenced' : 'missing',
      notes: [`figmaNodeId: ${item.node.id || 'unknown'}`],
    });
  }
  return refs.slice(0, 40);
}

function collectStyleEvidence(items) {
  const evidence = [];
  for (const item of items) {
    const styles = item.node.styles || item.node.style || {};
    for (const [name, value] of Object.entries(styles).slice(0, 12)) {
      evidence.push({
        name,
        value: typeof value === 'string' ? value : JSON.stringify(value),
        evidence: 'confirmed',
        notes: [`figmaNodeId: ${item.node.id || 'unknown'}`],
      });
    }
  }
  return evidence.slice(0, 40);
}

function collectComponentEvidence(items) {
  return items
    .filter((item) => item.component || item.node.type === 'INSTANCE' || Object.keys(item.properties || {}).length)
    .slice(0, 60)
    .map((item) => ({
      figmaName: item.component || item.name || 'Unnamed component',
      componentType: item.node.type,
      evidence: 'confirmed',
      notes: [
        `figmaNodeId: ${item.node.id || 'unknown'}`,
        Object.keys(item.properties || {}).length ? `properties: ${Object.keys(item.properties).join(', ')}` : 'properties: none',
      ],
    }));
}

function isComponentShowcase(items) {
  const text = items.map((item) => `${item.name} ${item.text}`).join(' ');
  return includesAny(text, ['表格展示', '基础', '行内编辑', '树形', '拖拽', '禁用行', '组件展示', '组件规范']);
}

function inferPageType({ fields, columns, filterFields, tabs, items }) {
  if (isComponentShowcase(items)) return 'componentShowcase';
  if (fields.length && columns.length) return 'formWithTable';
  if (columns.length && (filterFields.length || tabs.length)) return 'list';
  if (fields.length) return 'form';
  if (columns.length) return 'list';
  return 'unknown';
}

function buildSchema(input, urlInfo, rawInputFormat) {
  const root = resolveRoot(input);
  const metadata = input.metadata || {};
  const componentMap = metadata.components || input.components || {};
  const items = collect(root, componentMap);

  const rootName = nodeName(root);
  const title = findTitle(items, rootName);
  const actions = extractActions(items);
  const tabs = extractTabs(items);
  const fields = extractFields(items);
  const filterFields = extractFilterFields(items);
  const columns = extractColumns(items);
  const pageType = inferPageType({ fields, columns, filterFields, tabs, items });
  const imageRefs = collectImageRefs(items);
  const styleEvidence = collectStyleEvidence(items);
  const componentEvidence = collectComponentEvidence(items);
  const evidenceNotes = [
    'Generated by extract-page-schema.js',
    'This is a conservative draft; business contracts remain missing until confirmed.',
  ];

  if (rawInputFormat === 'yamlLike') {
    evidenceNotes.push('Input was parsed from YAML-like text with low confidence. Prefer saved Framelink JSON for reliable extraction.');
  } else if (rawInputFormat === 'framelinkJsonWrapper') {
    evidenceNotes.push('Input was a Framelink JSON wrapper with YAML-like tool text in data[0].text.');
  }

  if (input._parseWarning) {
    evidenceNotes.push(input._parseWarning);
  }

  const regions = [];
  regions.push({
    id: 'header',
    type: 'header',
    title,
    evidence: evidenceForText(title),
    actions,
  });

  if (tabs.length) {
    regions.push({
      id: 'tabs',
      type: 'tabs',
      evidence: 'confirmed',
      children: tabs.map((tab, index) => ({ id: `tab${index + 1}`, type: 'custom', title: tab.label, evidence: tab.evidence })),
    });
  }

  if (fields.length) {
    regions.push({
      id: 'form',
      type: 'form',
      title: items.find((item) => /basic information/i.test(item.text))?.text,
      evidence: 'confirmed',
      fields,
    });
  }

  if (filterFields.length && pageType !== 'componentShowcase') {
    regions.push({
      id: 'filterBar',
      type: 'filterBar',
      evidence: 'confirmed',
      fields: filterFields,
    });
  }

  if (columns.length) {
    regions.push({
      id: 'table',
      type: 'table',
      title: items.find((item) => /^table$/i.test(item.text))?.text,
      evidence: 'confirmed',
      columns,
    });
  }

  return {
    source: {
      type: 'figma',
      mcpTool: 'framelink',
      selectionUrl: getArgValue('--url'),
      fileKey: urlInfo.fileKey || metadata.fileKey,
      nodeId: urlInfo.nodeId || normalizeNodeId(root && root.id),
      rootNodeName: rootName,
      rawInputFormat,
      evidenceNotes,
      imageRefs,
      styleEvidence,
      componentEvidence,
    },
    page: {
      name: title,
      type: pageType,
      layout: tabs.length ? 'tabs' : fields.length > 4 ? 'multiColumnForm' : 'unknown',
      confidence: rawInputFormat === 'yamlLike' || pageType === 'unknown' ? 'low' : 'medium',
    },
    regions,
    integration: {
      targetStack: 'unknown',
      route: 'missing',
      permission: 'missing',
      i18n: 'missing',
      dataContract: 'missing',
      assets: imageRefs.length ? 'inferred' : 'missing',
    },
    openQuestions: [
      '请确认目标技术栈和目标模块路径。',
      '请提供字段清单、字段名、字段类型和校验规则。',
      '请提供接口契约、权限码、菜单入口和 i18n 规则。',
    ],
  };
}

function main() {
  const raw = readInput();
  const { input, rawInputFormat } = parseInput(raw);
  const urlInfo = parseFigmaUrl(getArgValue('--url'));
  const schema = buildSchema(input, urlInfo, rawInputFormat);
  const pretty = args.includes('--pretty');
  process.stdout.write(JSON.stringify(schema, null, pretty ? 2 : 0));
  process.stdout.write('\n');
}

main();
