# Handoff: CI tripwire for snake_case on the public API docs

Written 2026-09-14. Product ruling: every field on `/api/v1` is `snake_case`, no exceptions (recorded in
`whisper-web/docs/handoff/20260914-api-v1-snake-case-envelopes.md`). The backend rename is done on `feat/api-v1`
(uncommitted there at time of writing). This repo's spec snapshot and guides were flipped to match on
`feat/api-spec-sync` (PR #3). Nothing enforces it yet. This handoff is the check that keeps it true.

## Current state

- **This repo has no CI.** No `.github/`, no `package.json`, no lint. Mintlify builds from `docs.json` on push; that
  is the only automation. Verified by `ls -a`.
- Two throwaway scripts exist in `tmp/` (git-ignored, so **only on the author's machine**; copy them out before they
  vanish):
  - `tmp/camel_fields.py`: walks `api-reference/openapi.json`, prints every camelCase property per schema and which
    path serves it. Key-only walk, already skips values.
  - `tmp/walk_casing.py`: hits a running backend and reports camelCase keys per response. Needs a live container and a
    dev key; not CI material, but its `keys()` walker is the reusable part.
- The backend side of the guard (a test over the generated Swagger doc) is a whisper-web item, not this repo's. It is
  mentioned in the whisper-web handoff above; do not build it here.

## Immediate next action

Add `.github/workflows/lint.yml` running one script on every push and PR, exit 1 on any hit:

1. **Spec keys.** Every property name under `components.schemas.*.properties`, every `parameters[].name`, and every
   key inside `requestBody` schemas in `api-reference/openapi.json`, against `[a-z][A-Z]`. Keys only, never values.
2. **Guide examples.** Every JSON key inside ```` ```json ```` fences in `*.mdx`. Parse the block; if it is not valid
   JSON, regex the `"key":` positions instead (a few examples carry `…` placeholders).
3. **Em dashes.** `—` anywhere in `*.mdx` fails. Same zero tolerance as `.claude/rules/001-tone-style.md`; cheap to add
   in the same script.

Python 3, no dependencies, so the workflow is `actions/checkout` plus `python3 scripts/lint-docs.py`. Put the script
in `scripts/`, not `tmp/`.

## Traps

- **No allowlist.** The moment the script carries an exceptions list the rule erodes. If a real exception appears, it is
  a backend bug, not a lint exception.
- **Values that look like keys.** `SPEAKER_00`, ISO timestamps, `transcription_job.resolved`, `vk_live_…` all pass
  `[a-z][A-Z]` or look like identifiers. Walk dict keys only; never regex the raw file for the casing check.
- **The spec is a generated snapshot.** A hit in `openapi.json` means the backend regressed or the sync was wrong.
  Never patch the JSON by hand (`CLAUDE.md`); re-sync from `/api/v1/docs-json` and re-add the `servers` block.
- **The `servers` block is hand-added on every sync.** Not a casing concern, but if the lint ever validates structure,
  it must expect that block to be present in the repo copy and absent in the raw `/docs-json` output.
- **Two JSON blocks are not API bodies.** `docs.json` (Mintlify config) and anything under `docs/` are out of scope;
  lint only `api-reference/openapi.json` and the top-level `*.mdx`.
- **`prompts/` at the repo root** is unrelated to the docs content. Leave it out of the lint.

## Start here

```
Read docs/handoff/20260914-snake-case-ci-tripwire.md — it has the full state.
Start with: write scripts/lint-docs.py (spec keys, mdx JSON keys, em dashes), then .github/workflows/lint.yml around it.
```
