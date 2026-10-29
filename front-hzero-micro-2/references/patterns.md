# HZERO Micro Frontend Patterns

## Runtime Notes
These are non-runnable micro-frontend configuration and consumption patterns. Confirm package names, exposed keys, route prefixes, public url, build artifact paths, deployment access paths, and project conventions before applying. Do not infer a remote URL from package names, route names, menu names, or environment names.

## Expose Component From Submodule

```ts
export default {
  hzeroMicro: {
    mfExposes: {
      '<confirmedExposeKey>': '<confirmedLocalPath>',
    },
  },
};
```

Notes:
- Confirm the submodule owns the component and the local path exists.
- Confirm exposed key naming convention.
- Rebuild and deploy the submodule so `remoteEntry.js` contains the exposure.

## Consume Federated Component

```tsx
// Use the project's confirmed federation consumer, such as MfComponent or getComponent.
// Do not replace this with direct import across package boundaries.
```

Notes:
- Confirm package name and exposed key.
- Confirm props contract before using the component.
- If loading fails, check `PACKAGE_PUBLIC_URL`, `packages/microConfig.json`, `window.mfRemotes`, `remoteEntry.js`, and `mfExposes`.

## Route-Based Submodule Loading

```ts
export default {
  hzeroMicro: {
    microConfig: {
      registerRegex: '\\/<confirmed-route-prefix>',
    },
  },
};
```

Notes:
- Match the actual route prefix that should trigger the submodule.
- Avoid broad `\/.*` unless confirmed first-screen loading or legacy extension behavior requires it.
- Validate that narrowing the regex does not break layout/card/customize extension loading.

## Deployment Check
- Confirm `PACKAGE_PUBLIC_URL` from project or environment evidence before using it.
- Confirm `${PACKAGE_PUBLIC_URL}/packages/microConfig.json` is reachable.
- Confirm the target package appears in micro config.
- Confirm runtime `window.mfRemotes` includes the target package and compare it with micro config.
- Confirm the target package build artifact contains `remoteEntry.js`.
- Confirm the deployed `remoteEntry.js` URL from micro config, runtime `window.mfRemotes`, deployment documentation, or Network evidence; do not invent it.
- Browser Console distinguishes resource load failures from component runtime errors.
