# Skills

> For the complete documentation index, see [llms.txt](/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Skills are folders of instructions and resources that teach ChatGPT and Codex
how to complete repeatable workflows. In an MCP-backed plugin, skills
complement the server by teaching the model how to combine its tools for
recognizable user goals.

Each skill has a `SKILL.md` file with:

- A name.
- A description that tells the model when to consider the skill.
- Instructions for completing the workflow.
- Optional references, scripts, templates, and other assets.

## How skills complement an MCP server

An MCP server provides live information and controlled actions. A skill
provides the workflow around those tools: when to call them, in what order, how
to handle incomplete results, and what the final output should contain.

For example, a skill can define how to:

- Retrieve account activity and turn it into a customer briefing.
- Review project data, identify risks, and draft a status update.
- Combine search and fetch tools into a sourced research workflow.
- Apply an organization's writing or review standards to MCP results.

Keep the boundary clear: the [MCP server](https://developers.openai.com/plugins/concepts/mcp-server)
provides data, authentication, authorization, and actions; the skill provides
reusable instructions, examples, templates, and other resources. A skill can
also work without an MCP server when the workflow needs only packaged
instructions and resources.

## How skills activate

The model first sees skill metadata, including the name and description. It
loads the complete instructions when the user's request matches the skill or
the user invokes it directly.

Write descriptions around the user goal and the conditions that should trigger
the workflow. Keep detailed steps and output requirements in the instruction
body.

## Skills in a plugin

Skills are the workflow layer of a plugin. They can:

- Guide the model through tools exposed by the plugin's MCP server.
- Package organization-specific procedures with reusable templates and
  references.
- Work on their own when no live data or controlled action is required.

Skills and MCP tools should have clear, complementary roles. A skill explains
how to complete the workflow; an MCP server provides live information and
enforces controlled actions.

Continue with [Build skills](https://developers.openai.com/plugins/build/skills) to create, test, and
package a skill.