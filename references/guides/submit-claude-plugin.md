# Submit your Claude Code plugin to OpenAI

> For the complete documentation index, see [llms.txt](/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

If you already publish a Claude Code plugin or connector, choose the submission
path based on whether it includes skills, an MCP server, or both.

| What you have               | What to submit                                                                                                     |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| Skills and no MCP server    | Upload a [skills-only plugin](#submit-a-skills-only-plugin).                                                       |
| A public HTTPS MCP endpoint | Create a [remote MCP submission](#submit-a-plugin-with-a-remote-mcp-server). Include any skills in the same draft. |
| A local MCP server          | Deploy it to a public HTTPS URL. If you can't, reach out to your OpenAI contact for local MCP support.             |

Claude uses separate submission processes for Claude Code plugins and MCP
connectors. OpenAI uses one plugin package that can contain skills, MCP servers,
or both. Claude marketplace listings and approvals don't transfer.

If your plugin includes skills, review their instructions using the
[instruction-following guidance](https://developers.openai.com/plugins/build/skills#review-instruction-following)
before submitting them through either path.

## Submit a skills-only plugin

Choose this path when the plugin doesn't need an MCP server.

### Review what OpenAI supports

| What your Claude plugin has                                                                                 | What to do                                                                                                                                                                                                                                                                                                                                                                 |
| ----------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `skills`                                                                                                    | Keep each skill with its `SKILL.md`, scripts, references, and assets. A direct Claude archive upload must include at least one skill at `skills/<skill-name>/SKILL.md`.                                                                                                                                                                                                    |
| Manifest-declared custom skill directories                                                                  | Keep the directories and their manifest declarations in the archive.                                                                                                                                                                                                                                                                                                       |
| Skills that explicitly refer to Claude                                                                      | Replace Claude-specific references in the skill instructions with provider-neutral language, such as “the model.” Keep a product name only when the instruction genuinely applies to that product.                                                                                                                                                                         |
| `commands`, `commands/`, `agents`, or `agents/`                                                             | Convert reusable behavior to skills. Turn each Markdown command into a skill, move reusable agent procedures into skills, and merge useful persona instructions into the relevant skill.                                                                                                                                                                                   |
| `hooks` or `hooks/hooks.json`                                                                               | Remove lifecycle hooks before public directory submission. If the plugin depends on lifecycle hooks, distribute it so users can install it manually in Codex desktop. See [lifecycle hooks](https://developers.openai.com/plugins/build/plugins#bundled-mcp-servers-and-lifecycle-hooks).                                                                                                               |
| `userConfig` or `${user_config.*}`                                                                          | OpenAI doesn't run Claude installation prompts or expand `user_config` variables. Follow [Replace Claude `userConfig`](#replace-claude-userconfig). If the plugin needs credentials or persistent user settings, use an MCP server.                                                                                                                                        |
| Skills that create or update Claude live artifacts                                                          | OpenAI doesn't currently support Claude live artifacts. Remove instructions that require creating, reopening, refreshing, or updating an artifact. Return the underlying content as regular conversation output instead; for example, render artifact tables as standard tables. Artifact-specific HTML, persistence, refresh behavior, and interactions aren't preserved. |
| `bin/`, `settings`, `settings.json`, `CLAUDE.md`, or `.claude/settings*.json`                               | Keep required helpers and instructions in the plugin. Call bundled executables with package-relative paths, and remove Claude-only settings.                                                                                                                                                                                                                               |
| `outputStyles`, `lspServers`, `experimental.themes`, `experimental.monitors`, `channels`, or `dependencies` | Move essential behavior into skills, then remove the Claude declaration. Contact your OpenAI partner if the core workflow requires inbound channel messages.                                                                                                                                                                                                               |
| `.claude-plugin/plugin.json`                                                                                | Keep the manifest for a direct Claude archive upload. The portal converts it to `.codex-plugin/plugin.json`.                                                                                                                                                                                                                                                               |
| `.claude-plugin/marketplace.json`, `.mcp.json`, `mcpServers`, `.app.json`, or `apps`                        | Don't rely on these files or declarations. A skills-only upload excludes MCP server configuration, and you can't submit an existing MCP server integration by reference.                                                                                                                                                                                                   |

### Prepare and upload the archive

1. Confirm that the archive root, or its single top-level directory, includes
   `.claude-plugin/plugin.json` with a nonempty `description` and at least one
   valid skill at `skills/<skill-name>/SKILL.md`.
2. Open the [plugin submission portal](https://platform.openai.com/plugins),
   select **Create plugin**, choose **Skills only**, and upload the archive.
3. Review the generated `.codex-plugin/plugin.json`. The portal adds missing
   interface defaults and normalizes text fields during conversion.
4. Test the imported skills in a clean environment. Confirm that each skill can
   find its referenced files and executables and doesn't depend on undeclared
   local packages, files, or credentials.
5. Complete the listing and review fields, fix every scan result, and submit the
   draft.

If the archive doesn't qualify for direct upload, use
[Package your plugin](https://developers.openai.com/plugins/build/plugins#plugin-structure) to create the
OpenAI manifest and package layout. See [Build skills](https://developers.openai.com/plugins/build/skills)
for skill requirements.

<a id="submit-a-plugin-with-an-mcp-server"></a>

## Submit a plugin with a remote MCP server

Choose this path when the server has a stable, public HTTPS URL that OpenAI can
reach. The server can have been local in the Claude plugin; what matters for
this submission is that you have deployed it as a remote service.

### Review what OpenAI supports

| What your Claude integration has                                                                            | What to do                                                                                                                                                                                                                                                                                                                                                                 |
| ----------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| A remote MCP server                                                                                         | Reuse the server implementation. Submit a stable, public HTTPS endpoint that uses Streamable HTTP.                                                                                                                                                                                                                                                                         |
| A local MCP server or Claude Desktop extension (`.mcpb`)                                                    | Deploy the MCP server to a public HTTPS URL. If you can't, reach out to your OpenAI contact for local MCP support. The portal doesn't accept `.mcpb` files.                                                                                                                                                                                                                |
| Skills or manifest-declared custom skill directories                                                        | Include the skills in the same **With MCP** submission. Keep each `SKILL.md` with its scripts, references, and assets.                                                                                                                                                                                                                                                     |
| Skills that explicitly refer to Claude                                                                      | Replace Claude-specific references in the skill instructions with provider-neutral language, such as “the model.” Keep a product name only when the instruction genuinely applies to that product.                                                                                                                                                                         |
| `commands`, `commands/`, `agents`, or `agents/`                                                             | Convert reusable behavior to skills. Turn each Markdown command into a skill, move reusable agent procedures into skills, and merge useful persona instructions into the relevant skill.                                                                                                                                                                                   |
| `hooks` or `hooks/hooks.json`                                                                               | Remove lifecycle hooks before public directory submission. If the plugin depends on lifecycle hooks, distribute it so users can install it manually in Codex desktop. See [lifecycle hooks](https://developers.openai.com/plugins/build/plugins#bundled-mcp-servers-and-lifecycle-hooks).                                                                                                               |
| `userConfig` or `${user_config.*}`                                                                          | OpenAI doesn't run Claude installation prompts or expand `user_config` variables. Follow [Replace Claude `userConfig`](#replace-claude-userconfig) to move each value to an explicit input, OAuth, hosted storage, or Codex-local configuration.                                                                                                                           |
| Skills that create or update Claude live artifacts                                                          | OpenAI doesn't currently support Claude live artifacts. Remove instructions that require creating, reopening, refreshing, or updating an artifact. Return the underlying content as regular conversation output instead; for example, render artifact tables as standard tables. Artifact-specific HTML, persistence, refresh behavior, and interactions aren't preserved. |
| `.app.json`, `apps`, or an existing MCP server integration                                                  | Submit the MCP server endpoint directly. You can't submit an existing MCP server integration by reference.                                                                                                                                                                                                                                                                 |
| `outputStyles`, `lspServers`, `experimental.themes`, `experimental.monitors`, `channels`, or `dependencies` | Move essential behavior into skills or MCP tools, then remove the Claude declaration. Contact your OpenAI partner if the core workflow requires inbound channel messages.                                                                                                                                                                                                  |

### Prepare and submit the MCP server

1. Deploy the MCP server at its production HTTPS endpoint using Streamable
   HTTP. Use OAuth 2.1 when the server accesses private user data or takes
   actions for a user. Follow [Authenticate users](https://developers.openai.com/plugins/build/auth) for the
   supported product requirements and MCP authorization specification.
2. Add accurate tool schemas and safety annotations. Test that every tool
   connects, authenticates, returns the expected result shape, and requires the
   intended confirmation for write or destructive actions.
3. Convert any commands or agents to skills and make sure the skills don't
   depend on undeclared local packages, files, or credentials.
4. Open the [plugin submission portal](https://platform.openai.com/plugins),
   select **Create plugin**, choose **With MCP**, and submit the production
   endpoint. Add the converted skills to the same draft when applicable.
5. Verify the server domain, configure authentication when the server requires
   sign-in, complete the listing and review fields, fix every scan result, and
   submit the draft.

Plan for these two setup steps before you submit:

- **Domain verification:** You must be able to serve the portal's exact token
  from `/.well-known/openai-apps-challenge` on the MCP host or an allowed parent
  host. Complete the challenge when the portal prompts you. See
  [Configure the MCP submission](https://developers.openai.com/plugins/deploy/submission#mcp).
- **OAuth and workspace domain restrictions:** If the plugin uses OAuth, expose
  a UserInfo Endpoint that returns the user's `email` claim and
  `email_verified: true`. Advertise and enable the `openid` and `email` scopes.
  See
  [Support workspace domain restrictions](https://developers.openai.com/plugins/build/auth#support-workspace-domain-restrictions).

Review the [remote MCP server review requirements](https://developers.openai.com/plugins/deploy/app-review)
before submitting.

## Replace Claude `userConfig`

OpenAI plugins don't run Claude `userConfig` installation prompts or expand
`${user_config.*}` references. Remove those references and replace each value
based on how the plugin uses it.

| What the value controls                      | OpenAI replacement                                                                                                                                                                            |
| -------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| A choice that can change for each task       | Add an explicit skill or MCP tool input. Ask for the value only when the workflow needs it.                                                                                                   |
| A credential for a remote service            | Use OAuth 2.1 through the remote MCP server. Don't put secrets in the skill archive, manifest, instructions, or default values.                                                               |
| A preference that should persist             | Store it in the hosted service and associate it with the authenticated user. Let the user update it through an explicit workflow or tool input.                                               |
| A setting for a Codex-local script or hook   | Use a documented environment variable or config file. Check it before use and return an actionable error when missing. Don't make this local setting necessary for the core ChatGPT workflow. |
| A fixed value that is the same for all users | Put a non-secret default in the skill instructions or hosted service configuration.                                                                                                           |

If a skills-only plugin needs a credential or a setting that must persist
between conversations, add an MCP server. Use OAuth and hosted storage for the
remote server.
If the value only affects the current task, keep the plugin skills-only and
collect it as an explicit skill input.

## Complete the submission requirements

Before submitting either plugin, get **Apps Management** write access in the
OpenAI organization that will own it. You must also complete individual or
business identity verification. Every plugin must complete OpenAI review.

Contact your OpenAI partner before submitting if the plugin's core value
requires local execution, arbitrary access to files on the user's computer,
hardware or application access, offline operation, or inbound channel
messages. These cases may need product-specific review.

For the complete portal workflow, see
[Submit plugins](https://developers.openai.com/plugins/deploy/submission). If the portal reports a package
validation code, use the
[submission error reference](https://developers.openai.com/plugins/deploy/submission-errors).