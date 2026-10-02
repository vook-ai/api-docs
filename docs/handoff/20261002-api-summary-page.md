# Handoff: summary of a transcription

Written 2026-10-02 from a `whisper-web` session. Not deployed. Backend source: `whisper-web` PR #2200
(`feat/api-summary-rate`, stacked on #2197). Publish only after #2200 reaches prod: the spec re-sync below reads prod.

Design, cited not restated (paths in `whisper-web`):

- `docs/tech/adr/api/0008-api-summary.md` §1 surface and response, §2 access, §3 a call, §4 charge, §5 continuing as
  chat, §8 retention.
- `docs/tech/adr/api/0006-api-surface-conventions.md` §1 error code table.
- `docs/pr/20261002-api-summary-route.md`: what shipped.

## Facts to document (exact names)

Routes, Bearer API key, **every key** (no beta, no `chat_not_enabled`). Swagger tag `Summaries (API v1)`, not beta:

- `POST /api/v1/transcriptions/{id}/summary`, no body. Synchronous: `200`, `status: completed`, summary in the
  response. Repeat call returns the same summary, not generated or charged again.
- `GET /api/v1/transcriptions/{id}/summary`.

Response, both routes: `transcription_id`, `status` (`processing` | `completed`), `summary` (Markdown, in the
transcript's language; `null` while `processing`), `created_at`. No model, no token usage, no chat id.

Behaviour:

- One summary per transcription. No regeneration, no prompt / length / style option.
- Transcription must be `completed`.
- Disconnect does not stop generation. Poll `GET` until `completed`; `404 summary_not_found` after `processing` means
  generation failed, send `POST` again.
- Typical generation time on web summaries (ADR 0008 §3): p50 ~12 s, p99 ~21 s, max ~68 s. Client timeout must allow
  for the tail.
- Price: included in the hourly rate (global `summary` rate 0). `402 insufficient_api_credits` only when the account's
  rate is above 0 and its credit balance is empty.
- Summary is a chat titled `Summary`: appears in `GET /api/v1/transcriptions/{id}/chats`, holding only the assistant
  answer. Accounts with chat access can continue it with follow-up prompts (billed as chat).
- Deleted with its transcription.

Error codes (wire casing), new rows for `errors.mdx`:

| Code                             | Status | Reader's next step                                                      |
| -------------------------------- | ------ | ----------------------------------------------------------------------- |
| `transcription_not_completed`    | `409`  | transcription still processing; poll the job, then retry               |
| `transcription_not_summarizable` | `409`  | transcription is empty or failed; nothing to summarize, do not retry    |
| `summary_in_progress`            | `409`  | `POST` while another call generates; poll `GET` until `completed`       |
| `summary_not_found`              | `404`  | `GET` with no summary, or generation failed; send `POST`                |

Backend copy for each route and field: `packages/backend/src/api/v1/summaries/api-v1-summary.controller.ts`,
`packages/backend/src/api/v1/dto/api-summary.dto.ts`.

## Target design in api-docs

- **New guide page** `summary.mdx`, in `docs.json` → `navigation.groups[0].pages` before `chat`. Not beta: no callout.
  Covers: one call, synchronous; curl + Python in `<CodeGroup>`, same shape as `retrieve-export.mdx`; full response
  JSON; one summary per transcription, repeat call free; disconnect and polling; the four codes; continuing it as a
  chat (link `/chat`).
- **`errors.mdx`** "Error codes" table: four rows above, sorted by status like existing rows. `summary_in_progress` is a
  retryable `409` (via `GET`), as `chat_turn_in_progress` is.
- **`chat.mdx`**: one line, the chat list can hold a `Summary` chat created by the summary route.
- **`retention.mdx`**: summary row or one line; it is a chat, deleted with its transcription.
- **`api-reference/openapi.json`**: re-sync from prod `/api/v1/docs-json` once #2200 deploys; never edited by hand.
  Wording fixes go to `whisper-web` decorators.
- Tone rules (`.claude/rules/001-tone-style.md`): no em dashes, no model or provider name, no output token cap (cost
  bound, not a contract).

## Open points for this session

- Pricing wording: "included in the hourly rate" is the public default. Contract accounts can carry a summary price;
  ask the user whether the page mentions that at all.
- Recommended client timeout / poll interval: none in the ADR. Ask the user; do not invent numbers.
