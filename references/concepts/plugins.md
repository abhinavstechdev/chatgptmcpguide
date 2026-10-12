# Plugin architecture

> For the complete documentation index, see [llms.txt](/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Plugins are the packages people discover, install, share, and publish in
ChatGPT and Codex. A plugin can contain:

- **Skills** that give the model instructions and resources for repeatable
  workflows.
- **An MCP server** that exposes tools and connects to external systems.
- **Both skills and an MCP server** when the model needs workflow guidance and
  server-backed capabilities.
- **Lifecycle hooks** that run commands at configured points in the Codex
  runtime, including ChatGPT Work and Codex.

ChatGPT and Codex share one universal plugin directory. When you publish a
public plugin, people can discover the same listing from supported surfaces in
either product. Individual capabilities can still be surface-specific; for
example, hook scripts must be available in the execution environment.
Installing a plugin on the web doesn't deploy those scripts. See
[bundled hooks](https://developers.openai.com/plugins/build/plugins#bundled-mcp-servers-and-lifecycle-hooks)
for setup and trust requirements.

An MCP server can return structured data and model-readable text without
custom UI. When a task benefits from visual interaction, the server can also
return a UI resource.

```text
Plugin
├── Skills
└── MCP server (optional)
    ├── Tools and structured results
    └── UI resources (optional)
```

Start with the smallest shape that supports your use cases. You can add an MCP
  server or UI later without changing the plugin's purpose.

## Skills

A skill is a folder containing a `SKILL.md` file and, when needed, supporting
scripts, references, templates, or assets. Skills describe when to use a
workflow, which steps to follow, and what a successful result looks like.

Use skills when instructions and the tools already available to the model are
enough to complete the task. A plugin can package one skill or group related
skills into one installable experience.

For example, a meeting follow-up plugin might include separate skills for
drafting a recap, identifying action items, and preparing a customer email.

When writing skill instructions, follow the
[instruction-following guidance](https://developers.openai.com/plugins/build/skills#review-instruction-following).

## MCP servers

Build an MCP server when your plugin must connect to a service, expose a
controlled set of tools, authenticate users, or run behavior on infrastructure
you operate. The server defines:

- The tools the model can call.
- Input and output schemas for those tools.
- Authentication and authorization requirements.
- Structured results and model-readable content.
- Optional UI resources.

An MCP server gives you control over which capabilities you expose. It also
lets you update server behavior independently and observe requests made to
your infrastructure.

## Optional UI

Custom UI is not required for an MCP server. Use model responses or structured
results when they communicate the outcome.

Add UI when people need to inspect, compare, edit, confirm, or navigate
structured information. For example, a product comparison, editable schedule,
or map can benefit from a component, while a background status lookup often
does not.

ChatGPT supports the open [MCP Apps UI
standard](https://developers.openai.com/plugins/build/chatgpt-ui#start-with-mcp-apps). Start with the shared
standard, then add optional ChatGPT extensions only when the UI needs
capabilities the standard does not cover. Keep tools useful without the
component so the model can complete headless workflows and decide when UI adds
value.

## Choose a plugin shape

| Shape                 | Choose it when                                                            |
| --------------------- | ------------------------------------------------------------------------- |
| Skills only           | Instructions and existing tools are enough to complete the workflow.      |
| MCP server only       | The plugin needs MCP tools but does not need extra workflow instructions. |
| Skills and MCP server | Skills should guide the model through workflows that use your MCP tools.  |
| MCP server with UI    | Visual interaction materially improves part of an MCP-backed workflow.    |

After choosing a shape, [build the skills](https://developers.openai.com/plugins/build/skills) or
[build the MCP server](https://developers.openai.com/plugins/build/mcp-server). Add
[UI to the MCP server](https://developers.openai.com/plugins/build/chatgpt-ui) only when a use case
requires it, then [package the plugin](https://developers.openai.com/plugins/build/plugins).