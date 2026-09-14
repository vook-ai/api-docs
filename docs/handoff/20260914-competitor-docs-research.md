# Competitor API docs research for open docs questions

Written 2026-09-14 from an `api-docs` session. Research only: nothing to edit in
the guides.

## What this is

`docs/questions/20260914-api-docs-open-questions.md` lists open docs-shape
questions on branch `feat/api-spec-sync` (host notes, base URL notes, webhook
signature docs, status wording, upload response). The user answers them one by
one and wants evidence of how competitors' public API docs handle each.

## Immediate next action

For each question in the questions doc, fetch the relevant pages of competitor
API docs and record how they handle it. Write findings to
`docs/research/20260914-competitor-docs-answers.md`.

## Read first

1. `docs/questions/20260914-api-docs-open-questions.md`: the questions.
2. Vendor list: `whisper-web` repo,
   `docs/tech/investigations/api-competitive-scan.md` (on `main`), header
   paragraph "Vendors:" and §3 (Gladia, closest competitor). Read only; do not
   edit whisper-web.
3. `.claude/rules/001-tone-style.md`: Gladia's docs are the stated reference
   model (`https://docs.gladia.io/api-reference`).

## Scope

**Vendors, in priority order:** Gladia, AssemblyAI, Deepgram, Speechmatics,
Rev AI, ElevenLabs Scribe. Others from the scan list only if these six give no
signal on a question (most of the rest are sync-only APIs with no job, upload
host or webhook, so they rarely apply).

**Per question, what to capture:**

| Question | Look for |
| --- | --- |
| Q1 two-host upload note | Upload-to-separate-host flows (presigned URL / upload endpoint returning a URL). Do guides warn against hardcoding the returned URL? Where: callout, field table, nowhere? |
| Q2 base URL note | Is the base URL repeated on every guide page, or stated once (overview/auth)? |
| Q3 webhook signatures | How customers get the signing secret (dashboard, key creation response, dedicated endpoint). Verification recipe format: languages, header names, replay window. Is signing documented before the secret is obtainable? |
| Q4 `locked`-like state | Any status for "result exists but withheld for billing". Scan says none withhold; confirm from docs, and note how they phrase balance-related states or errors. |
| Q5 `canceled` status | Meaning of canceled/cancelled job status, who triggers it, what the client should do. |
| Q6 upload response | What their upload endpoint returns, and whether guides show or tell you to ignore it. |

**Output format:** one `##` section per question. In each: a short table
(vendor, what they do, source URL), then 1 to 3 lines "Pattern" summarising the
majority and notable outliers. No recommendation beyond the pattern; the user
decides.

## Traps

- **Primary sources only:** vendor docs pages, cite the exact URL per row. No
  blog posts or third-party comparisons. If a page could not be fetched, say so
  in the row rather than filling it from memory.
- **Never put competitor or AI provider names in published docs.** The research
  file lives under `docs/`, which `.mintignore` excludes from docs.vook.ai.
  Confirm `.mintignore` still lists `docs/` before writing. Do not create any
  `.md`/`.mdx` outside `docs/`: Mintlify publishes every page file by URL, even
  when not in the navigation (verified: `docs.vook.ai/CLAUDE` served the repo's
  `CLAUDE.md` on 2026-09-14).
- Spelling varies (`canceled` / `cancelled`); search both.
- The scan in whisper-web is dated 2026-09-07/08 and covers billing and job
  status, not docs presentation. Use it for the vendor list and Gladia context,
  not as evidence for these questions.

## Start here

```
Read docs/handoff/20260914-competitor-docs-research.md.
Start with: fetch Gladia, AssemblyAI, Deepgram, Speechmatics, Rev AI and
ElevenLabs API docs for each question in
docs/questions/20260914-api-docs-open-questions.md, and write cited findings to
docs/research/20260914-competitor-docs-answers.md.
```
