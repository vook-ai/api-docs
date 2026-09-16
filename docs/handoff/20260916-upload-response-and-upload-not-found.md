# Handoff — upload response + `upload_not_found`

Written 2026-09-16 from a `whisper-web` session. Docs work for **vook-ai/whisper-web#1997**
(`fix/api-upload-presence-check`), which changes what `upload_url` returns and adds a submit-time error. PR open,
**not merged, not deployed** (checked on `gh` at write time).

## Current state

- **API side, done in #1997** (verified by its tests; see `docs/pr/20260916-api-upload-presence-check.md` in
  `whisper-web` for the full contract):
  - `POST {upload_url}` answers only after the file is stored. `201 { "size_bytes": N }`. Errors use the same body as
    `/api/v1` (`status_code`, `code`, `message`, `timestamp`, `path`): `401 unauthorized`, `413 upload_too_large`,
    `502 upload_failed` (retry the upload, same token).
  - `POST /api/v1/transcription-jobs` with a token whose file was never stored → `409 upload_not_found`. No job
    created, token still usable.
  - Job `error_code` gains `upload_not_found` (worker could not find the upload; rare backstop).
- **Prod today (before deploy)**: `upload_url` answers `{}` **before** storage; skipping step 2 gets `201 queued`, then
  job `failed` / `internal_error` ~2 min later (observed on prod job `25ebeb56-…`).
- **This repo**: nothing changed yet.

## Immediate next action

Wait for #1997 to merge and deploy (`gh pr view 1997 -R vook-ai/whisper-web`), then edit:

1. `upload.mdx` step 2 — show the `201 { "size_bytes" }` body; list the three upload error codes and what to do; say
   explicitly: wait for the upload response before step 3.
2. `upload.mdx` step 3 — add the `409 upload_not_found` case next to the existing `insufficient_api_credits` note.
3. `errors.mdx` — "Error codes" table: `upload_not_found` (409), `upload_too_large` (413), `upload_failed` (502).
   "Job error codes" table: `upload_not_found`.
4. Re-sync `api-reference/openapi.json` per `README.md` → "Updating the OpenAPI spec" (the 409 on create comes from
   the backend decorator).

## Traps

- **Do not publish before deploy.** The docs would promise a `size_bytes` body and a 409 that prod does not return.
- `upload.mdx` already says "A `2xx` status means the file is stored" — **false in prod today**, true only after #1997.
  Keep the sentence; it becomes correct.
- Status is **`201`**, not `200` (Nest POST default). The curl example writes the body to `upload-response.json`; don't
  imply it was empty before in customer-facing text — just document the new body.
- `upload_too_large`/`upload_failed`/`unauthorized` on `upload_url` are derived from the HTTP status by the ingress
  filter — there is no other code on that route.
- Never hand-edit `api-reference/openapi.json` (this repo's `CLAUDE.md`); wording fixes go to backend decorators in
  `whisper-web`.
- Large uploads: the request now also waits for server-side storage, so it runs longer. Worth one line telling clients
  not to set a short timeout.

## Start here

```
Read docs/handoff/20260916-upload-response-and-upload-not-found.md.
First check vook-ai/whisper-web#1997 is merged and deployed; only then update upload.mdx and errors.mdx and re-sync openapi.json.
```
