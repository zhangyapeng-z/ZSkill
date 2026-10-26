# 工程定位与案例

来源为 2026-10-22 本地检查，运行技能时核实路径和版本。

- 工程：D:/00-ZhangYP/20-Product/front-code/pms-front
- demo 模块：packages/hpis-demo-front；页面 src/pages/demo；路由 config/config.ts。
- 主模块登记：根 config/packages-config.js，已包含 hpis-demo-front。
- 公共 mock：模块 src/utils/mockStore.js；createMockStore/createMockAxios，列表 {content,totalElements}，API 页码从 0 起。
- 产品 C7N 配置：node_modules/hzero-front/lib/utils/c7nUiConfig.js，只读参考，不修改依赖。
- 已观察到 React 16、Umi 3、choerodon-ui 1.6.9-alpha.25；实际安装版本优先。
- 当前 .trae/rules/前端代码开发规范.md 可作为工程规范材料。

## 德赛参考（按需读取）

- desay-tco-demo-report/售前原型转DEMO-技能手册.md：六步法和验收。
- sdd-workspace/changes/tco-part-data-mgmt 等：需求、设计和任务记录。
- 模块 src/pages/demo/partEntry：列表及交互；partShared、strategyShared 的 sharedStores.js：共享数据；listShared：筛选、看板适配。
- 原型候选 sdd-workspace/css。按用户输入找具体文件，旧客户材料不自动当新需求。

## 飞码资料（可选，不是运行依赖）

插件 ZIP：D:/50-Downloads/Quark/hzero-copilot-1.3.0-beta.7/hzero-copilot/plugins/hzero-spec-0.3.5.zip。只读查阅相关文件，无需安装：

- hzero-spec/skills/front-hzero-figma-to-enterprise/templates/page-schema.md
- hzero-spec/skills/front-hzero-enterprise-page/
- hzero-spec/skills/front-hzero-choerodon-ui/
- hzero-spec/skills/front-hzero-renderer/
- hzero-spec/agents/frontend/frontend-design-agent.md

不存在时用目标源码与对应版本官方文档继续。

## 经验边界

- 默认 C7N CSS 或自行搭建平台壳不能证明产品主题一致；真实 HZERO 环境可能有动态主题配置。
- 日期字段不强制全转 string，应保留业务语义并正确 renderer。
- mock 换真实 API 不承诺零修改，先核对字段、状态、权限、分页契约。
- develop/master 已有部署链路，本地改动不代表线上更新，发布后仍需验证版本和入口。
