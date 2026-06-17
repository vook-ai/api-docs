# Vook API docs

Source for the public Vook API documentation site at
[`docs.vook.ai`](https://docs.vook.ai), built with [Mintlify](https://mintlify.com).

This is a docs-only repo. It holds the hand-written guides plus a committed
snapshot of the production OpenAPI spec. The backend source stays private.

## Structure

```
docs.json                 # Mintlify config: theme, nav, logo, OpenAPI wiring
introduction.mdx          # what the API is, base URL, beta + billing notes
quickstart.mdx            # read flow: list, status, transcript, export
authentication.mdx        # minting and using vk_live_ keys
api-reference/
  openapi.json            # snapshot of the prod spec (auto-rendered reference)
logo/
  light.svg               # blue mark + black wordmark (light backgrounds)
  dark.svg                # blue mark + white wordmark (dark backgrounds)
favicon.ico
```

The **API Reference** group is generated automatically from
`api-reference/openapi.json`. It currently covers the read endpoints; the write
endpoints will appear once they are added to the public spec.

## Preview locally

Run the Mintlify dev server from the repo root with pnpm:

```bash
pnpm dlx mint dev
```

Then open the local URL it prints (default `http://localhost:3000`).

## Updating the OpenAPI spec

The spec is a manual snapshot. Re-sync it when the API changes:

```bash
curl -s https://www.api.vook.ai/api/v1/docs-json -o api-reference/openapi.json
```

Then re-add the `servers` block so the playground has a callable base URL:

```json
"servers": [{ "url": "https://www.api.vook.ai", "description": "Production" }]
```
