# Build skills

> For the complete documentation index, see [llms.txt](/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

A skill complements your MCP server by teaching ChatGPT and Codex how to use
its tools in a repeatable workflow. Use the server for live data,
authentication, authorization, and controlled actions. Use the skill for tool
sequences, decision points, output requirements, examples, templates, and
other reusable guidance.

A plugin can contain one skill or a group of related skills. Keep every skill
focused on a recognizable user goal from your
[use-case inventory](https://developers.openai.com/plugins/plan/use-case). A skill can also work without an
MCP server when the workflow needs only packaged instructions and resources.

## Create a skill

The fastest way to start is with the built-in skill creator. Describe the user
goal and the MCP tools that support it:

```text
@skill-creator Create a skill named tabletop-dice that understands dice
notation such as 3d6, calls roll_dice once for each die, and reports every
roll and the total.
```

In Codex, invoke the same creator as `$skill-creator`.

You can also create the files manually. Each skill lives in its own directory
and requires a `SKILL.md` file:

## Write `SKILL.md`

Start the file with a name and a description, followed by the instructions:

```md
---
name: tabletop-dice
description: Roll one or more dice for tabletop games and report each result and the total.
---

Use this skill when the user asks to roll dice.

1. Parse requests written as `NdS` as N dice with S sides. For example, `3d6`
   means three six-sided dice.
2. Call `roll_dice` once for each requested die and pass S as `sides`.
3. Report each tool result in order.
4. When the user requests multiple dice, add the results and report the total.

Do not invent, replace, or reroll a result unless the user asks you to.
```

The description determines when the model considers the skill. State the
workflow and the conditions that should trigger it. Put detailed procedure,
format, and safety instructions in the body.

## Define the workflow boundary

Connect every skill to one or more use cases. The instructions should make the
following clear:

- What input the workflow expects.
- Which steps the model should follow.
- What output the user should receive.
- Which facts the model must not infer.
- When the workflow should ask a question, stop, or decline.
- Which supporting files the model should consult.

Prefer one focused skill over a large collection of loosely related
instructions. Split workflows when they have different triggers, inputs, or
success criteria.

### Review instruction following

When writing or importing skills for GPT-6 Astra, review the [instruction-following guidance](https://developers.openai.com/api/docs/guides/latest-model#gpt-6-astra-instruction-following).
Audit skills and supporting files for unclear or conflicting instructions, and
make the priority of explicit user instructions over skill guidelines clear.

## Add supporting resources

Keep `SKILL.md` concise and place detailed material next to it:

- Use `references/` for policies, schemas, examples, and background material.
- Use `assets/` for templates or files the workflow should copy or transform.
- Use `scripts/` when the workflow needs deterministic computation or file
  processing.

Reference supporting files from `SKILL.md` and explain when to load or run
them. Do not add a script when instructions and existing tools can complete the
task reliably.

## Connect skills to MCP tools

A skill can guide the model through tools exposed by the plugin's MCP server.
Use the skill for workflow instructions and the server for live data,
authorization, and controlled actions.

If a skill requires an MCP server, declare the dependency in
`agents/openai.yaml`:

```yaml
dependencies:
  tools:
    - type: "mcp"
      value: "dice-roller"
      description: "Roll an N-sided die"
      transport: "streamable_http"
      url: "https://tinymcp.dev/api/moldy-aloof-zettabyte/mcp"
```

A dependency makes the required tool available; it does not replace clear
  workflow instructions. Tell the model which tools to use, in what order, and
  how to handle missing or ambiguous results.

## Import a skill from MCP

You can upload a packaged skill during submission or import it from the
plugin's MCP server. The MCP option keeps the skill's instructions and
supporting files with the server deployment.

OpenAI imports skills from MCP when you select **Scan Tools** in the plugin
submission portal. The imported files become a snapshot in the draft; ChatGPT
and Codex do not fetch them from your MCP server at runtime. After changing the
skill, deploy the server and scan it again before submitting a new plugin
version.

For the capability declaration, discovery methods, resource manifest, and
import limits, see
[Import skills from the MCP server](https://developers.openai.com/plugins/build/mcp-server#import-skills-from-the-mcp-server).

## Test the skill

Test with representative requests from the use-case inventory:

1. Direct requests that should activate the skill.
2. Indirect requests that express the same goal.
3. Incomplete inputs that should trigger a follow-up question.
4. Requests that should not activate the skill.
5. Edge cases where the skill must avoid inventing information or taking an
   unsupported action.

Review both activation and output quality. Refine the description when the
skill activates at the wrong time. Refine the instructions when it chooses the
right workflow but produces an inconsistent result.

## Package the skill

Point the plugin manifest at the skills directory:

```json
{
  "name": "dice-roller",
  "version": "1.0.0",
  "description": "Roll dice for tabletop games",
  "skills": "./skills/",
  "apps": "./.app.json"
}
```

See [Package your plugin](https://developers.openai.com/plugins/build/plugins) for the complete manifest,
MCP server mapping, local testing, and distribution flow.