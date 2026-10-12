# Connect and test your plugin

> For the complete documentation index, see [llms.txt](/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Test each capability before testing the complete installed plugin. If the
plugin includes an MCP server, start by connecting and evaluating the server in
ChatGPT. Then package the plugin with its skills and test the complete
experience. Skills-only plugins can skip the first section.

Keep your evaluation prompts and results throughout development so you can
compare behavior across releases.

## Test an MCP server (optional)

### Prepare the endpoint

Confirm that:

- The MCP server is reachable through a public HTTPS endpoint or
  [Secure MCP Tunnel](https://developers.openai.com/api/docs/guides/secure-mcp-tunnels).
- A public endpoint supports streamable HTTP, typically at `/mcp`, or the
  tunnel can reach its configured stdio or HTTP MCP server.
- Tool names, descriptions, schemas, and annotations are present.
- Authentication discovery works for tools that require an account.

Use Secure MCP Tunnel to connect a private MCP server in ChatGPT without
exposing the server to the public internet. A development tunnel or another
HTTPS forwarding service can also provide an endpoint for local testing. These
testing options do not replace the public HTTPS endpoint required for
[plugin submission](https://developers.openai.com/plugins/build/mcp-server#deploy-the-endpoint).

### Inspect the MCP server

Use [MCP Inspector](https://modelcontextprotocol.io/docs/tools/inspector) to
list and call tools directly:

```bash
npx @modelcontextprotocol/inspector@latest
```

Exercise each tool with representative inputs, edge cases, missing identifiers,
and empty results. Verify schema validation, authentication errors, annotations,
confirmation behavior, and the model-readable result.

### Add the MCP server

Account and workspace policies apply to adding and using custom MCP servers.

1. Go to [ChatGPT Plugins](https://chatgpt.com/plugins).
2. Select the plus button, then **Add custom MCP server**.
3. Enter a user-facing name and description.
4. Under **Connection**, choose the connection method:
   - For a public endpoint, enter the MCP server URL, including the `/mcp` path.
   - For Secure MCP Tunnel, select **Tunnel**, then choose an available tunnel
     or enter its `tunnel_id`.
5. Configure authentication, review the risk warning, and select **I understand and want to continue**.
6. Select **Create as a plugin**.
7. Review the tools and metadata discovered from the server.

If ChatGPT cannot connect, verify the public HTTPS endpoint with MCP Inspector,
or check the tunnel's workspace association and `tunnel-client` status. Resolve
transport, initialization, schema, or authentication errors before continuing.

### Check tool selection

Install the resulting plugin, then start a new conversation. Type `@` in the
prompt box and select the plugin. Create
an evaluation set that includes:

- Direct requests that should call a specific tool.
- Indirect requests that express the same goal.
- Follow-up requests that reuse identifiers from earlier results.
- Write actions that require authorization or confirmation.
- Unsupported requests that shouldn't call a tool.

For each request, record the selected tool, arguments, result, errors, and
confirmation behavior. Rerun the set whenever you change tool names,
descriptions, schemas, or annotations.

If the server returns optional UI, test both the component and the
model-readable result.

### Test through the API Playground

For raw request and response logs, open the
[API Playground](https://platform.openai.com/playground):

1. Choose **Tools → Add → MCP Server**.
2. Enter the HTTPS endpoint and connect.
3. Run test prompts and inspect the request and response data.

### Refresh metadata

After changing tool names, descriptions, schemas, annotations, authentication,
or UI resources:

1. Deploy or restart the MCP server.
2. Open the connection at [ChatGPT Plugins](https://chatgpt.com/plugins).
3. Select **Refresh**.
4. Confirm that the advertised metadata changed.
5. Start a new conversation and rerun the affected tests.

This refresh flow applies to custom MCP servers connected directly in ChatGPT.
Published plugins use
[continuous review](https://developers.openai.com/plugins/deploy/app-review#continuous-review-and-tool-updates)
for tool updates. Changes to submitted plugin information or imported skills
still require a new version, review, and publication.

Before packaging the plugin, confirm that:

- The tool list matches the documented capabilities.
- Structured results match each tool's declared output schema.
- Authentication failures return useful errors.
- Positive prompts select the expected tools and negative prompts don't.
- Optional UI renders without console errors and restores state correctly.

## Test the complete plugin

After the MCP server works—or immediately for a skills-only plugin—package and
install the complete plugin from a local source:

1. [Package the plugin](https://developers.openai.com/plugins/build/plugins) with its skills, manifest, and
   MCP server connection when applicable.
2. Add the plugin to a local marketplace and install it from the Plugins
   Directory.
3. Start a new conversation with the plugin enabled.
4. Run representative requests from the plugin's use-case inventory.

Create an evaluation set that includes:

- Direct requests that should use a skill.
- Indirect requests that express the same goal.
- Follow-up requests that depend on an earlier result.
- Negative requests that shouldn't use the plugin.
- Boundary cases that the plugin intentionally doesn't support.

For each request, check that the plugin follows the skill instructions, uses
the expected resources, completes every required step, and produces a useful
result. Record any missing steps, unnecessary activations, or inconsistent
results.

For plugins with an MCP server, also confirm that skills invoke the right tools,
tool results return to the workflow, authentication works after installation,
and users can complete each combined workflow from start to finish.

Before submission, confirm that:

- Each skill activates for the intended requests.
- Similar phrasing produces consistent behavior.
- Unsupported requests don't activate the plugin.
- Bundled files and references resolve after installation.
- The plugin's starter prompts represent workflows it can complete.
- For plugins with an MCP server, bundled skills and tools work together as
  intended.