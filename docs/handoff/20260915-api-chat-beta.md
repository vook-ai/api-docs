# Handoff: chat over a transcription, beta

Written 2026-09-15 from a `whisper-web` session. Nothing is deployed yet. Backend source: `whisper-web` branch
`feat/api-chat-beta` (umbrella PR #1970 into `feat/api-v1`), contract commit `c925440be`.

Design, cited not restated (paths in `whisper-web`):

- `docs/tech/adr/api/0007-api-llm-chat-beta.md` §1 routes and bodies, §3 turn and response shape, §5 token cap, §8 beta
  label.
- `docs/tech/adr/api/0006-api-surface-conventions.md` §1 error body and code table, §5 what the beta tag exempts.

## Facts to document (exact names)

Routes (0007 §1), all Bearer API key:

- `POST /api/v1/transcriptions/{id}/chats`, body `title` (1 to 255 chars), `prompt`. Opens chat, answers first prompt.
- `POST /api/v1/transcriptions/{id}/chats/{chat_id}/messages`, body `prompt`.
- `GET /api/v1/transcriptions/{id}/chats`, returns `data: { id, transcription_id, title, created_at }[]`, unpaginated.
- `GET /api/v1/transcriptions/{id}/chats/{chat_id}`.

Chat body (create, message, read one), 0007 §3: `id`, `transcription_id`, `title`, `created_at`,
`messages: { role, content, created_at }[]` oldest first, `role` is `user` or `assistant`, `turn_in_progress`.

Error codes (`ApiError` values, wire casing):

| Code                       | Status | Reader's next step                                   |
| -------------------------- | ------ | ---------------------------------------------------- |
| `chat_not_enabled`         | `403`  | account not in beta; every chat route, reads too     |
| `chat_turn_in_progress`    | `409`  | another turn on this chat running; retry after it    |
| `chat_token_limit_reached` | `409`  | chat full; open a new chat                           |

Backend `message` strings (not stable, do not document as contract): `packages/backend/src/shared/types/api.ts`
`API_SURFACE_ERROR_MESSAGES`.

Cap: 2,000,000 tokens per chat (`CHAT_TOKEN_LIMIT`), all messages from any source. Checked before a turn; a turn started
under it completes, so a chat can end past it.

## Target design in api-docs

- **New guide page**, e.g. `chat.mdx`, in `docs.json` → `navigation.groups[0].pages` after `retrieve-export`. Beta label
  in title or a `<Warning>`/`<Info>` callout at top. Covers:
  - access: beta only, `403 chat_not_enabled` otherwise, on every route (0007 §8 requires it per route);
  - the four routes with curl + Python in `<CodeGroup>`, same shape as `retrieve-export.mdx`;
  - one response per turn, full JSON, no streaming;
  - chat belongs to the account: web-app chats appear in the list and can be continued; opening one may show an
    `assistant` message first;
  - disconnect: turn keeps running. Poll `GET` the chat until `turn_in_progress` is `false`; prompt and answer present
    means done, absent means failed, resend prompt;
  - context frozen at first turn: later edits to the transcript do not reach an existing chat, open a new chat;
  - one turn at a time per chat, `409 chat_turn_in_progress`;
  - 2M token cap, `409 chat_token_limit_reached`, open a new chat;
  - beta exemption (0006 §5): shape may change or be removed within `/v1` without notice; `snake_case` still holds.
- **`errors.mdx`** "Error codes" table: three rows above, sorted by status like existing rows. `chat_turn_in_progress`
  is a retryable `409`; "When to retry" names only `429` as retryable, so the chat page or table row says it.
- **`errors.mdx`** "Limits" table: row for tokens per chat.
- **`retention.mdx`**: a transcription's chats are deleted with it (0007 §9). Outside the listed sections, one line.
- **`api-reference/openapi.json`**: re-sync from `/api/v1/docs-json` once chat ships to prod; never edited by hand.
  Chat routes render under their beta `@ApiTags` tag. Wording fixes go to `whisper-web` decorators.
- Tone rules apply (`.claude/rules/001-tone-style.md`): no em dashes, no model or provider name. Response carries no
  model and no token usage; do not mention either.

## Open points for this session

- Beta tag string not fixed in ADR or plan. Read it from the controller on `feat/api-chat-surface` (Track B) or the
  re-synced spec before naming it in prose.
- Create + disconnect: client has no `chat_id` to poll. List has no `turn_in_progress`, and a failed first turn
  soft-deletes the chat. Safe doc advice: list chats, match on `title`, then poll that chat; missing after a while means
  failed. Confirm with the user before publishing.
- No recommended client timeout or poll interval in the ADR. Ask the user; do not invent numbers.
- No `prompt` length limit stated. Take it from Track B's DTO or omit.
- "Contact support to request access": ADR names no channel. Ask the user.
