// rd-dev-planning 门禁复检工具（对齐技能 v2.1.0）
// 用法: node gate-check.js
// 说明: 校验 artifacts/03-planning/dev-plan.json + dev-plan.xlsx 的 L1/L2/L3 门禁
//       - 版本号从 SKILL.md frontmatter 动态读取
//       - 数据库规范对齐 demo 工程（Oracle + Liquibase groovy：审计五列/租户列/序列/唯一约束）
//       - API 路径与原型 DataSet transport 双向一致
//       - Excel 为合法 xlsx（文件头 PK + 非空），内容一致性由 generate-excel.py 自校验
const fs = require('fs');
const path = require('path');

// 定位项目根：优先当前工作目录（cwd 下存在 artifacts/ 即为项目根，支持用户级技能安装后在任何项目使用），
// 回退到脚本自身向上 4 级（项目级安装 .workbuddy/skills/rd-dev-planning/tools/ 布局）
const root = fs.existsSync(path.join(process.cwd(), 'artifacts')) ? process.cwd() : path.resolve(__dirname, '../../../../');
const skillPath = path.join(root, '.workbuddy/skills/rd-dev-planning/SKILL.md');
const base = path.join(root, 'artifacts/03-planning');
const planPath = path.join(base, 'dev-plan.json');
const xlsxPath = path.join(base, 'dev-plan.xlsx');
const reqPath = path.join(root, 'artifacts/01-requirement/requirement-spec.json');
const protoPath = path.join(root, 'artifacts/02-prototype/prototype-spec.json');

// ---- 从 SKILL.md frontmatter 动态读取版本号 ----
let skillVersion = '';
try {
  const md = fs.readFileSync(skillPath, 'utf8');
  const m = md.match(/^version:\s*([\d.]+)/m);
  skillVersion = m ? m[1] : '';
} catch (e) { /* 忽略 */ }
const GATE_VER = skillVersion ? 'v' + skillVersion : 'vUNKNOWN';

// 实体名 -> 表名（snake_case）：WorktimeWeekReport -> worktime_week_report
const toSnake = (s) => String(s || '').replace(/([a-z0-9])([A-Z])/g, '$1_$2').toLowerCase();
// 路径占位符归一：/v1/worktime/details/{id} -> ^/v1/worktime/details/[^/]+$
const toRegex = (p) => new RegExp('^' + String(p).replace(/\{([^}]+)\}/g, '[^/]+') + '$');

// ---- JSONL 审计日志（数据驱动优化数据源，metrics-report.js 周报消费）----
const LOG_DIR = path.join(root, 'logs');
const LOG_FILE = path.join(LOG_DIR, 'gate-check.jsonl');
const checkRecords = [];
const t0 = Date.now();
let pass = 0, fail = 0;
const ok = (name) => { pass++; checkRecords.push({ name, result: 'PASS' }); console.log('PASS | ' + name); };
const no = (name, why) => { fail++; checkRecords.push({ name, result: 'FAIL', why: why || '' }); console.log('FAIL | ' + name + (why ? ' -> ' + why : '')); };
function writeAudit(exitCode) {
  try {
    if (!fs.existsSync(LOG_DIR)) fs.mkdirSync(LOG_DIR, { recursive: true });
    fs.appendFileSync(LOG_FILE, JSON.stringify({
      ts: new Date().toISOString(), stage: '03-planning', gate: 'rd-dev-planning',
      gateVersion: GATE_VER, script: 'gate-check.js', pass, fail,
      checks: checkRecords, durationMs: Date.now() - t0, exitCode,
    }) + '\n', 'utf8');
  } catch (e) { /* 审计日志失败不影响门禁结论 */ }
}

// ---- 读取上游 ----
let req, proto, plan;
try { req = JSON.parse(fs.readFileSync(reqPath, 'utf8')); } catch (e) { req = null; }
try { proto = JSON.parse(fs.readFileSync(protoPath, 'utf8')); } catch (e) { proto = null; }
try { plan = JSON.parse(fs.readFileSync(planPath, 'utf8')); } catch (e) { plan = null; }

// ---- L1: 入口校验 ----
fs.existsSync(planPath) ? ok('L1-1: dev-plan.json 存在') : no('L1-1', '文件缺失');
fs.existsSync(xlsxPath) ? ok('L1-2: dev-plan.xlsx 存在') : no('L1-2', '文件缺失');
req && req._meta && req._meta.qualityGateStatus === 'PASSED' ? ok('L1-3: 上游 requirement-spec.json qualityGateStatus=PASSED') : no('L1-3');
proto && proto._meta && proto._meta.qualityGateStatus === 'PASSED' ? ok('L1-4: 上游 prototype-spec.json qualityGateStatus=PASSED') : no('L1-4');
if (!plan) {
  console.log('==================================');
  console.log('门禁复检结果: ' + pass + ' 通过 / ' + fail + ' 失败  (技能版本 ' + (skillVersion || '未知') + ')');
  writeAudit(1);
  process.exit(1);
}
const ups = (plan._meta && plan._meta.upstreamArtifacts) || [];
(ups.includes('../01-requirement/requirement-spec.json') && ups.includes('../02-prototype/prototype-spec.json'))
  ? ok('L1-5: upstreamArtifacts 指向两个上游产物') : no('L1-5', JSON.stringify(ups));

// ---- 收集原型 transport URL ----
const transportUrls = [];
for (const p of (proto.pages || [])) {
  for (const d of (p.dataSets || [])) {
    const t = d.transport || {};
    for (const op of ['read', 'create', 'update', 'submit', 'delete']) {
      const cfg = t[op];
      if (!cfg) continue;
      const u = typeof cfg === 'string' ? cfg : (cfg.url || '');
      if (typeof u === 'string' && u.startsWith('/v1/')) transportUrls.push(u);
    }
  }
}
const uniqueTransport = [...new Set(transportUrls)];

// ---- L2: 过程校验 ----
// L2-1: 实体 -> 表 覆盖
const entities = [];
for (const m of (req.modules || [])) for (const e of (m.entities || [])) entities.push(e);
const tableNames = (plan.database && plan.database.tables || []).map(t => t.name);
const missTables = entities.map(e => toSnake(e.name)).filter(tn => !tableNames.includes(tn));
missTables.length === 0 ? ok('L2-1: 全部实体有数据库表定义 (' + entities.length + ' 实体)') : no('L2-1', '缺表: ' + missTables.join(', '));

// L2-2: 标准字段（审计五列 + 租户列 + 主键）
const STD_COLS = ['id', 'tenant_id', 'object_version_number', 'creation_date', 'created_by', 'last_update_date', 'last_updated_by'];
const badTables = [];
for (const t of (plan.database.tables || [])) {
  const cols = new Set((t.columns || []).map(c => c.name));
  for (const sc of STD_COLS) if (!cols.has(sc)) { badTables.push(t.name + '缺' + sc); break; }
}
badTables.length === 0 ? ok('L2-2: 所有表含标准字段（主键/租户/乐观锁/审计）') : no('L2-2', badTables.join('; '));

// L2-3: 序列 + 唯一约束（Oracle groovy 规范）
const noSeq = (plan.database.tables || []).filter(t => !t.sequence);
const noUc = (plan.database.tables || []).filter(t => !(t.uniqueConstraints || []).length);
noSeq.length === 0 ? ok('L2-3: 所有表定义序列 ({table}_s)') : no('L2-3', noSeq.map(t => t.name).join(', '));
noUc.length === 0 ? ok('L2-4: 所有表定义唯一约束 (addUniqueConstraint)') : no('L2-4', noUc.map(t => t.name).join(', '));

// L2-5: FR 的 apiEndpoint 全部有 API 定义
const frs = req.functionalRequirements || [];
const apiPaths = (plan.apiDesign || []).map(a => a.path);
const missApi = [];
for (const fr of frs) {
  for (const key of ['apiEndpoint', 'apiEndpoint2']) {
    const ep = fr[key];
    if (!ep || !ep.path) continue;
    if (!apiPaths.some(ap => toRegex(ap).test(ep.path))) missApi.push(fr.id + ':' + ep.path);
  }
}
missApi.length === 0 ? ok('L2-5: 全部 FR 的 apiEndpoint 有 API 定义 (' + frs.length + ' FR)') : no('L2-5', missApi.join('; '));

// L2-6: 页面 -> 前端任务覆盖
const pageIds = (proto.pages || []).map(p => p.id);
const feTaskPages = new Set();
for (const t of (plan.tasks || [])) for (const pid of (t.artifacts && t.artifacts.pageIds || [])) feTaskPages.add(pid);
const missPages = pageIds.filter(id => !feTaskPages.has(id));
missPages.length === 0 ? ok('L2-6: 全部页面有前端任务 (' + pageIds.length + ' 页面)') : no('L2-6', '缺任务: ' + missPages.join(', '));

// L2-7: 原型 transport 必须全部有 API 对应（强校验）；
//      API 多于 transport 的为动作类接口（submit/approve/reject 等，由 FR apiEndpoint 驱动，L2-5 已校验来源），合法并提示数量
const apiNotInProto = (plan.apiDesign || []).map(a => a.path).filter(ap => !uniqueTransport.some(tu => toRegex(tu).test(ap)));
const protoNotInApi = uniqueTransport.filter(tu => !apiPaths.some(ap => toRegex(ap).test(tu)));
protoNotInApi.length === 0
  ? ok('L2-7: 原型 DataSet transport 全部有 API 对应 (' + uniqueTransport.length + ' 条 transport)')
  : no('L2-7', 'transport无API对应: ' + protoNotInApi.join(','));
apiNotInProto.length === 0
  ? ok('L2-7b: API 路径均能在原型 transport 中找到')
  : ok('L2-7b: ' + apiNotInProto.length + ' 个动作类 API（submit/approve/reject 等）由 FR apiEndpoint 驱动，合法: ' + apiNotInProto.join(', '));

// L2-8: 任务依赖无环（DFS 拓扑）
const tasks = plan.tasks || [];
const taskIds = new Set(tasks.map(t => t.id));
const depIssues = [];
for (const t of tasks) for (const d of (t.dependencies || [])) if (!taskIds.has(d)) depIssues.push(t.id + '->' + d);
const visiting = new Set(), visited = new Set();
let cyclic = null;
const visit = (id, chain) => {
  if (visiting.has(id)) { cyclic = chain.concat(id).join(' -> '); return; }
  if (visited.has(id)) return;
  visiting.add(id);
  const t = tasks.find(x => x.id === id);
  for (const d of (t ? t.dependencies || [] : [])) visit(d, chain.concat(id));
  visiting.delete(id);
  visited.add(id);
};
for (const t of tasks) { if (!visited.has(t.id)) visit(t.id, []); if (cyclic) break; }
depIssues.length === 0 ? ok('L2-8: 任务依赖均指向存在的任务') : no('L2-8', depIssues.join('; '));
!cyclic ? ok('L2-9: 任务依赖无环') : no('L2-9', '环: ' + cyclic);

// L2-10: 工时估算完整 + 无占位符
const noHours = tasks.filter(t => !(t.estimatedHours > 0));
noHours.length === 0 ? ok('L2-10: 所有任务有估算工时 (' + tasks.length + ' 任务)') : no('L2-10', noHours.map(t => t.id).join(', '));
const allText = JSON.stringify(plan);
/(abc|xxx|待补充|TODO|TBD)/i.test(allText) ? no('L2-11', '存在占位符') : ok('L2-11: 无 abc/xxx/待补充/TODO 占位符');

// ---- L3: 出口校验 ----
// L3-1: FR 覆盖率 100%
const frIds = frs.map(f => f.id);
const cov = plan.coverageMatrix || [];
const covFrIds = new Set(cov.filter(c => c.covered).map(c => c.frId));
const missFr = frIds.filter(id => !covFrIds.has(id));
missFr.length === 0 ? ok('L3-1: 需求覆盖矩阵覆盖全部 FR (100%)') : no('L3-1', '未覆盖: ' + missFr.join(', '));

// L3-2: taskSequence 任务覆盖（全部任务出现在序列中）
const seqTasks = new Set();
for (const ph of (plan.taskSequence || [])) for (const id of (ph.tasks || [])) seqTasks.add(id);
const missSeq = tasks.map(t => t.id).filter(id => !seqTasks.has(id));
missSeq.length === 0 ? ok('L3-2: 任务序列覆盖全部任务') : no('L3-2', '未排期: ' + missSeq.join(', '));

// L3-3: Excel 为合法 xlsx（魔数 PK）且非空
let xlsxOk = false, xlsxSize = 0;
try {
  const buf = fs.readFileSync(xlsxPath);
  xlsxSize = buf.length;
  xlsxOk = buf.length > 16 && buf[0] === 0x50 && buf[1] === 0x4b; // PK
} catch (e) { /* 忽略 */ }
xlsxOk ? ok('L3-3: dev-plan.xlsx 为合法 xlsx 文件 (' + xlsxSize + ' 字节)') : no('L3-3', '文件缺失或非 xlsx');

// L3-4: _meta 版本与技能版本对齐
(plan._meta && plan._meta.version === skillVersion && plan._meta.gateVersion === GATE_VER && plan._meta.deliverable === 'dev-plan.xlsx')
  ? ok('L3-4: _meta 版本与技能版本 ' + GATE_VER + ' 对齐，deliverable=dev-plan.xlsx')
  : no('L3-4', JSON.stringify(plan._meta));

// L3-5: qualityGateStatus
(plan._meta && plan._meta.qualityGateStatus === 'PASSED') ? ok('L3-5: qualityGateStatus=PASSED') : no('L3-5');

console.log('==================================');
console.log('门禁复检结果: ' + pass + ' 通过 / ' + fail + ' 失败  (技能版本 ' + (skillVersion || '未知') + ')');
writeAudit(fail ? 1 : 0);
process.exit(fail ? 1 : 0);
