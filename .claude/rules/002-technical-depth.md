# Technical Depth

How much technical detail to put in customer-facing docs and replies. The default
is **the consumer's view, not the implementation's**. Document the contract a
reader needs to send a correct request and handle the response. Leave out how it
works under the hood.

## The litmus test

Before writing any technical sentence, ask:

> Does the reader need this to make a correct request or handle the response?

If **no**, cut it. Internal mechanics are interesting to us, not actionable for
them.

## Document this (observable contract)

- Endpoints, methods, paths, and required vs optional parameters.
- Request and response shapes: field names, types, and `null` conditions a
  client can actually observe.
- Status and lifecycle values the API returns (e.g. `queued`, `completed`,
  `empty`, `failed`), and what each means for the reader's next action.
- Auth, headers, formats, limits, and error codes.
- What to do when a value is not ready yet (poll, re-request, check for `null`).

## Leave this out (internal mechanics)

- **How** a value is produced: "computed lazily", "cached", "queued on a worker",
  "processed in chunks", "denormalized from…".
- Internal service names, infrastructure, databases, queues, file layouts.
- Implementation reasons for behavior. State the behavior, not the cause.
- Anything that names or hints at a third-party provider (see Technology
  Disclosure in `CLAUDE.md`).

## Rewrite pattern

Describe the **effect** the client sees, not the **cause** inside the system.

| Too deep (internal) | Right level (observable) |
| --- | --- |
| "The transcript is computed lazily, so `plain_text` is `null` until ready." | "If the transcript is not ready yet, `plain_text` comes back `null`." |
| "Status is decoupled from internal processing states." | "Status reflects where your transcription is in its lifecycle." |
| "Files are split into chunks on the processor before transcription." | "Large files may take longer to process." |

## When deeper detail is justified

Only when the reader must act on it: a required polling loop, an idempotency
caveat, a rate limit, or a sequence that fails without a specific order. Even
then, describe the behavior to handle, not the internals that cause it.
