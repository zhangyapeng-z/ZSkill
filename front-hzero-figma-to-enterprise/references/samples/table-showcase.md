# Figma Samples - Table Showcase

## Included cases
- `H-ZERO 流光蓝表格展示`
- `H-ZERO 流光蓝表格规格`

## Shared takeaways
- These are table showcase/specification nodes, not business lists.
- They confirm table regions, column families, selection states, sort/filter hints, and inline-edit visuals.
- They do not confirm field names, pagination protocol, action permissions, or persistence behavior.

## PageSchema hints
- Use `componentShowcase` or `list` with a note that the node is not a business page.
- Map visual column families to candidate types only: selection, text, action, status/tag, switch, editor, Lov, number, select, time, drag.
- Put fields, pagination, sorting/filtering protocol, action permission, and row edit save protocol into `missing`.
