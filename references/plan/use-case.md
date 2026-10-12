# Brainstorm plugin use cases

> For the complete documentation index, see [llms.txt](/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Start by listing the things people will expect your plugin to do. The plugin's
name, description, skills, tools, and connection to an existing product all
create expectations. Your implementation should cover those expectations or
have a deliberate reason not to.

This work determines what belongs in the plugin:

- Add a **skill** when instructions, examples, or bundled resources can guide
  the model through the workflow.
- Add an **MCP server** when the workflow needs live data, authentication,
  controlled tools, or code that runs on infrastructure you operate.
- Add **UI to the MCP server** only when visual interaction materially improves
  part of the workflow.

## Start from user expectations

Imagine that a person has installed your plugin but has not read its
documentation. What would they reasonably ask it to do?

Gather likely requests from:

- Tasks people already complete in your product or service.
- User interviews, support requests, search queries, and feature requests.
- Common terms people use for your product, data, and workflows.
- Existing workarounds that require copying data between tools.
- The plugin name, listing, screenshots, and starter prompts.

Include direct requests that name your plugin and indirect requests that state
the goal. For example, a project-management plugin might need to handle both
“Show my Acme launch board” and “What is blocking the launch?”

Do not limit the brainstorm to workflows that fit your current API. First
capture what people will expect. Then compare those expectations with what you
can support safely and reliably.

## Build a use-case inventory

For each use case, record:

| Field             | Question to answer                                                         |
| ----------------- | -------------------------------------------------------------------------- |
| User goal         | What is the person trying to accomplish?                                   |
| Example requests  | How might they ask directly or indirectly?                                 |
| Expected result   | What would make the interaction successful?                                |
| Required context  | What information, account access, or prior state is needed?                |
| Plugin capability | Can a skill handle it, or does it need an MCP tool?                        |
| Safety boundary   | Could it expose data, change state, spend money, or affect another person? |
| Support decision  | Will the first version support it, defer it, or intentionally exclude it?  |

Group requests that share the same goal. “List my open tasks,” “What do I need
to do today?” and “Show overdue work” may belong to one task-review use case
with different filters rather than three unrelated features.

## Check coverage

Review every expectation against the proposed plugin capabilities:

1. Confirm that each supported use case has a complete path from request to
   useful result.
2. Identify missing skills, tools, data, permissions, or error states.
3. Look for tools that expose technical operations without completing a
   recognizable user goal.
4. Verify that write actions include appropriate authorization and confirmation.
5. Check that the plugin can explain what it cannot do and offer a useful next
   step.

A plugin should not imply broad capability while supporting only a narrow
slice of the expected workflow. If users can create projects but cannot list,
inspect, or update them, either add the missing coverage or narrow the plugin's
positioning.

## Document intentional exclusions

You do not need to implement every imaginable request. You should have a good
reason for each important exclusion, such as:

- The action would create unacceptable safety or privacy risk.
- The underlying product or API does not support it reliably.
- The workflow requires permissions that the plugin cannot verify.
- The result would be misleading without information the plugin cannot access.
- The use case is out of scope for the first release and the plugin's listing
  sets that expectation.

Record these decisions. They should inform skill boundaries, tool
descriptions, refusal behavior, test cases, and public listing copy.

## Turn use cases into build decisions

For each supported use case, choose the smallest implementation that can
complete it:

- [Build a skill](https://developers.openai.com/plugins/build/skills) for repeatable instructions and
  resources.
- [Build an MCP server](https://developers.openai.com/plugins/build/mcp-server) for live data and
  controlled actions.
- [Add UI to the MCP server](https://developers.openai.com/plugins/build/chatgpt-ui) when people need to
  inspect, compare, edit, confirm, or navigate structured information.

Keep the use-case inventory as a test plan. Add representative direct,
indirect, edge-case, and out-of-scope requests, then verify that the finished
plugin behaves as intended for each one.

If the plugin needs live data or controlled actions, continue with
[Define tools](https://developers.openai.com/plugins/plan/tools).