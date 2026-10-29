# 运行时配置 - 设计与契约

## 阅读路由
- 运行时配置 设计、契约冻结、question gate、事实确认或资源选择时读取。

## 事实确认契约
- 仅依赖自身说明和本地 `references/` 给出安全流程、硬规则、输出结构和不确定性处理。
- 本地 references 是模式和候选事实，不等同于目标项目契约。
- 输出具体 `app.tsx`、`routes-config.tsx`、runtime export、layout wrapper、请求拦截、导航 hook 或配置代码前，必须先从项目源码、现有配置或明确文档确认；确认不了就列为待确认项。
- 不要仅凭 HZERO 经验假设 `appInit` 可用；先确认目标项目 Umi runtime valid keys、项目模板或现有 `app.tsx`。
- 未确认 `appInit` 是目标项目 runtime valid key 前，禁止输出 `export async function appInit()` 作为可运行答案；若不支持或暂不确认，改推荐已确认 runtime export、模块级初始化、页面级初始化或局部 wrapper。
