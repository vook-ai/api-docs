# Full Responses in Guides

Every time a guide calls an endpoint that returns a JSON body, it shows the
**full response**, mirroring the API Reference page for that endpoint.

## Required for each JSON response

1. **Example JSON with every field** in the response schema, required and
   optional, nested objects included. Never trim to the fields the step uses.
2. **A field table** right after it: `Field | Type | Description`.
   - Type states nullability: `string or null`, `number or null`.
   - Description says when a value is `null` if the schema allows it.
   - Nested objects: document their fields (dotted names such as `folder.id`,
     or a sentence naming them).
3. Status or enum values the reader acts on get their own table (as for
   `status`), linked from the field row.

A response with no body (`204`, binary export) says so in one line.

The same schema returned twice **on one page** (for example a chat after open,
follow-up and read): the example JSON is still shown in full each time, and the
field table may be replaced by one line linking to the table earlier on that
page. Across pages, repeat the table.

## Source of truth

Take fields, types and nullability from `api-reference/openapi.json`, which the
API Reference renders. Do not add fields the spec lacks; do not drop fields it
has.

Descriptions follow the tone and depth rules (`001`, `002`), so they may be
worded differently from the spec. If the spec text leaks internals (for example
"prediction"), fix it in the backend decorators, not by hand in the spec.

## Keep in sync

Each spec re-sync: diff the response schemas against every guide example and
table, and update both. A new or removed field in the spec is a docs change.

## Pre-save check

- Every JSON response in the page has a complete example and a field table.
- Field set matches the schema exactly.
