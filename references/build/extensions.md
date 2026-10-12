# Plugin Extensions

> For the complete documentation index, see [llms.txt](/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

OpenAI MCP Extensions enables developers to hook their plugins into key surfaces
of the ChatGPT user experience, including the sidebar, composer, and file viewers.

Plugin extensions on the web are coming soon to ChatGPT Free and Go users.
  Existing plugin functionality is unaffected. Composer mentions are available
  only in the ChatGPT desktop app.

<img src="https://developers.openai.com/images/apps-sdk/extensions/chatgpt-plugin-surfaces.webp"
  alt="Illustration of plugin extensions across the ChatGPT sidebar, settings, composer, conversation, and side panel."
  width="1600"
  height="769"
  class="my-6 h-auto w-full rounded-xl"
/>

## Try it out

Get a feel for extensions with [Bits & Bolts](https://github.com/openai/mcp-extensions/tree/main/plugins/bits-and-bolts), our kitchen sink plugin. We'll keep it up to date as new extensions roll out.



  [Install Bits & Bolts Remote



        <img src="https://developers.openai.com/images/apps-sdk/extensions/bits-and-bolts-remote.svg"
          alt=""
          width={32}
          height={32}
        />
      

      Try the examples in ChatGPT.](https://chatgpt.com/plugins/plugin_asdk_app_6abadab6e7d881919e7491d52c7846e8)



## Start building

Use the GitHub repository for installation, SDK examples, and the full
specification.



  [TypeScript SDK



        Add extensions to your MCP server and app UI.](https://github.com/openai/mcp-extensions/blob/main/typescript/README.md)
  [Python SDK



        Add server-side extensions with the MCP Python SDK.](https://github.com/openai/mcp-extensions/blob/main/python/README.md)
  [Protocol specification



        Defines the formal, language-agnostic API that extends the MCP and MCP
      Apps specifications.](https://github.com/openai/mcp-extensions/blob/main/docs/spec.md)



Once your server is ready, [connect and test your
plugin](https://developers.openai.com/plugins/deploy/connect-chatgpt), then [package it for
distribution](https://developers.openai.com/plugins/build/plugins).

## Extension reference

Extensions give users new ways to interact with your plugin across ChatGPT.
Declaring support for an extension takes just a few lines of SDK code.

|                                                            | Extension                                                                                                                   | What users can do                                                                                            |
| ---------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| | [Sidebar apps](https://github.com/openai/mcp-extensions/blob/main/docs/spec.md#global-entrypoint)                           | Give users a place to open your app from the sidebar and work in it fullscreen.                              |
| | [Conversation panels](https://github.com/openai/mcp-extensions/blob/main/docs/spec.md#thread-entrypoint)                    | Let users open your app beside a conversation, keeping their work and chat together.                         |
| | [Plugin settings](https://github.com/openai/mcp-extensions/blob/main/docs/spec.md#structured-settings)                      | Let users configure your plugin's product-specific settings from within ChatGPT.                             |
| | [File viewers and editors](https://github.com/openai/mcp-extensions/blob/main/docs/spec.md#file-extension-entrypoint)       | Open supported files in your own interface, with reading, live updates, and saving changes handled together. |
| | [Display modes](https://github.com/openai/mcp-extensions/blob/main/docs/spec.md#display-modes)                              | Choose where and how your app appears in ChatGPT conversations.                                              |
| | [Deep links](https://github.com/openai/mcp-extensions/blob/main/docs/spec.md#deep-links)                                    | Take users directly to a specific page or item within your sidebar app.                                      |
| | [Extended model context](https://github.com/openai/mcp-extensions/blob/main/docs/spec.md#uiupdate-model-context-extensions) | Control annotations and how attached context appears in the composer.                                        |
| | [Extended message sending](https://github.com/openai/mcp-extensions/blob/main/docs/spec.md#prompt-target-and-send-behavior) | Send messages to the current conversation, or a new one on desktop and Work on the web.                      |
| | [Composer mentions](https://github.com/openai/mcp-extensions/blob/main/docs/spec.md#composer-at-mentions)                   | Let users find and select content from your plugin in the ChatGPT desktop composer.                          |
| | [Extended forms](https://github.com/openai/mcp-extensions/blob/main/docs/spec.md#openai-form-elicitation)                   | Ask users for structured input or let them choose from images, then return their response to your tool.      |
| | [Plugin onboarding](https://developers.openai.com/plugins/build/plugins#add-an-onboarding-skill)                                                         | Guide users through setup in a new or existing conversation.                                                 |

### Sidebar apps

Add an entry to the global sidebar that launches your MCP App fullscreen.



[Opening the Bits & Bolts CAD parts library from the sidebar](https://developers.openai.com/videos/plugins/extensions/sidebar-entrypoint.mp4)



Pass this metadata as `_meta` when registering your MCP App tool. Replace
`ui://parts/library` with your registered UI resource URI:

```ts


const toolMetadata = {
  ui: { resourceUri: "ui://parts/library" },
  "openai/ui": {
    entrypoints: [{ type: "global" }],
  } satisfies OpenAIUiToolMetadata,
};
```

Use `{ type: "thread" }` to add an entrypoint in a conversation's side panel.
See the [entrypoint guide](https://github.com/openai/mcp-extensions/blob/main/typescript/README.md#ui-entrypoints)
for full registration examples.

### File viewers and editors

Open your MCP App in the thread side panel when a user opens a file with a
supported extension.



[Opening a CAD file in the Bits & Bolts file viewer](https://developers.openai.com/videos/plugins/extensions/file-viewer.mp4)



Use a file entrypoint in your tool's `_meta`, with the extensions your viewer
supports:

```ts


const toolMetadata = {
  ui: { resourceUri: "ui://parts/viewer" },
  "openai/ui": {
    entrypoints: [{ type: "file", extensions: ["stl"] }],
  } satisfies OpenAIUiToolMetadata,
};
```

Replace `ui://parts/viewer` with your registered UI resource. The app receives a
resource URI for the opened file. Follow the [file handler
guide](https://github.com/openai/mcp-extensions/blob/main/typescript/README.md#file-extension-handlers)
to receive that input and read the resource with the app SDK.

### Extended forms

Extend standard MCP forms with richer components native to ChatGPT.



[Selecting images in a Bits & Bolts form](https://developers.openai.com/videos/plugins/extensions/image-picker.mp4)



```ts


function partSelectionSchema(parts: OpenAIFormOption[]): OpenAIForm {
  return {
    type: "object",
    properties: {
      part: {
        type: "string",
        title: "Part",
        oneOf: parts,
      },
    },
    required: ["part"],
  };
}
```

Pass this schema as `requestedSchema` in your form request. Each option uses
`const` and `title`, with an optional `x-openai-thumbnail` icon.
OpenAI-registered MCP servers require
[multi-round-trip requests (MRTR)](https://modelcontextprotocol.io/specification/2026-07-28/basic/patterns/mrtr).

<a id="plugin-examples"></a>

## Extensions in the wild

See how plugins you already know are building with extensions.



  <article className="overflow-hidden rounded-xl border border-default bg-surface">
    

      

        <img src="https://developers.openai.com/images/codex/icons/chatgpt-plugin-canva.svg"
          alt=""
          width={32}
          height={32}
          className="size-8 shrink-0 object-contain"
        />
        <h3 className="heading-md text-primary">Canva</h3>
      

      

        **Sidebar Tabs** enable Canva users to create designs and preview them
        as a native sidebar feature of ChatGPT.
      

      [
View plugin
](https://chatgpt.com/plugins/plugin_connector_68df33b1a2d081918778431a9cfca8ba)
    

  </article>
  <article className="overflow-hidden rounded-xl border border-default bg-surface">
    

      

        <img src="https://developers.openai.com/images/codex/work-plugins/figma.png"
          alt=""
          width={32}
          height={32}
          className="size-8 shrink-0 object-contain"
        />
        <h3 className="heading-md text-primary">Figma</h3>
      

      

        **Composer Mentions** enable Figma users to search for and mention files
        directly in the ChatGPT desktop app.
      

      [
View plugin
](https://chatgpt.com/plugins/plugin_connector_68df038e0ba48191908c8434991bbac2)
    

  </article>
  <article className="overflow-hidden rounded-xl border border-default bg-surface">
    

      

        <img src="https://developers.openai.com/images/apps-sdk/extensions/adobe-icon.webp"
          alt=""
          width={32}
          height={32}
          className="size-8 shrink-0 object-contain"
        />
        <h3 className="heading-md text-primary">Adobe</h3>
      

      

        **File Extension Handlers** enable Adobe users to edit files with
        Acrobat and Photoshop directly in ChatGPT.
      

      [
View plugin
](https://chatgpt.com/plugins/plugin_asdk_app_69312da8e4dc81919370cb86fd172b6c)
    

  </article>