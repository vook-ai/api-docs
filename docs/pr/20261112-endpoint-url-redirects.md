# Redirect renamed API-reference endpoint URLs

## Functional summary

7 old API Reference page URLs, 404 since the 2026-09-14 → 09-16 spec syncs,
now redirect to the renamed pages. Search Console (vook.ai property, Not found
export, 2026-11-12) flagged `/api-reference/chats-api-v1/list-the-chats-for-a-transcription`.

## Implementation details

- `docs.json`: top-level `redirects`, 7 `{source, destination}` entries. No
  `permanent` field: Mintlify defaults to 308.[^mint]
- Cause: Mintlify builds each endpoint URL as
  `/api-reference/<slug(tag)>/<slug(summary)>`. Syncs `71fb1c6`, `de5517d`,
  `898ee9d`, `87dd99e` renamed tags (`chats-api-v1` → `chats-api-v1-beta`) and
  summaries. Old URLs found by diffing slugs of every historical
  `api-reference/openapi.json` against `b52422b`.
- 2 old create-job URLs both land on
  `create-a-transcription-job-from-an-uploaded-file-or-a-url`.
- `.claude/scripts/provision-worktree.sh`: new, minimal. `/worktree` requires
  it; repo has no env files or deps, so it only checks it runs in a worktree.
- Recurrence: any sync changing a tag or summary moves a page. Each sync PR
  should diff old vs new slugs and add redirects.

## Testing

- Every destination present in slugs rebuilt from current
  `api-reference/openapi.json`; no source collides with a live page.
- Pre-merge live check 2026-11-12 09:50 UTC: 7 old → 404, 7 new → 200.
- After deploy: re-check each old URL answers 308 to its new URL.

## Behaviour change

Developers following old links or search results to 7 renamed API Reference pages now land on the current page instead of a 404. Wiki: `public-api`

[^mint]: Mintlify docs, Redirects — https://www.mintlify.com/docs/create/redirects (no version shown), accessed 2026-11-12 UTC.
    > "By default, redirects are permanent (308). To use a temporary redirect (307), set `permanent` to `false`."
