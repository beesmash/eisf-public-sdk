# Package and Archive Publishing Strategy

GitHub Releases are the canonical public distribution point for v0.1.0.

## Python package registry

Before publishing to PyPI:

- reserve and verify the intended package name;
- enable account 2FA;
- prefer trusted publishing from GitHub Actions over long-lived API tokens;
- verify package metadata from a clean build;
- publish to a test registry first if desired;
- document the exact package name in the README only after publication succeeds.

## npm registry

Before publishing the TypeScript package:

- confirm ownership of the `@beesmash` scope;
- enable account 2FA;
- use provenance/trusted publishing where supported;
- test `npm pack` output before public publishing;
- publish only from a tagged, green release.

## Archival / DOI

For durable scholarly or industry citation, evaluate an archive that can snapshot a GitHub release and assign a persistent identifier such as a DOI. The archive record should point to the exact tagged release, not a moving `main` branch.

## Rule

Do not add registry badges or installation commands that imply a package is on PyPI/npm until it is actually published there.
