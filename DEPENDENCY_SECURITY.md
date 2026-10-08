# Dependency security review — 5 October 2026

Next.js and eslint-config-next are aligned at 16.3.8; all direct Tiptap packages at 3.31.4. The unused shadcn CLI dependency was removed; generated UI components do not import it. Supported manifest ranges were resolved together from a clean directory, without force or legacy peer bypasses. The lockfile records the resulting exact dependency graph.

SheetJS uses the version-pinned official `https://cdn.sheetjs.com/xlsx-0.20.3/xlsx-0.20.3.tgz` distribution and SHA-512 lockfile integrity. The public npm `xlsx` package is obsolete, as documented at https://docs.sheetjs.com/docs/getting-started/installation/nodejs/. SheetJS CE retains its Apache-2.0 license. Moving to the official distribution does not mean registry audit alone validates this package: CSV/XLSX import, export, workbook structure, malformed inputs, and resource bounds require explicit regression checks.

## Temporary development-tool exception

- Advisory: https://github.com/advisories/GHSA-vfj7-8cjw-p6xm (braces recursion denial of service; no patched release listed on the review date).
- Exact chain: eslint-config-next → @next/eslint-plugin-next → fast-glob → micromatch → braces. All five audit entries originate from this one advisory.
- Reachability: eslint-config-next is a development dependency. Its rules use getRootDirs, which invokes fast-glob for configured `settings.next.rootDir` patterns. With no such setting it returns the repository working directory directly. These patterns come from reviewed ESLint configuration. HTTP requests, CRM fields, file imports, and user-facing Next.js execution do not call this ESLint helper. The production dependency audit must remain free of all high/critical advisories; any change making this chain a runtime dependency fails the gate.
- Scope: only this exact advisory and these five package names. A different advisory on any of the same packages fails CI. Audit/network/report failures also fail CI.
- Owner: Crusource frontend maintainers.
- Expires: 4 November 2026, 00:00 UTC. Review the upstream fix before expiry; do not silently extend it.
- Mitigation: keep lint configuration/patterns under reviewed repository control, run lint only in the CI job, and do not expose a lint endpoint. Untrusted PR workflow changes require the normal repository review.
- Decision: retain the matching Next.js 16 lint package. The suggested downgrade to Next.js 14's lint configuration is incompatible with this application's framework and is not an acceptable security remediation.

`npm run audit` evaluates both runtime and full reports and enforces this exact expiring exception. `npm audit` still reports the development-only chain; it must not be described as a zero-vulnerability full audit.
