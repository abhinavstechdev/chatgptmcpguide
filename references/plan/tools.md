# Define tools

> For the complete documentation index, see [llms.txt](/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Tools are the actions and data that a plugin's MCP server exposes to ChatGPT
and Codex. Define them after you
[brainstorm use cases](https://developers.openai.com/plugins/plan/use-case) and before you implement the
server.

Every tool should help complete a user goal. Do not mirror an internal API
without considering how people will ask for and use the capability.

## Map use cases to tools

For each supported use case:

1. Write the outcome the user expects.
2. List the information required to produce that outcome.
3. Identify the reads, writes, or external actions the server must perform.
4. Group operations that represent one coherent action.
5. Split operations when they have different permissions, safety risks, or
   confirmation requirements.

For example, a project plugin might expose:

- `list_projects` to find projects.
- `get_project` to inspect one project.
- `create_project` to create a project.
- `update_project` to change project details.
- `archive_project` to perform a consequential state change.

Separate read and write behavior so the model and user can distinguish
information retrieval from actions that change state.

## Define each contract

Record the following for every proposed tool:

| Field            | What to define                                                       |
| ---------------- | -------------------------------------------------------------------- |
| Name             | A stable, action-oriented identifier.                                |
| Title            | A concise human-readable action.                                     |
| Description      | The user goal and conditions that should trigger the tool.           |
| Input schema     | Required and optional parameters, types, allowed values, and limits. |
| Output schema    | Structured fields the model can inspect and reuse.                   |
| Authorization    | The account, role, or resource access the server must verify.        |
| Side effects     | Data or external state the tool can change.                          |
| Failure behavior | Errors the model can explain or recover from.                        |

Use explicit inputs. Do not depend on the model guessing identifiers, account
scope, or other values that are required for correctness.

Return stable identifiers and enough structured information for follow-up
calls. Keep secrets, access tokens, internal diagnostics, and unnecessary
personal data out of results.

## Write descriptions for selection

The model uses tool descriptions to decide when a tool fits a request. Describe
the user intent, not the implementation.

Good descriptions:

- State what the tool does.
- Explain when to use it.
- Distinguish it from similar tools.
- Call out important limits or prerequisites.

Avoid descriptions that only restate the tool name or expose internal service
terminology that users do not know.

## Plan safety annotations

Assign annotations based on actual behavior. See the MCP
[`ToolAnnotations`
schema](https://modelcontextprotocol.io/specification/2025-11-25/schema#toolannotations)
for the canonical definitions, defaults, and interactions between these hints:

- `readOnlyHint` is `true` only when the tool cannot change state.
- `destructiveHint` is `true` when the tool can cause irreversible or difficult
  to reverse outcomes.
- `openWorldHint` is `true` when the tool accesses the public internet or
  open-ended external entities, including through read-only actions such as
  web search. A bounded private account or workspace isn't open-world solely
  because it is externally hosted.

Annotations do not replace server-side authorization, input validation, or
confirmation for consequential actions.

## Check coverage and boundaries

Compare the proposed tools with the complete use-case inventory:

1. Confirm that every supported use case has a path to a useful result.
2. Identify tools that do not serve a documented use case.
3. Look for missing reads that users need before taking a write action.
4. Verify that unsupported requests produce an understandable limitation
   instead of an unsafe approximation.
5. Test whether two similar tools have overlapping descriptions that could
   confuse selection.

Keep the resulting tool plan as an implementation and evaluation checklist.
Then [build the MCP server](https://developers.openai.com/plugins/build/mcp-server) and test each contract
with representative, invalid, and unauthorized inputs.