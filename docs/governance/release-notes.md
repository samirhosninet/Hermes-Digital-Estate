# Release Notes

## v0.1.1

Release readiness update for the GitHub profile distribution.

- Hardened the local setup wizard with localhost-only serving, dynamic port selection, safer credential persistence, and launcher diagnostics.
- Added the local staging distribution builder so releases are built from manifest-approved artifacts only.
- Added the Arabic operator runbook as a distribution artifact.
- Tightened the pre-GitHub release gate so CI and documentation validate staging output, not only the development workspace.
- Set the canonical GitHub distribution source to `github.com/samirhosninet/Hermes-Digital-Estate`.

No Hermes core runtime changes are included in this release.
