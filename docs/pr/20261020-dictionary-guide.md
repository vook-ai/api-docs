# Dictionary guide

## Functional summary

New `dictionary.mdx` guide (sidebar "Dictionary", between Chat and MCP server):
add a vocabulary word, add or update a replacement rule, list either by
language, delete by `id`. API Reference gains the "Dictionary (API v1)" group
through the spec re-sync.

## Implementation details

- `api-reference/openapi.json`: re-synced from prod on 2026-10-20. Only change
  vs the previous snapshot: 6 dictionary endpoints + 7 schemas (checked by
  diffing with dictionary paths/schemas stripped).
- Prod spec now ships its own `servers` block (`addServer` in whisper-web's
  public Swagger builder). README and CLAUDE.md drop the manual re-add step.
- Guide examples `tumbler` → `Tumblr`, matching the backend `@ApiProperty`
  examples. `tumbler` is not in the backend stop-word list, so it does not hit
  `dictionary_entry_common_word`.
- `page_size` row: `1`–`100`, else `400 invalid_request`, same wording as
  `retrieve-export.mdx`. Prod validates instead of clamping (CTO ruling on the
  whisper-web PR audit, 2026-10-19).
- `errors.mdx`: adds `dictionary_entry_common_word`.
- Deletes `docs/handoff/20261019-dictionary-page-size.md` (untracked, its
  "Done when" met here).
- Every response shown in full with a field table, per rule 003.

## Testing

`python3 scripts/lint-docs.py` passes. Field set of each example checked
against the prod spec.

## Behaviour change

The API docs have a new Dictionary page explaining how to teach transcriptions custom words and replacement rules through the API. Wiki: `api-dictionary`
