# API docs: open questions

Branch `feat/api-spec-sync`. One heading per question; status emoji at the start
of the heading is the only status. ❓ open · ✅ answered and applied · 🙅 won't do.

Competitor evidence: `docs/research/20260914-competitor-docs-answers.md` (to be
written, see `docs/handoff/20260914-competitor-docs-research.md`).

---

### ✅ Q1: Keep the "two hosts" note on `/upload`?

**Where:** `upload.mdx`, `<Note>` under the intro.

> The main API is `https://www.api.vook.ai/api/v1`. The file upload goes to a
> separate upload host, returned as `upload_url` in step 1. Always use that
> returned value rather than hardcoding the host.

**Context:** leftover from when both hosts were hardcoded in the guide. Upload
host now comes from `upload_url`, and "The flow at a glance" table already shows
`POST {upload_url}`.

**Options:**

- A. Remove the note. Table + step 1 carry it.
- B. Remove the note, add one clause to the `upload_url` row in step 1 ("use it
  as returned"). Keeps the don't-hardcode warning where the value appears; the
  JSON example shows a real host a reader could copy.
- C. Keep as is.

**Answer:** B. Note removed; `upload_url` row says "Use it as returned."

---

### ✅ Q2: Base URL note on `/transcribe-url`

**Where:** `transcribe-url.mdx`, `<Note>` under the intro.

> The base URL is `https://www.api.vook.ai/api/v1`. To send a file from your
> machine instead, see Transcribe from a file.

**Context:** only one host is involved on this page, and it is the usual API
host. Stating it reads as if it were special. The same note pattern ("The base
URL is ...") sits on `retrieve-export.mdx` and `webhooks.mdx`; Overview already
has a "Base URL" section.

**Options:**

- A. Remove the note here. Move the file-page pointer into the intro sentence.
- B. Remove the base URL note from every guide; Overview is its single home.
- C. Keep as is.

**Answer:** B. Base URL lives in Overview and in every request example. Note
removed from quickstart, upload, transcribe-url, retrieve-export, webhooks.

---

### ❓ Q3: Webhook signature verification section

**Where:** `webhooks.mdx`. Headers documented; verification recipe not.

**Context (verified in `whisper-web` `feat/api-v1` code):** HMAC-SHA256 over
`${timestamp}.${rawBody}`, key = per-API-key `webhook_secret` used as its
64-char hex string. Backend returns `webhook_secret` once, in the API key
creation response. No `front` branch displays it, so customers cannot obtain it
today.

**Options:**

- A. Wait for `front` to show `webhook_secret` at key creation; then add
  "Verify the signature" with curl/Python. Handoff into `front`.
- B. Ship the recipe now, marked as available once the secret is shown.
- C. Drop signature docs; rely on polling as source of truth.

**Answer:**

---

### ❓ Q4: Wording for `locked` transcription status

**Where:** `retrieve-export.mdx`, status table.

> `locked`: The transcript is ready and unlocks once you top up your API
> credits. Reads return `402` until then.

**Context:** not defined in the spec. Meaning taken from backend enum comment
(transcript produced but withheld, balance exhausted when it settled). Fine to
publish? If yes, same wording belongs in the spec description (whisper-web).

**Answer:**

---

### ❓ Q5: Meaning of `canceled` transcription status

**Where:** `retrieve-export.mdx`, status table: "The transcription was
canceled."

**Context:** spec gives no meaning. Unknown: who or what cancels (user action,
credit gate, system)? Does the reader need to act?

**Answer:**

---

### ❓ Q6: Upload step 2 response (`201 {}`)

**Where:** `upload.mdx` step 2.

**Context:** kept from the previous guide. Step 2 hits the ingress host, not in
the spec, so not re-verified against the new API.

**Answer:**
