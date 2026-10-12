# Remote MCP server review requirements

> For the complete documentation index, see [llms.txt](/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Prepare a remote MCP server and its optional UI for public review as part of a
plugin.

This page covers remote MCP submissions. Submit and publish the complete
  plugin, including its skills, MCP server, and optional UI, through the plugin
  submission portal. See
  [Submit plugins](https://developers.openai.com/plugins/deploy/submission) for the
  source-of-truth submission flow. See
  [Build an MCP server](https://developers.openai.com/plugins/build/mcp-server) for how
  server-backed capabilities fit into plugins.

<a id="prepare-mcp-capabilities-for-plugin-submission"></a>

## Prepare remote MCP capabilities for plugin submission

Use this page for requirements that apply when a plugin includes a remote MCP
server: organization verification, management permissions, server requirements,
review snapshots, and version maintenance.

When the remote MCP server works in
[ChatGPT](https://developers.openai.com/plugins/deploy/connect-chatgpt#test-an-mcp-server-optional),
submit it
for review in the
[plugin submission portal](https://platform.openai.com/plugins). This page
covers the remote MCP server and optional UI requirements for that submission.

Only submit the plugin if you intend for it to be publicly available in the
countries you define during submission. For private or workspace-only use, use
[a custom MCP server connection](https://developers.openai.com/api/docs/guides/custom-mcp-server)
instead.

Before submitting the plugin, review the
[plugin guidelines](https://developers.openai.com/plugins/plugin-guidelines) for MCP server and optional UI
expectations, and see
[Submit plugins](https://developers.openai.com/plugins/deploy/submission) for the full plugin submission,
approval, and publishing flow.

For the complete flow, including skills-only and MCP-backed plugins, review,
approval, and publishing, see
[Submit plugins](https://developers.openai.com/plugins/deploy/submission).

## Before you submit the plugin

### Organization verification

Before submitting any plugin, complete identity verification
in the [OpenAI Platform Dashboard](https://platform.openai.com/settings/organization/general)
for the name you plan to publish under in the directory.

- **If you want to publish under your own name**, complete **individual verification**.
- **If you want to publish under a business name**, complete **business verification**.

This is enforced during review. Publishing under an unverified individual or
business name will result in rejection.

### Plugin submission permissions

To create plugin drafts and submit them for review, you need
the `api.apps.write` permission. To view drafts and review status in the
Dashboard, you need the `api.apps.read` permission. Organization owners
automatically have both permissions, and can grant them to non-owners through
roles in the [OpenAI Platform Dashboard](https://platform.openai.com/settings/organization/roles).

<a id="mcp-server-requirements"></a>

### Remote MCP server requirements

- Your MCP server is hosted on a publicly accessible domain
- You are not using a local or testing endpoint
- If the server returns UI, you defined a [content security policy (CSP)](https://developers.openai.com/plugins/build/chatgpt-ui#content-security-policy-csp) that allows the exact domains the component fetches from.

### Template MCP server URLs

Most plugins should submit a universal MCP server URL: a single hosted MCP endpoint that works for all users and organizations. Choose **Template** only if the plugin uses workspace-specific MCP server URLs, such as when each customer has a separate tenant, workspace, or managed MCP endpoint. We only support template-based URLs for trusted developers with whom we have an established relationship.

Template submissions require two URL values:

- **Example MCP Server URL:** A concrete, working MCP endpoint for review and automated checks.
- **Template MCP Server URL:** The URL pattern that describes which part of the MCP endpoint changes across customer workspaces.

The example MCP server URL must be a real endpoint that OpenAI can connect to during submission review. Don't enter a placeholder URL in the **Example MCP Server URL** field.

Use placeholders in the **Template MCP Server URL** for the parts that a workspace admin will configure later. Placeholders must use `{name}` syntax, start with a letter, and contain only letters, numbers, or underscores. Each placeholder name must be unique.

Make sure the concrete **Example MCP Server URL** matches the template pattern after replacing each placeholder with a real value.

For example:

```text
Example MCP Server URL: https://acme.example.com/mcp
Template MCP Server URL: https://{workspace}.example.com/mcp
```

## Submit for review

If the prerequisites are met, you can submit the plugin
for review from the [plugin submission portal](https://platform.openai.com/plugins).

### Start the review process

In the plugin submission portal:

1. Add your MCP server details (as well as OAuth credentials if OAuth is selected), and then select **Scan Tools**.
2. Complete the required fields in the submission form and check all confirmation boxes. You will need to provide the plugin name, logo, description, company and privacy policy URLs, MCP and tool information, test prompts and responses, and localization information. If the plugin has UI, you may also provide optional screenshots. Don't provide screenshots when the plugin has no UI.
3. Select **Submit for review**.

### Metadata stored during tool scanning

When you select **Scan Tools**, the dashboard imports metadata advertised by your MCP endpoint into the draft. This includes tool names, titles, and descriptions; input and output schemas; security schemes; `_meta` fields; [tool annotations](https://developers.openai.com/plugins/reference#annotations); linked UI resource metadata, including CSP settings; and MCP server `instructions`. The dashboard displays the annotation values provided by your server.

Your submission justifications should explain why those server-provided annotation values match each tool's behavior. They don't override the annotations. For example, if your server advertises `readOnlyHint: false`, describing the tool as “functionally read-only” in the justification doesn't make the tool read-only. If the tool is truly read-only, update its server annotation to `readOnlyHint: true`, deploy the change, select **Scan Tools** again, verify the updated value, and then submit.

Each organization can publish multiple unique plugins with MCP. For each MCP
server integration, only one version may be published at a time and only one
version may be in review at a time. If you need to make changes after
submitting, withdraw that submission by selecting **Cancel Review** and
resubmit the same version draft.

_For now, projects with EU data residency cannot submit plugins with MCP
servers for review. Use a project with global data residency. If you don't have
one, create a new project in your current organization from the OpenAI
Dashboard._

## Review and approval

Once submitted, the plugin will enter the review queue. You can review the
status within the Dashboard and will receive an email notification informing
you of any status changes.

### Reviews and checks

We may perform automated scans or manual reviews to understand how your plugin
works and whether it may conflict with our policies.

### Approval, rejection, and appeals

If your plugin is approved, we will notify you by email. Once approved, you can publish it from the plugin submission portal.

If your plugin is rejected or removed because of its MCP server, tools, or UI,
you will receive feedback on which checks were unsuccessful. After making the
necessary changes, you may resubmit the plugin for review. To appeal the
decision, respond to the email you received with a clear rationale and any new
information that can assist the review.

### Getting help

If you have questions before, during, or after submission and the documentation
does not answer them, contact OpenAI support. Include the ID shown in the plugin
submission portal so the support team can identify your plugin.

### Review and approval FAQs

**How long does review take?**

Review timelines may vary as we continue to build and scale our processes. Please do not contact support to request expedited review, as these requests cannot be accommodated.

**What are common rejection reasons and how can I resolve them?**

- **We're unable to connect to your MCP server using the MCP URL and/or test credentials we were given.**
  - For servers requiring authentication, our review team must be able to log into a demo account with no further configuration required.
  - Ensure that the provided URL and credentials are correct, do not feature MFA (including requiring SMS codes, login through systems that require SMS, email or other verification schemes).
  - Ensure that the provided credentials can be used to log in successfully (test them outside any company networks, local area networks, or other internal networks).
  - Confirm that the credentials have not expired.
- **One or more of your test cases did not produce correct results.**
  - Review all test cases carefully and rerun each one. Ensure that outputs match the expected results. Verify that there are no errors in the UI (if applicable) - for example, issues with loading content, images, or other UI issues.
  - Ensure that the returned textual output closely adheres to the user's request, and does not offer extraneous information that is irrelevant to the request, including personal identifiers.
  - Ensure that all test cases pass on the supported ChatGPT and Codex surfaces
    where the plugin will be available.
  - Compare actual outputs to precise expected behavior for each tool and fix any mismatch so results are relevant to the user's input and the plugin reliably does what it promises.
  - If required, in your resubmission, modify your test cases and expected responses to be clear and unambiguous.
- **Your plugin returns user-related data types that are not disclosed in your privacy policy.**
  - Audit your MCP tool responses in ChatGPT by running a few realistic example requests and listing every user-related field the server returns (including nested fields and “debug” payloads). Ensure tools return only what's strictly necessary for the user's request and remove any unnecessary PII, telemetry/internal identifiers (for example, session, trace, or request IDs; timestamps; internal account IDs; or logs) and any auth secrets (tokens, keys, or passwords).
  - You may also consider updating your published privacy policy so it explicitly discloses all categories of personal data you collect, process, or return and why—if a field isn't truly needed, remove it rather than disclose it.
  - If a user identifier is truly necessary, make it explicitly requested and directly tied to the user's intent (not “looked up and echoed” by default).
- **Tool hint annotations do not appear to match the tool's behavior:**
  - **readOnlyHint:** Set to `true` if it strictly fetches/looks up/lists/retrieves data and does not modify anything. Set to `false` if the tool can create/update/delete anything, trigger actions (send emails/messages, run jobs, enqueue tasks, write logs, start workflows), or otherwise change state.
  - **Destructive hint:** Set the destructive annotation to `true` if the tool can cause irreversible outcomes (deleting, overwriting, sending messages or transactions you can't undo, revoking access, or destructive admin actions), even in only select modes, through default parameters, or through indirect side effects. Ensure the justification explains what is irreversible and under what conditions, including safeguards such as confirmation steps, dry-run options, or scoping constraints. Otherwise, set it to `false`.
  - **openWorldHint:** Set to `true` if the tool accesses the public internet or open-ended external entities. This includes read-only tools such as web search and write tools that post to public platforms, send messages to external recipients, publish content, push code, or submit forms. Set to `false` if the tool is limited to a bounded private account or workspace, even when that service is externally hosted.

## Publication and distribution

### Publish the plugin

Once the plugin is approved, you can publish it from the [plugin submission portal](https://platform.openai.com/plugins) by selecting **Publish**.

### Discovery

Once published, users can find your plugin in the universal directory shared
by ChatGPT and Codex by:

- Clicking a direct link to the plugin listing in the directory.
- Searching for the plugin by name.

Plugins that demonstrate strong real-world utility and high user satisfaction may be eligible for enhanced distribution opportunities—such as directory placement or proactive suggestions—but few plugins will receive enhanced distribution at publication. Developers cannot request enhanced distribution.

### Publication and Distribution FAQs

**What happens after the plugin is approved? Will it be listed in the plugin directory automatically?**

After the plugin is approved, you can choose to publish it from the [plugin submission portal](https://platform.openai.com/plugins). You must publish before it can appear in the universal plugin directory.

**Why can't I see my plugin in the directory?**

Plugins appear on the directory's main pages only if OpenAI selects them for enhanced distribution. To confirm that your plugin is published, search for it using the exact publication name or open its directory URL from the plugin submission portal.

**What should I do if I want to issue a press release or public announcement about my plugin?**

Before issuing any press releases or public announcements regarding the launch
of your plugin, please first reach out to
[press@openai.com](mailto:press@openai.com) to coordinate with our
communications team.

## Ongoing Maintenance

### How published MCP metadata versions work

Treat the metadata exposed by your MCP server as a versioned API contract for
the plugin. When you scan the MCP endpoint in the plugin submission portal,
OpenAI stores the discovered metadata with that draft version. Submitting the
version sends that stored snapshot for review. After publication, continuous
review updates tool definitions without requiring a new plugin version. Tool
calls and UI resources continue to use your live MCP server.

### Continuous review and tool updates

OpenAI periodically fetches your MCP server's tools and compares them with the
published definitions, including their descriptions, schemas, and annotations.

- **Deleted tools:** Removed from the published tool list as soon as a scan
  detects the deletion, without waiting for automated checks.
- **New tools:** Made available after they pass automated checks. Until then,
  they aren't available to users.
- **Changed tools:** The previous definition stays live until the updated
  definition passes automated checks or a scan detects that you removed the tool.
  Passing updates replace the previous definition automatically.

Each tool can pass independently. For example, you add `create_note`, change
`search` to accept a `folder` parameter, and delete `archive_note`. The next
scan removes `archive_note` immediately. If `create_note` passes but the
`search` update is held, users get `create_note` and keep the old `search`
definition without `folder`.

Keep your server compatible with the live definition while an update is held.
OpenAI retains the definition, not a copy of your server implementation.
An incomplete check doesn't approve an update, even if it has no findings.

### Other changes

Use this table to determine how to ship each change:

| Change                                                                                                                                            | Required action                                                                                                                                                                 | When users see the change                                                                                       |
| ------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| Tool security schemes, tool `_meta` fields, UI resource references, or linked resource metadata, including content security policy (CSP) settings | Deploy the change. These fields are reviewed with the tool definition through continuous review.                                                                                | After the updated tool definition passes automated checks.                                                      |
| MCP server `instructions`                                                                                                                         | Deploy the change. Shared instructions are reviewed with the affected tools.                                                                                                    | After the required checks complete without holding existing tool updates or finding issues in the instructions. |
| Backward-compatible content update served from the same published UI resource URI                                                                 | Deploy the content update. You don't need to scan, submit, or publish a new version if the URI and published contract remain compatible.                                        | After deployment. ChatGPT may continue serving cached resource contents for up to one hour.                     |
| Server-only fix or change to live tool results, including result `_meta`, or business data                                                        | Deploy the server change. You don't need to scan, submit, or publish a new version if the change preserves the published contract.                                              | Through your live endpoint after deployment.                                                                    |
| MCP server origin (`scheme`, `hostname`, or `port`)                                                                                               | To change the origin, create a new plugin, then complete its scan, submission, review, and publication flow. To change only the endpoint path, use the normal new-version flow. | After you publish the new plugin or approved version.                                                           |

Server changes take effect before a scan can discover or approve them. Keep
existing input schemas and each published UI resource URI working during that gap.
If a deployment breaks the live contract, roll back the server change rather
than waiting for review.

### Submitting new versions for review

To change submitted plugin information or imported skills, create a new draft
version of the existing plugin and resubmit it for review. Continuous tool
review doesn't replace this process. Each resubmission starts a new review.
In the release notes, describe what changed.

The MCP server origin (`scheme`, `hostname`, or `port`) can't change between
versions. To use a different origin, submit a new plugin with the new MCP
server origin. You can change the endpoint path in a new version of the
existing plugin.

We will review the updated plugin metadata again and inform you by email and in
the [plugin submission portal](https://platform.openai.com/plugins) whether the
update was approved or rejected. If rejected, you may update and resubmit or
appeal the decision.

Once your resubmission is approved, you can publish the update, which will
replace the previous plugin version.

If you've made additional changes to the plugin between submission and approval
and want to submit a new version for review, cancel the review from the plugin
submission portal and resubmit.

### Changing published metadata versions and removing the plugin

To replace a published plugin version, publish an approved replacement directly
from the [plugin submission portal](https://platform.openai.com/plugins). Keep
the current version published while the replacement is under review. Publishing
the approved version replaces the current version, so you don't need to remove
the current version from publication first.

Remove the current version from publication only when you intend to remove the
plugin from public visibility. Without a published replacement, removing the
current version makes the plugin unavailable.

To remove the plugin from your organization and from ChatGPT and Codex, delete
it from the plugin submission portal.

### Maintenance requirements

Plugins may be removed if they are inactive, unstable, or non-compliant. We may
reject or remove any plugin from our services at any time and for any reason
without notice, such as for legal or security concerns or policy violations.

### Ongoing Maintenance FAQs

**What happens if users report my plugin as harmful or misleading?**

OpenAI reviews user reports and may review or investigate your plugin,
including its MCP server, tools, and UI. Plugins that violate our policies may
be restricted or removed. You may appeal a removal or other enforcement action
by following the appeals process described here. Regularly review and respond
to feedback, and update your plugin if issues are found.

**How long will updates take?**

Similar to new reviews, we are unable to offer estimated times for update
reviews.