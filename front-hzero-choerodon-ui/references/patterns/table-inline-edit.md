# Choerodon Table Inline Edit

Use for editable tables that submit through a `DataSet`.

## Minimal shape
- Use columns with `editor` or built-in inline edit mode.
- Keep row commands aligned with the project's confirmed command pattern.
- For large tables, evaluate pagination or virtual rendering before adding heavy renderers.

## Non-runnable skeleton
- DataSet: primary key, editable fields, validation, and submit protocol待确认.
- Table: prefer built-in inline edit mode or column `editor` when project style confirms it.
- Commands: edit/save/delete/remove semantics待项目写法确认.
- Transport:待确认，暂不配置.

## Guardrails
- Avoid custom editing state when built-in inline edit already covers the interaction.
- Do not invent save or delete protocol details.
