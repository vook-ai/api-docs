# API v1 docs drift — fixes to match the API

Source of truth: `whisper-web` branch `feat/api-v1`. Behaviour below checked in backend source and asserted by
`packages/backend/scripts/api-v1-walk.sh` (W) and `api-v1-chat-walk.sh` (C). Chat guide already matches; C needs
nothing beyond the billing/404 additions.

## Corrections — docs wrong today

1. **Free day.** No-subscription user gets one free transcript per day. 402 only when free day used **and** balance
   empty. Free day spent only when a transcript is delivered (backend ADR api/0002 §17). Fix `upload.mdx:166`,
   `transcribe-url.mdx:85`, `errors.mdx:55`, openapi 402 description ("balance is empty"). W:159-164.
2. **Upload token re-submit is idempotent.** Same `upload_token` submitted again → same job id, not an error. openapi
   `upload_token` says "single-use" (`openapi.json:818`) — reword; add one line to `upload.mdx`. W:195-196.
3. **`url_not_accessible` scope.** Covers dead links **and** unsafe URLs (loopback, private IPs, e.g.
   `https://127.0.0.1/…`). `errors.mdx:53` says only "answered with a 4xx". W:258.
4. **Empty transcription (no speech).** Job `completed`, transcription `status: empty`, `has_transcription: false`.
   Transcript read → `200`, `plain_text: null` (both scopes). Every export format → `204`, no body. Guide only covers
   not-ready → 409. Add the case to `retrieve-export.mdx` (near :114, :159). W:470-488.
5. **`page_size` above 100 is clamped, not rejected.** openapi schema carries `maximum: 100`, contradicting its own
   description. Drop `maximum` or state clamp. W:277-280.

## Additions — API does it, docs silent

- `name` omitted on URL submit → last path segment of the URL (`transcribe-url.mdx:78`). W:250, W:465.
- GET `/transcriptions/{id}` after delete → 404 (`retention.mdx:37` covers transcript reads only). W:328.
- Balance can go negative: a job admitted on a low balance is charged in full at settle; next submit → 402. W:429-440.
- Export content types: pdf `application/pdf`, docx
  `application/vnd.openxmlformats-officedocument.wordprocessingml.document`, html `text/html`, md `text/markdown`, srt
  `text/plain`. W:412-415.
- md export labels speakers `Speaker N`. W:426.
- `speaker_count` on transcription: in openapi, absent from `retrieve-export.mdx`. W:398.
- GET `/transcription-jobs` accepts `search`, `in_progress`, `page` (openapi yes, `retrieve-export.mdx:27` no).
- Chat: turns bill API credits (can return 402); web-app turns on the same chat do not. Chat 404s (unknown
  transcription, unknown chat, transcription deleted) — in openapi, not in `chat.mdx`. C:149, C:168, C:191-199, C:258-266.
- Webhook deliveries go out on a 30 s tick; `webhooks.mdx:133` says "when the job finishes".
- Missing `file_name` with `upload_token` → `400 invalid_request` **without** `validation_errors`; `errors.mdx:32`
  implies all validation 400s carry them. W:184.

Minor: `webhooks.mdx:111` strips spaces in `X-Vook-Signature` parts; API emits `v1=<hex>(,v1=<hex>)*`, no spaces.

## Keep out of docs

`backend_url` on job submit — dev-only override (ngrok callback). Scripts send it; not public.

## Spec snapshot

Do not re-curl `openapi.json` from prod (`README.md:43`) for these — `feat/api-v1` is not deployed. Pull from a local
backend running the branch: `curl -s http://localhost:8000/api/v1/docs-json -o api-reference/openapi.json`, then
re-check fixes 2 and 5 in the regenerated file (they may need the backend DTO changed rather than a docs edit).

## Why it drifted

- `openapi.json` is a prod snapshot; unreleased branch behaviour never reaches it.
- Last sync 2026-09-14 (`71fb1c6`, `de5517d`). Same day the branch shipped free day (#1952), empty-export 204, URL
  refusals (#1956), snake_case rename; chat beta (#1970) on 09-15.
- Guides are hand-written, not generated from DTOs.
- Walk scripts assert the backend, not the docs — prose drift fails nothing.
- Separate repos; no API PR requires an `api-docs` change.
