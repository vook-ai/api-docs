# Handoff — API docs walked against the backend, doc fixes owed

Written 2026-09-14 17:30. Every page under `docs.json` was followed to the letter against the `feat/api-v1` backend
(worktree container on 8000, staging ingress, RunPod GPU). Every documented call behaves as written; `openapi.json` is
byte-identical to the backend's `/docs-json` on the v1 paths and schemas. What remains is a list of doc errors and gaps,
measured against the API ADRs in `whisper-web/docs/tech/adr/api/`. The ADR side of the same walk (ADRs stale vs code)
is `whisper-web/docs/handoff/20260914-api-adr-drift.md`, not here.

Branch `feat/api-spec-sync` was being edited by another session during the walk; findings are against the 17:23 state
of the pages. Re-read a page before editing it.

## Immediate next action

Fix the two wrong statements first, then the gaps, in this order.

1. **`retrieve-export.mdx` status table, `locked` row** — says "unlocks once you top up your API credits". False.
   Unlock is the web app's minute pools only (`KnexPredictionRepository.unlockIfLocked` writes
   `cost_in_monthly_credits` / `cost_in_lifetime_credits`); ADR 0004 §10: `locked` describes web-app rows, never API
   work. Reword: web-app transcript locked behind the web paywall; API top-ups do not release it.
2. **Same table, `canceled` row** — ADR 0004 §10: never served. Either drop the row or say it is defensive.
3. **`webhooks.mdx` — signature verification is not implementable from the page.** Add: canonical string
   `${X-Vook-Timestamp}.${raw body}`, HMAC-SHA256, hex, header may carry several comma-separated `v1=` pairs during
   rotation (accept any match), and where the secret comes from: shown once with the key at mint. `authentication.mdx`
   never mentions that second secret — add it to "Mint a key". Source: ADR 0004 §8, ADR 0001 "A key carries a webhook
   signing secret".
4. **Error contract page (new, or a section on `introduction.mdx`)** — ADR 0006 §1–2: the body (`statusCode`, `code`,
   `message`, `timestamp`, `path`, optional `validation_errors`), `code` stable / `message` not, 4xx stop / 5xx retry
   with backoff / 429 retry after `Retry-After`. Then the code table from ADR 0006 §1, plus `job_failed` (in code, live
   `409`, missing from the ADR table — see the whisper-web handoff).
5. **Limits never stated anywhere**: `429 too_many_unsettled_jobs` with `Retry-After: 60` at 20 unresolved jobs, 5 h
   per submission (`file_too_long` lands asynchronously as the job's `error_code`), 6 GB (`url_too_large` on fetch),
   the job `error_code` vocabulary, the `url_*` split (400 fix-your-URL vs 502/504 retry). Sources: ADR 0003 "What
   bounds an accepted file", ADR 0006 §1.
6. **Retention page** — ADR 0005 "What we publish": four bounds (working audio 1 day; delete-on-request; account
   deletion 30 days; two-year inactivity), the sentence "no automatic expiry of API transcripts or audio", and
   `DELETE /api/v1/transcriptions/{id}` named next to it. Add to `docs.json` nav.
7. Smaller: `GET /api/v1/transcriptions` is account-wide (includes web-app transcripts); `GET /api/v1/transcription-jobs`
   list is never mentioned in the guides; free daily transcription and price appear nowhere.

## Verified on the walk (do not re-test)

Auth 200/401; upload init → ingress `201 {}` → submit `{id, status}`; idempotent re-submit; `file_name` required with
`upload_token`; URL submit; `url_not_accessible` on the docs' example URL; poll shape field-for-field;
`transcription_id` null while `queued`; transcript identical on both scopes; export pdf/srt, 400 on a missing boolean,
400 on `json`/`txt`, 204 on empty audio; 409 `job_not_completed` while running on transcript/export/DELETE, both
scopes; 409 `job_failed` on a failed job; list envelope, `page_size` clamp to 100, `search`, `in_progress=true` (visible
during `processing`, not `queued`); DELETE 204, idempotent, then 404 on transcript reads, job read still 200; failed job
DELETE → 204; `/webhooks/test` (example.com answers `delivered:false, 405`), `invalid_callback_url` on `http://` and
`:8443`; real deliveries signed and verified; 402 at balance 0.

## Traps

- `/webhooks/test` sample `data` lacks `callback_url`; a real delivery has it. Docs say "same shape as GET job". Backend
  fix (`api-v1-webhooks.service.ts:14`), not a doc fix — noted in the whisper-web handoff.
- Transcript paragraphs are camelCase (`speakerKey`, `startTimeSeconds`, `endTimeSeconds`) on a snake_case surface.
  The docs show it correctly; ADR 0006 §4 does not admit it. Do not "fix" the docs to snake_case.
- `page=0` is accepted and answers page 1. Not worth documenting.
- Walk artifacts: `whisper-web/.claude/worktrees/api-v1/tmp/docs-walk.sh`, `tmp/docs-walk.log`, `tmp/dw-*.json`.

## Start here

```
Read docs/handoff/20260914-docs-walk-findings.md — it has the full state.
Start with: fix the `locked` row in retrieve-export.mdx, then add signature verification to webhooks.mdx.
```
