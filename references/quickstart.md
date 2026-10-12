# Quickstart

> For the complete documentation index, see [llms.txt](/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Plugins extend and customize ChatGPT and Codex. They can add capabilities,
connect to external services, or both. A plugin can include skills that provide
instructions and resources, an MCP server that exposes tools, or both.

ChatGPT and Codex share one universal plugin directory. Public plugins are
published once and become discoverable from supported surfaces in both
products.

This tutorial creates a personal plugin by connecting an MCP server. By the
end, you will find the plugin in your personal Plugins directory and invoke its
tool from ChatGPT Work on the web. Custom UI is optional and is not part of
this quickstart.

This quickstart uses a public example MCP server at
  `https://tinymcp.dev/api/moldy-aloof-zettabyte/mcp`. It exposes a read-only
  `roll_dice` tool and does not require authentication.

## Connect your MCP server

First, connect your MCP server with [Add custom MCP server](https://developers.openai.com/api/docs/guides/custom-mcp-server):

1. Go to [ChatGPT Plugins](https://chatgpt.com/plugins).
2. Select the plus button, then **Add custom MCP server**.
3. Enter a name and use `https://tinymcp.dev/api/moldy-aloof-zettabyte/mcp` as the **Server URL**. Select **No authentication** for **Authentication**.
4. Review the risk warning and select **I understand and want to continue**.
5. Select **Create as a plugin**.

## Test the plugin

1. Go to [your personal plugins](https://chatgpt.com/plugins?view=personal).
   The plugin you created from the MCP server should appear there.
2. Open the plugin and select the plus button to install it.
3. Return to the [ChatGPT homepage](https://chatgpt.com).
4. At the top of the homepage, switch the tab from **Chat** to **Work**.
5. Start a new Work chat. In the prompt box, type `@` and select your plugin to
   invoke it directly.
6. Ask the plugin to roll one 20-sided die. Confirm that it calls `roll_dice`
   once with `sides` set to 20 and returns one value from 1 through 20.

Test several realistic inputs, including different die sizes, invalid values,
  and requests that should not call the tool. Refine the tool metadata when the
  wrong tool is selected or its arguments are inconsistent.

## Add more capabilities

Add more focused tools when the use-case inventory calls for them. To package
reusable instructions with the MCP server, continue with [Build
skills](https://developers.openai.com/plugins/build/skills) and [Package your
plugin](https://developers.openai.com/plugins/build/plugins). If a workflow benefits from visual
interaction, continue with [Add UI to your MCP
server](https://developers.openai.com/plugins/build/chatgpt-ui). UI remains optional.

## Publish the plugin

When the plugin is ready for other people, review the complete [plugin build
guide](https://developers.openai.com/plugins/build/plugins). To publish it publicly, use the [plugin
submission portal](https://developers.openai.com/plugins/deploy/submission).