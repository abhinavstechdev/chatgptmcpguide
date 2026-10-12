# Optimize Metadata

> For the complete documentation index, see [llms.txt](/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

## Why metadata matters

ChatGPT and Codex decide when to call your tool based on the metadata you
provide. Well-crafted names, descriptions, and parameter docs increase recall
on relevant prompts and reduce accidental activations. Treat metadata like
product copy—it needs iteration, testing, and analytics.

## Gather a golden prompt set

Before you tune metadata, assemble a labelled dataset:

- **Direct prompts:** users explicitly name your product or data source.
- **Indirect prompts:** users describe the outcome they want without naming your tool.
- **Negative prompts:** cases where built-in tools or other tools should handle the request.

Document the expected behaviour for each prompt (call your tool, do nothing, or use an alternative). You will reuse this set during regression testing.

## Draft metadata that guides the model

For each tool:

- **Name:** pair the domain with the action (`calendar.create_event`).
- **Description:** start with “Use this when…” and call out disallowed cases ("Do not use for reminders").
- **Parameter docs:** describe each argument, include examples, and use allowed values for constrained inputs.
- **Read-only hint:** annotate `readOnlyHint: true` on tools that only retrieve
  or compute information and never create, update, delete, or send data outside
  the conversation.
- **Destructive hint:** Annotate `destructiveHint: false` on tools that don't
  delete or overwrite user data.
- **Open-world hint:** Annotate `openWorldHint: true` when a tool accesses the
  public internet or open-ended external entities, including read-only tools
  such as web search. Use `false` for a tool limited to a bounded private
  account or workspace, even when that service is externally hosted.

## Evaluate your custom MCP server

1. [Connect your custom MCP server](https://developers.openai.com/api/docs/guides/custom-mcp-server) in ChatGPT and install the resulting plugin.
2. Run through the golden prompt set and record the outcome: which tool was selected, what arguments were passed, and whether the component rendered.
3. For each prompt, track precision (did the right tool run?) and recall (did the tool run when it should?).

If the model picks the wrong tool, revise the descriptions to emphasise the intended scenario or narrow the tool’s scope.

## Iterate methodically

- Change one metadata field at a time so you can attribute improvements.
- Keep a log of revisions with timestamps and test results.
- Share diffs with reviewers to catch ambiguous copy before you deploy it.

After each revision, repeat the evaluation. Aim for high precision on negative prompts before chasing marginal recall improvements.

## Production monitoring

Once your MCP server is live:

- Review tool-call analytics weekly. Spikes in “wrong tool” confirmations usually indicate metadata drift.
- Capture user feedback and update descriptions to cover common misconceptions.
- Schedule periodic prompt replays, especially after adding new tools or changing structured fields.

Treat metadata as a living asset. The more intentional you are with wording and evaluation, the easier discovery and invocation become.