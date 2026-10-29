# HZERO Layout Extension Patterns

## Scope
Use this reference for RootLayout, layout header extra, layout extra, workbench cards, user menu, global loading components, plugins, layout/theme extension points, or federated layout components.

These patterns are non-runnable until verified from project source. Confirm extension point availability, package name, exposed key, visibility rule, and project version before applying.

## Extension Order
1. Confirm extension position: RootLayout, header, layout extra, workbench card, user menu, plugin, or global component.
2. Confirm scope: parent project global, submodule contribution, tenant/project customization, or route-prefix layout.
3. Choose mechanism: runtime extension, federation exposure, route-prefix layout, or plugin.
4. Confirm `code`, `priority`, `entrySort`, package name, exposed key, and permission/visibility rules.
5. Check first-screen loading impact and whether `registerRegex` needs to load the contributing submodule.

## Mechanism Notes
- Global layout concerns should not live in ordinary page code.
- Submodule-provided UI should use confirmed federation exposure and consumption mechanisms.
- Workbench cards and layout extensions need stable code keys and ordering rules.
- If a card or extension fails after narrowing `registerRegex`, check legacy/customize/card loading assumptions before blaming the component.

## Confirmation Items
- Extension code/key and display name.
- Package name and exposed component key.
- Priority/order/entrySort.
- Role, tenant, or permission visibility.
- Route prefix and `registerRegex` impact.
- Whether target extension point exists in the project version.

## Risks
- Global layout changes affecting all modules.
- Header/layout UI depending on page render order.
- Wide `registerRegex` used to hide missing federation/card migration.
- Invented backend card code or exposed key.
- User menu or header entries without permission/tenant rules.
