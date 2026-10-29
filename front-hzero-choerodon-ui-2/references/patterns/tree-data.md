# Choerodon Tree Data

Use for tree tables and hierarchical data.

## Minimal shape
- Choose nested tree data when the response already carries children.
- Choose flat parent-child data when hierarchy must be recovered from `idField` and `parentField`.
- Keep the final row shape compatible with the DataSet, not just the raw network payload.

## Non-runnable skeleton
- Nested model: children field and row shape待确认.
- Flat model: id field, parent field, root value, and final DataSet row shape待确认.
- Table: tree mode only after DataSet hierarchy model is confirmed.
- Async loading: append/load protocol待确认，暂不配置.

## Guardrails
- Confirm whether the project uses `children`, `childrenField`, or flat parent-child keys.
- Do not invent tree loading or transform behavior.
