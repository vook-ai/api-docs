---
description: Procedures for starting new features and saving work via Git
alwaysApply: true
---

# Team Workflow Rules (api-docs)

The shared canonical workflow is imported below. Repo-specific facts live in
**Repo overrides**. Keep this file thin: edit the shared body in the
`shared-claude` repo (`non-dev-workflow-base.md`), not here.

@~/.claude/vook-non-dev-workflow.md

## Repo overrides

- **Default branch:** `main`. Sync and hard-reset target is `origin/main`.
- Docs-only repo: no translation-key review, no API mocking, no `/cpo-qa` gate.
- The `docs/pr/` PR-doc step applies only if the repo has a `docs/pr/` folder; skip it otherwise and describe the change in the PR body instead.
