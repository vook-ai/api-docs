# Upload step: show progress instead of apparent hang

Written 2026-09-16 from a `whisper-web` session. Docs-only change to `upload.mdx` step 2. Nothing edited yet.

## Problem

Following `upload.mdx` step 2 (`curl -X POST "$UPLOAD_URL" … -F "chunk=@…"`) on a large file prints nothing until the
upload ends. Looks hung; it succeeds. Reported by CTO on an `.aac` file.

## Current state (verified in `whisper-web`, 2026-09-16)

- Ingress `POST /upload`: `packages/processor/src/ingress.controller.ts`. Multer writes whole `chunk` field to disk
  **before** handler runs; handler replies `{}` immediately after. Wait = client-to-ingress transfer time only.
- Server emits nothing mid-request. Progress can only come from the client (bytes sent / file size).
- Max single upload: 6 GB (`MAX_SINGLE_UPLOAD_BYTES`, same file).
- curl hides its progress meter when the response body goes to the terminal. Redirecting output (`-o`) restores it.
  Documented curl behavior; the exact command below **not run** from this session.
- `upload-response.json` untracked at repo root: likely CTO's own `-o` test. Not committed; ask before deleting.

## Next action

Edit `upload.mdx` step 2 (lines ~79-108):

1. curl tab: add `--progress-bar -o upload-response.json` (or `-o /dev/null`, response is `{}`):
   ```bash
   curl -X POST "$UPLOAD_URL" \
     -H "Authorization: Bearer $UPLOAD_TOKEN" \
     -F "chunk=@meeting.mp3" \
     --progress-bar -o upload-response.json
   ```
2. One sentence after CodeGroup: large files take a while; request returns once the whole file is sent; show progress
   client-side.
3. Python tab: decide (see Open decisions).
4. Separate stages in copy: step 2 progress = upload bytes; transcription progress = step 4 polling / webhook.
5. Run `pnpm dlx mint dev`, check page renders.

## Open decisions

- **Python progress example.** `requests` has no upload callback. Options: `requests-toolbelt`
  `MultipartEncoderMonitor` (extra dependency in a guide), or a sentence only. Guide currently depends on `requests`
  alone — lean sentence-only unless CTO wants the snippet.
- **JS/browser mention.** No JS tab exists. `XMLHttpRequest.upload.onprogress` / axios `onUploadProgress` work; `fetch`
  does not report upload progress. Add only if a JS tab is added.

## Traps

- Style rules: `.claude/rules/001-tone-style.md`. No em dashes, no "no X, no Y". Grep for `—` before saving.
- `.claude/rules/002-technical-depth.md`: do not mention multer, disk, S3, background copy. Contract only.
- Line 108 "A `2xx` status means the file is stored" is looser than reality: ingress replies after receiving the file,
  the S3 copy runs in background and a failure there is only logged (`ingress.controller.ts` ~L159-183). Do not
  describe internals in docs; if wording changes, flag to CTO rather than inventing a failure contract.
- `.claude/rules/003-full-responses.md` wants full responses. Step 2 response body is `{}` and currently undocumented;
  adding it is in scope if touching the section.
- Do not touch `api-reference/openapi.json` (generated). Ingress route is hand-documented only here.

## Start here

```
Read docs/handoff/20260916-upload-progress-bar.md.
Start with: update upload.mdx step 2 curl snippet to show a progress bar, add one line on client-side progress.
```
