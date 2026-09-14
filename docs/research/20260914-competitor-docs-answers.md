# Competitor API docs: evidence for open docs questions

Answers evidence for `docs/questions/20260914-api-docs-open-questions.md`.
Researched 2026-09-14 from vendor docs sites only. Internal: `docs/` is in
`.mintignore`.

Caveats:

- Fetch tool summarizes pages; quotes are near-verbatim, not char-checked.
- Gladia and Speechmatics read via their official `llms-full.txt`; Rev AI async
  reference via its published OpenAPI spec (`docs.rev.ai/_spec/api/asynchronous/reference.yaml`),
  rendered page is JS-only.
- "No signal" = searched both page and site text, nothing found. Pages checked listed per row.
- Fallback vendors from the scan list not researched: the six gave signal on
  every question except Q1's core pattern (see there).

---

## Q1: Two-host upload note

| Vendor | What they do | Source |
| --- | --- | --- |
| Gladia | `POST /v2/upload` returns `audio_url` on same API host (`api.gladia.io/file/...`). No hardcoding warning. Quickstart: "pass the returned `audio_url` to the next step." | https://docs.gladia.io/api-reference/v2/upload/audio-file, https://docs.gladia.io/chapters/pre-recorded-stt/quickstart |
| AssemblyAI | `POST /v2/upload` returns `upload_url` on same host. No hardcoding warning. Only callout on upload reference: same-project API key required, else 403 "Cannot access uploaded file". | https://www.assemblyai.com/docs/api-reference/files/upload |
| Deepgram | No upload step. Raw bytes or JSON URL straight to `/v1/listen`. No host warning. | https://developers.deepgram.com/docs/pre-recorded-audio |
| Speechmatics | No upload step. Multipart on job create, or `fetch_data.url`. Closest note: "all requests relating to that job must use the same endpoint" (region). | https://docs.speechmatics.com/speech-to-text/batch/input, https://docs.speechmatics.com/get-started/regions |
| Rev AI | No upload step. Multipart on `POST /jobs` (<2GB) or `source_config.url`. No host warning. | https://docs.rev.ai/api/asynchronous/reference/ |
| ElevenLabs | No upload step. Multipart `file`, `source_url`, deprecated `cloud_storage_url`. Only host warning on data residency page: use correct API URL and key for isolated environment. | https://elevenlabs.io/docs/api-reference/speech-to-text/convert, https://elevenlabs.io/docs/overview/administration/data-residency |

**Pattern:** None of six upload to a separate host. The two with an upload step
(Gladia, AssemblyAI) return a URL on the main API host and just say "pass it to
the next step"; neither warns against hardcoding it. No direct precedent for a
two-host note either way.

---

## Q2: Base URL note

| Vendor | What they do | Source |
| --- | --- | --- |
| Gladia | Never stated in prose. Only in reference `servers` block; full URL repeated in every guide code sample. | https://docs.gladia.io/api-reference/authentication, https://docs.gladia.io/api-reference/index |
| AssemblyAI | Reference pages list US + EU servers. Quickstart hardcodes `base_url` in code. Dedicated region page with host table. | https://www.assemblyai.com/docs/pre-recorded-audio/select-the-region, https://www.assemblyai.com/docs/getting-started/transcribe-an-audio-file |
| Deepgram | No base URL on API overview. Host appears in guide code samples. Dedicated "Custom Endpoints" page for EU host swap, per-SDK config. | https://developers.deepgram.com/reference/deepgram-api-overview, https://developers.deepgram.com/reference/custom-endpoints |
| Speechmatics | Region host table stated once, on Authentication page ("Supported endpoints"). Guide code hardcodes `eu1` host (~30 places) with no per-page note. | https://docs.speechmatics.com/get-started/authentication, https://docs.speechmatics.com/speech-to-text/batch/output |
| Rev AI | Spec `servers` block; Get Started shows full URL once. EU host on dedicated Global Deployments page. | https://docs.rev.ai/api/asynchronous/get-started/, https://docs.rev.ai/api/global-deployments |
| ElevenLabs | Only in API reference and data residency page. Guides use SDK client, no URL. | https://elevenlabs.io/docs/api-reference/speech-to-text/convert, https://elevenlabs.io/docs/overview/administration/data-residency |

**Pattern:** No vendor puts a "The base URL is ..." note on each guide page.
Host is stated once (auth, region or reference page) and otherwise lives only
inside code samples. Multi-region vendors give regions their own page.

---

## Q3: Webhook signatures

| Vendor | Auth mechanism | Secret source | Verification recipe | Source |
| --- | --- | --- | --- | --- |
| Gladia | None documented. Dashboard-configured webhooks, payload = job `id`. | n/a | None | https://docs.gladia.io/chapters/pre-recorded-stt/quickstart, https://docs.gladia.io/api-reference/v2/pre-recorded/webhook/success |
| AssemblyAI | Customer-set header per request (`webhook_auth_header_name` / `_value`) + fixed IP allowlist (US, EU). | Customer chooses | None needed; Python/JS receive examples | https://www.assemblyai.com/docs/deployment/webhooks |
| Deepgram | Basic auth in callback URL, or `dg-token` header = API Key Identifier of submitting key. | Existing key identifier | None; compare header | https://developers.deepgram.com/docs/callback |
| Speechmatics | Customer-set `auth_headers` in `notification_config` + per-region IP allowlist. | Customer chooses | None | https://docs.speechmatics.com/speech-to-text/batch/notifications |
| Rev AI | Customer-set `auth_headers` in `notification_config` (stored encrypted). | Customer chooses | None | https://docs.rev.ai/api/asynchronous/webhooks/ |
| ElevenLabs | HMAC, `ElevenLabs-Signature: t=...,v0=...`. HMAC-SHA256 over `{timestamp}.{raw_body}` (search snippet only, Custom Channel page not fetched). | "shared secret generated upon creation of the webhook" (Developers > Webhooks dashboard). Show-once not stated. | SDK helpers only: `constructEvent` (JS), `construct_event` (Python); "verify the signature, validate the timestamp". No manual recipe, no replay window value. | https://elevenlabs.io/docs/eleven-api/resources/webhooks, https://elevenlabs.io/docs/eleven-api/guides/how-to/speech-to-text/batch/webhooks |

**Pattern:** 4 of 6 skip signing: customer supplies their own auth header
(AssemblyAI, Speechmatics, Rev AI), often with IP allowlist. Gladia documents no
auth at all. Only ElevenLabs signs (same `timestamp.body` HMAC shape as ours),
secret issued in dashboard at webhook creation, verification via SDK helper, no
manual recipe. No vendor found documenting signing before the secret is obtainable.

---

## Q4: `locked`-like status (withheld for billing)

| Vendor | Status list | Balance wording | Source |
| --- | --- | --- | --- |
| Gladia | `queued`, `processing`, `done`, `error` | No 402/balance wording. Limits framed as plan usage + 429 concurrency. | https://docs.gladia.io/api-reference/v2/pre-recorded/get, https://docs.gladia.io/chapters/limits-and-specifications/concurrency |
| AssemblyAI | `queued`, `processing`, `completed`, `error` | 400 "Insufficient Funds": "Your current account balance is negative. Please top up to continue using the API." Bulk guide: balance hitting zero mid-run "invalidates your results". | https://www.assemblyai.com/docs/pre-recorded-audio/guides/common_errors_and_solutions, https://www.assemblyai.com/docs/pre-recorded-audio/guides/bulk-transcription-and-load-tests-at-scale |
| Deepgram | n/a (sync / callback) | 402 `ASR_PAYMENT_REQUIRED`: "Project does not have enough credits for an ASR request and does not have an overage agreement." Rejects before work. | https://developers.deepgram.com/reference/errors |
| Speechmatics | `running`, `done`, `rejected`, `deleted`, `expired` | No insufficient-balance error. Billing: "you can keep using the API for as long as you have credits." | https://docs.speechmatics.com/administration/billing, https://docs.speechmatics.com/speech-to-text/batch/troubleshooting |
| Rev AI | `in_progress`, `transcribed`, `failed` | Balance = `failed` with `failure: insufficient_balance` or `invoicing_limit_exceeded`; "Check `failure_detail` for specific details and solutions." | https://docs.rev.ai/api/asynchronous/reference/ |
| ElevenLabs | No status field on transcript | 402 `payment_required`: "User has insufficient credits or payment is required."; `insufficient_credits`: "Your account does not have enough credits for this operation." | https://elevenlabs.io/docs/eleven-api/resources/errors |

**Pattern:** Confirms scan: none has a "ready but withheld" state. Balance shows
up either as a request rejection (402 Deepgram/ElevenLabs, 400 AssemblyAI) or as
a failure reason on the job (Rev AI). Wording is factual and action-oriented
("top up", "enough credits").

---

## Q5: `canceled` status

| Vendor | Canceled status? | Nearest equivalent | Source |
| --- | --- | --- | --- |
| Gladia | No (both spellings) | `DELETE /v2/pre-recorded/{id}`; 403 "not in a deletable state". | https://docs.gladia.io/api-reference/v2/pre-recorded/delete |
| AssemblyAI | No | `DELETE /v2/transcript/{id}` removes data, "mark it as deleted". In-progress delete behavior not stated. | https://www.assemblyai.com/docs/api-reference/transcripts/delete |
| Deepgram | No | HTTP 499 "client closed the connection". | https://developers.deepgram.com/reference/errors |
| Speechmatics | No (`deleted` instead) | `deleted`: "The job was deleted before it could finish." Client-triggered via DELETE with `force` "if job seems stuck, too long running, or the output is no longer needed." | https://docs.speechmatics.com/speech-to-text/batch/synchronous, https://docs.speechmatics.com/speech-to-text/batch/output |
| Rev AI | No | DELETE only after completion; in-progress returns 403 "Job is in invalid state to be deleted". | https://docs.rev.ai/api/asynchronous/reference/ |
| ElevenLabs | No | Async guide mentions "failed" only. | https://elevenlabs.io/docs/api-reference/speech-to-text/get |

**Pattern:** No vendor has a canceled status. Only Speechmatics has a terminal
"stopped early" state (`deleted`), and it documents who triggers it (client
DELETE with `force`) and why. Others either block deleting in-progress jobs
(Gladia, Rev AI) or leave it unstated.

---

## Q6: Upload response

| Vendor | Response | Guide treatment | Source |
| --- | --- | --- | --- |
| Gladia | 200 `{ audio_url, audio_metadata{ id, filename, extension, size, audio_duration, number_of_channels } }` | Full example shown; use `audio_url`, `audio_metadata` unexplained. | https://docs.gladia.io/api-reference/v2/upload/audio-file |
| AssemblyAI | 200 `{ upload_url }` | Shown; quickstart feeds it into `audio_url`. | https://www.assemblyai.com/docs/api-reference/files/upload, https://www.assemblyai.com/docs/getting-started/transcribe-an-audio-file |
| Deepgram | No upload endpoint | n/a | https://developers.deepgram.com/docs/pre-recorded-audio |
| Speechmatics | Job create 201; async body never shown ("`$JOB_ID` is from the submit command output"). `?wait=` shows `{ id, status, txt }`. | Implied, not shown. | https://docs.speechmatics.com/speech-to-text/batch/output, https://docs.speechmatics.com/speech-to-text/batch/synchronous |
| Rev AI | Job create 200 with job object (`id`, `status: in_progress`, ...) | Shown in Get Started; `id` used next. | https://docs.rev.ai/api/asynchronous/get-started/ |
| ElevenLabs | No upload endpoint; STT 202 with `webhook=true`, body not shown | `request_id` mentioned, not shown. | https://elevenlabs.io/docs/api-reference/speech-to-text/convert |

**Pattern:** Where an upload step exists, the response is shown with a status
code and the one field the next step needs. No vendor documents an empty upload
response or tells readers to ignore it. Speechmatics and ElevenLabs leave the
body implied, which is the only "not shown" precedent.
