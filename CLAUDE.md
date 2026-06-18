# api-docs

Public Vook API documentation site (`docs.vook.ai`), built with Mintlify.
Docs-only repo: hand-written guides + a committed snapshot of the prod OpenAPI spec.

## Package manager

**Use `pnpm`** for all package commands. Do not use `npm` or `yarn`.

## Preview

```bash
pnpm dlx mint dev      # local preview at http://localhost:3000
```

(Or install the CLI globally with `pnpm add -g mint`, then `mint dev`.)

## Key facts

- Content root is the repo root. Mintlify config is `docs.json`.
- API Reference is auto-generated from `api-reference/openapi.json` (manual
  snapshot, re-sync with `curl … /api/v1/docs-json` and re-add the `servers`
  block when the API changes).
- Reference covers the read endpoints plus the upload/transcribe write flow.
  The upload step 2 hits a separate ingress host and is hand-documented in
  `upload.mdx`; new endpoints render automatically once added to the public spec.
- Brand color: `#0883C6`. American English. No invented API facts.

## Writing style

Follow `.claude/rules/001-tone-style.md` for all docs copy:

- **No em dashes (`—`).** Zero tolerance. Search output for `—` before saving;
  rewrite the sentence if found.
- Never name an AI provider/model (Whisper, OpenAI, Google, Gemini). It's
  proprietary AI by the Vook team.
- Positive framing. No "more expensive", "charged upfront", etc.
- **No "no X, no Y" anaphora** (e.g. "No browser, no login flow."). This punchy
  negative-parallelism cadence reads as marketing copy. State it plainly instead
  ("You authenticate with an API key alone.").

Follow `.claude/rules/002-technical-depth.md` for how much technical detail to
include: document the observable contract (endpoints, fields, status, what to do
when a value is `null`), not internal mechanics ("computed lazily", queues,
infra). Litmus test: does the reader need it to make a correct request or handle
the response?
