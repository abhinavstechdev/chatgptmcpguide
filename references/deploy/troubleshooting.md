# Troubleshooting

> For the complete documentation index, see [llms.txt](/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

## How to triage issues

When something goes wrong—components failing to render, discovery missing prompts, auth loops—start by isolating which layer is responsible: server, component, or ChatGPT client. The checklist below covers the most common problems and how to resolve them.

Server, tool, and discovery checks apply to plugins in ChatGPT and Codex. UI,
widget state, and client-authentication checks on this page describe ChatGPT
behavior.

## Server-side issues

- **No tools listed:** Confirm your server is running and that you are connecting to the `/mcp` endpoint. If you changed ports, update the MCP server URL and restart MCP Inspector.
- **Structured content only, no component:** Confirm the tool descriptor sets `_meta.ui.resourceUri` to a registered HTML resource with `mimeType: "text/html;profile=mcp-app"` (ChatGPT honors `_meta["openai/outputTemplate"]` as an optional compatibility alias), and that the resource loads without CSP errors.
- **Schema mismatch errors:** Ensure your Python or TypeScript models match the schema advertised in `outputSchema`. Regenerate types after making changes.
- **Slow responses:** Components feel sluggish when tool calls take longer than a few hundred milliseconds. Profile server calls and cache results when possible.

## Widget issues

- **Widget fails to load:** Open the browser console (or MCP Inspector logs) for CSP violations or missing bundles. Make sure the HTML contains your compiled JavaScript and that the bundle contains all dependencies.
- **Drag-and-drop or editing doesn't persist:** If you rely on ChatGPT's widget-state persistence, call `window.openai.setWidgetState` after each update and restore state from `window.openai.widgetState` on mount.
- **Layout problems on mobile:** If you rely on ChatGPT layout signals, inspect `window.openai.displayMode` and `window.openai.maxHeight` to adjust layout. Avoid fixed heights or hover-only actions.

## Discovery and entry-point issues

- **Tool never triggers:** Revisit your metadata. Rewrite descriptions with “Use this when…” phrasing, update starter prompts, and retest using your golden prompt set.
- **Wrong tool selected:** Add clarifying details to similar tools or specify disallowed scenarios in the description. Consider splitting large tools into smaller, purpose-built ones.
- **Launcher ranking feels off:** Refresh your directory metadata and ensure the plugin icon and descriptions match what users expect.

## Authentication problems

- **401 errors:** Include a `WWW-Authenticate` header in the error response so ChatGPT knows to start the OAuth flow again. Double-check issuer URLs and audience claims.
- **Client registration fails:** If you use CIMD, confirm your authorization server metadata includes `client_id_metadata_document_supported: true` and can fetch ChatGPT's client metadata document. For `private_key_jwt`, confirm your authorization server can fetch ChatGPT's public JWKS and check the signed client assertion. If you use DCR, confirm your authorization server exposes `registration_endpoint` and that newly created clients have at least one login connection enabled.
- **An existing MCP server connection returns `invalid_client`:** Confirm that the dynamically registered OAuth client still exists and that your authorization server accepts its client secret, if it has one. ChatGPT reuses these credentials, so restore them instead of creating a new client. An expired access token requires a different fix.

## Deployment problems

- **ngrok tunnel times out:** Restart the tunnel and verify your local server is running before sharing the URL. For production, use a stable hosting provider with health checks.
- **Streaming breaks behind proxies:** Ensure your load balancer or CDN allows server-sent events or streaming HTTP responses without buffering.

## When to escalate

If you have validated the points above and the issue persists:

1. Collect logs (server, component console, ChatGPT tool call transcript) and screenshots.
2. Note the prompt you issued and any confirmation messages.
3. Share the details with your OpenAI partner contact so they can reproduce the issue internally.

A crisp troubleshooting log shortens turnaround time and keeps your MCP server reliable for users.