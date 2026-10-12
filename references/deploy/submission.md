# Upload and submit your plugin

> For the complete documentation index, see [llms.txt](/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

If you’ve built a plugin and want to share it more broadly, the plugin directory helps people discover and use it in ChatGPT and Codex. Your plugin can include MCP connections, skills, or both.

Submit the package you’ve already built as a ZIP, resolve automated findings, and submit it for review. Once approved, you choose when to publish.

After initial publication, changes to your MCP server are picked up automatically, and eligible updates go live once they pass automated checks. There’s no need to upload a new plugin ZIP or publish each update; changes to plugin metadata or skills still require a new ZIP.

Before submitting, follow the [plugin package guide](https://developers.openai.com/plugins/build/plugins) and read the [plugin guidelines](https://developers.openai.com/plugins/plugin-guidelines). For help preparing your submission, use [Plugin Creator](https://chatgpt.com/plugins/plugin_connector_1p_e1a10c53223481918a42f1510ec46c1e?open_in_app), available in the plugin directory.

![Plugins dashboard showing upload, publication, review, and MCP setup status.](https://cdn.openai.com/devhub/docs/plugins/submission/plugins-overview-20260927.webp)

**_Plugins overview._** _Start a submission and track publication, review progress, and MCP setup from the Plugins page._

## 1. Upload your plugin ZIP

### Confirm access and publishing identity

Select the organization and project that will own the plugin. Organization owners can submit; other members need **Apps Management Write**, which an owner can grant through [organization roles](https://platform.openai.com/settings/organization/people/roles).

Complete individual or business verification in [organization settings](https://platform.openai.com/settings/organization/general) to publish under your name or a company name.

### Create the draft

If your plugin uses an MCP server, include it in the initial ZIP. Adding an MCP server to an existing skills-only plugin is not currently supported.

1. Open [Plugins](https://platform.openai.com/plugins) and select **Upload new or existing plugin**.
2. Choose your verified **Developer identity**. The directory displays the name associated with this identity.
3. Select **Upload plugin** and choose your ZIP file.
4. After validation, the plugin detail page opens with your new draft.

If validation fails, correct the reported package errors and upload again. Keep private credentials and secrets out of the ZIP.

## 2. Review checks and resolve issues

After you upload your ZIP, the plugin detail page shows automated check progress and findings so you can address issues before submitting for review. **Metadata &amp; Skills** shows the uploaded plugin package version, and **MCPs** shows the connected server and its scanned tools. These are separate because package changes require a new ZIP, but hosted tool changes are checked directly from your server.

### Check metadata

1. Open **Metadata &amp; Skills**. The most recently uploaded version is shown automatically.
2. Wait for the metadata checks to finish, then look for any **Issues** detected.
3. Select **Copy issues** to bring the findings into your development workflow.
4. Correct the affected fields in your package, then select **Upload plugin to fix issues** and upload the corrected ZIP. Check the new results.

**Tip:** Ask Codex or ChatGPT to inspect your package and the copied findings, explain the issues, and suggest corrections to the metadata or skills.

![Plugin metadata and skills with automated findings in the Issues panel.](https://cdn.openai.com/devhub/docs/plugins/submission/metadata-findings-20260927.webp)

**_Metadata findings._** _Review findings for the selected package version and upload a corrected ZIP._

Package details are read-only here; edit them in your source package using the [package field reference](#automatically-provide-submission-and-review-information). Public URLs must be accessible and identify the same publisher as the submission.

### Check skills

If your package contains skills, review any findings in **Metadata &amp; Skills**. Open a finding to see the affected skill and what needs to change, then update its instructions or supporting files and upload a corrected ZIP. Check the updated findings; required skill scans must finish successfully before you can submit.

<a id="mcp"></a>

### Connect and scan your MCP server

Your package can declare multiple MCP servers, but **only one MCP server can be connected per plugin**. Complete the setup below when you first connect that server. Use **Reconnect** if the connection needs attention; for tool changes, follow [Scan your latest changes](#scan-your-latest-changes).

1. Open **MCPs** and select the server you want to connect.
2. Select **Connect** to open **Connect MCP server**.
3. Check **MCP Server URL**, **Authentication**, and the applicable settings.
4. Complete the domain-verification challenge shown in the portal, then connect the server and complete authentication if required.
5. Wait for the automated tool scan to finish, then inspect the discovered tools. Open **Issues** to read any findings.
6. Correct connection problems or server-side findings, then use **Reconnect** or **Rescan**, as applicable, and check the new results.

![Connect MCP server drawer showing a verified domain and pending OAuth authorization.](https://cdn.openai.com/devhub/docs/plugins/submission/mcp-connection-20260927.webp)

**_MCP connection and domain verification._** _Connect the server and complete domain verification before checking the discovered tools._

If connecting or scanning fails, check endpoint availability and authentication, then reconnect or rescan. Resolve **Complete MCP setup** findings and connection failures before submitting. See the [plugin guidelines](https://developers.openai.com/plugins/plugin-guidelines) for MCP server URL, authentication, tool metadata, and UI requirements.

#### Configure authentication for submission

The portal reads advanced authentication settings from your package's
`mcp.json`. Configure the authentication method, OAuth client registration,
endpoints, and scopes using the [MCP authentication reference](https://developers.openai.com/plugins/build/plugins#configure-mcp-authentication).
The connection panel displays those settings; it doesn't provide an advanced
OAuth settings editor.

To change the configuration, update `mcp.json`, select **Upload new version**,
and inspect the saved settings under **MCPs** before connecting. Existing client
registration can lock credential changes; check the saved connection rather
than assuming an upload replaces an existing client.

For OAuth, choose a registration method supported by your provider:

| Registration method                          | What to provide                                                                                                                     |
| -------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| Registered client (`provided`)               | Declare the client ID and token endpoint authentication method in `mcp.json`. Enter the client secret in the portal when required.  |
| Dynamic Client Registration (`dcr`)          | Provide a registration endpoint through discovery or a `registrationUrl` override. Don't include client credentials in the package. |
| Client Identifier Metadata Document (`cimd`) | Configure CIMD preference. The runtime can fall back to DCR according to its registration policy.                                   |

For a registered client:

1. Register the callback URL used by the connection flow with your OAuth provider.
2. Open **MCPs**, select your server, and select **Connect**.
3. Enter **OAuth Client Secret** if your client requires a secret. The field appears for a provided OAuth client unless `tokenEndpointAuthMethod` is `"none"`.
4. Complete domain verification if needed, select **Connect**, and authorize the account used to connect and scan the server.
5. Wait for the scan to finish and resolve any connection or tool findings.

Don't put the client secret in `mcp.json`; the manifest rejects
`clientSecret`. The client secret authenticates your OAuth application. It
isn't the account password, an access token, or reviewer sign-in credentials.

If OAuth discovery doesn't provide the required endpoints, add
`authorizationUrl` and `tokenUrl` overrides to `mcp.json`. Ensure the client
ID, token endpoint authentication method, scopes, and callback URL match the
provider's configuration.

#### Authentication limitations

The portal connection form supports no authentication, OAuth, and mixed
unauthenticated/OAuth access. Although the manifest schema accepts API-key
authentication, the portal doesn't provide an API-key connection flow or a
bearer-token input. This limitation also applies to Basic and custom-header
API-key declarations. Uploading an API-key declaration alone won't complete
MCP setup. Contact OpenAI if your submission requires this authentication method.

Don't embed a token in server `headers` to work around this limitation:
public submission rejects nonempty server headers. Don't configure a protected
server as `type: "none"`.

The schema accepts `private_key_jwt` for a provided OAuth client, but that
value alone doesn't configure signing keys. This portal guide doesn't provide
a signing-key setup procedure; confirm the required setup with OpenAI before
using that method for submission.

<a id="domain-verification"></a>

#### Domain verification details

For domain verification, host the exact challenge token as plain text at the URL shown in the portal:

```text
https://<challenge-base-host>/.well-known/openai-apps-challenge
```

Return only the exact token—not JSON or a list of tokens. The challenge base must be an HTTPS origin on the MCP hostname or an eligible parent domain; paths are ignored. If another plugin uses the same challenge URL, use an allowed parent origin or a distinct hostname rather than replacing its token. Contact support if neither is possible.

## 3. Submit for review

Once you’ve reviewed the automated findings, complete the information the review team needs to test your plugin and submit the selected draft. Required setup and validation errors need to be resolved first; other automated findings can be sent to the review team for consideration.

### Complete review information

Plugins with MCP connections need review information so the review team can test the integration. You can include positive and negative test cases, the video walkthrough URL, and release notes in `plugin.json` so they are imported with the ZIP. See the [review and publication field reference](#configure-onboarding-review-and-publication) and [complete metadata examples](#complete-metadata-examples). [Plugin Creator](https://chatgpt.com/plugins/plugin_connector_1p_e1a10c53223481918a42f1510ec46c1e?open_in_app), available in the plugin directory, can help prepare this information. Reviewer credentials are entered separately in **Review details**. Prepare:

- **Reviewer credentials, if sign-in is required.** Provide a dedicated test account, login URL, workspace or tenant details, and sign-in instructions. Use sample data, not a real user’s account. The account needs the permissions and data required by your test cases and should work immediately without MFA approval, email or SMS codes, magic links, or private-network access.
- **Five positive test cases.** Include the scenario, user prompt, expected tools, and expected result. Run each case using the test account before submitting.
- **Three negative test cases.** Include a prompt or scenario where the plugin should not act, why it should not complete the request, and the expected refusal, clarification, or safe fallback.
- **A video walkthrough.** Demonstrate the test cases and plugin functionality, and provide an accessible recording URL.
- **Release notes.** Summarize the package version being submitted and what changed.

In **Metadata &amp; Skills**, open **Review information → Review details** to check the imported materials and enter reviewer credentials. Complete any editable fields and select **Save details**. For fields marked as managed by your plugin ZIP, add or change the information in your package and upload it again. Country availability and translations can also be supplied in the package metadata; check the imported settings where applicable. See [Automatically provide submission and review information](#automatically-provide-submission-and-review-information) for supported fields and import behavior.

![Review information drawer with fields for reviewer credentials and sign-in instructions.](https://cdn.openai.com/devhub/docs/plugins/submission/review-details-20260927.webp)

**_Review details._** _Check test cases and supporting materials imported from your ZIP, and enter private reviewer credentials separately._

Credentials stay outside the public package. Keep the test account and sample data available for subsequent reviews. If credentials or sign-in steps change, submit an updated draft with the new details.

### Submit the draft

Select the draft, choose **Submit for review**, and complete the required policy attestations. After submitting, track progress under **Review status** on the Plugins page. Feedback from the review team is sent by email.

![Submit for review dialog with required policy attestations.](https://cdn.openai.com/devhub/docs/plugins/submission/submit-for-review-20260927.webp)

**_Submit for review._** _Confirm the required attestations and submit the selected draft for review._

Only one review can be active per plugin. To replace a package under review, wait for the decision or cancel the review before uploading. For a rejected package, address the feedback and submit a corrected ZIP.

If the review team rejects your submission, check the rejection email for the reason. To appeal, reply to that email and explain why the decision should be reconsidered.

## 4. Publish your approved plugin

Once your plugin is approved, you choose when to make it available. Open the approved package version and select **Publish plugin**. Publishing an update replaces the previous package version.

## Update your published plugin

To update metadata, assets, or bundled skills, upload a new ZIP to the existing plugin. This creates a package version with its own checks and review outcome. Changes to hosted tools are handled separately through [MCP scans](#update-to-your-mcp-server), so they don’t require a package upload.

If you submitted through the previous submission form, download your existing plugin as a ZIP to get started. Open the plugin, select the published package version, and choose **Download release ZIP** from the **…** menu. If you already maintain the package locally, you can use that source instead.

1. Update the package contents and version number, then create a complete ZIP, including all components you intend to keep.
2. Open the existing plugin and select **Upload plugin to make changes**.
3. Confirm the selected package version in **Metadata &amp; Skills**. Review the new automated findings and resolve required issues.
4. Complete the applicable review steps and publish the approved package version.

Use the same plugin when adding or removing skills. To change an existing MCP server’s URL, contact support; the current update flow does not support URL changes.

## Update to your MCP server

After initial publication, OpenAI scans your hosted MCP server daily. Eligible updates become available after automated checks pass, without a new package version or a separate publish action. You can also request a scan immediately after deploying server changes.

### Scan your latest changes

1. Deploy the changes to your MCP server.
2. Open the existing plugin, select **MCPs**, and choose the connected server.
3. Under **Issues**, select **Rescan**.
4. Wait for the scan to finish and check the results and tool availability.

![MCP tools showing live availability, held updates, and scan findings.](https://cdn.openai.com/devhub/docs/plugins/submission/mcp-scan-overview-20260927.webp)

**_MCP scan overview._** _Rescan after server changes, then inspect the results and each tool’s availability._

Rescan may be unavailable during another scan, an active appeal, or when the plugin is not eligible for scanning.

### Find and resolve tool issues

1. Open **Issues** and select an affected tool.
2. Read **Issues found** and inspect **Held update** to see the metadata that was evaluated. **Live definition** shows the metadata currently in use.
3. Select **Copy issues** to bring the findings into your development workflow.
4. Correct the tool metadata or implementation on your server and deploy the changes.
5. Return to **Issues**, select **Rescan**, and check the updated results.

**Tip:** Ask Codex or ChatGPT to inspect your MCP server and the copied error. Ask it to explain the issue and suggest a fix.

Tool changes are evaluated independently. A flagged change does not necessarily block other eligible tool updates. New tools remain unavailable until approved; existing tools retain their previously approved metadata when an update is held. Removals take effect after a scan.

Keep your MCP server compatible with the currently approved tool schemas until the updated metadata is live.

### Appeal an automated finding

If you believe a tool finding is incorrect, select **Appeal** and explain why the review team should reconsider the findings. The review team considers the held tool changes from that scan together. If the finding is valid, correcting it on the server and rescanning is usually faster.

![Appeal dialog explaining that review covers the held tool changes from the scan.](https://cdn.openai.com/devhub/docs/plugins/submission/mcp-appeal-20260927.webp)

**_MCP appeal._** _Explain why the review team should reconsider the automated finding._

Automatic MCP updates pause during an appeal. To make changes, select **Withdraw appeal**, update the server, and rescan. Appeals cover held tool changes, not package changes, authentication, or shared server instructions.

For troubleshooting, see [submission errors](https://developers.openai.com/plugins/deploy/submission-errors). Include your plugin ID when contacting support.

<a id="prepare-metadata-in-pluginjson"></a>

## Automatically provide submission and review information

You can include listing, review, and publication details in your plugin manifest so they’re filled in when you upload your ZIP. The reference below covers supported fields, how uploads apply them, and examples for each package format.

Plugin ZIPs containing app references (`apps` / `.app.json`) or lifecycle hooks cannot currently be submitted. Declare MCP server URLs in your MCP configuration and complete setup in the dashboard.

Remove lifecycle hooks before public directory submission. If your plugin depends
on lifecycle hooks, distribute it so users can install it manually in Codex desktop.

### Complete metadata examples

These examples describe the same illustrative notes plugin in each format. Copy the manifest for your format, then replace the publisher information, URLs, tool names, review cases, translations, and country availability with your actual values. The example cases have not been run against a real service.

Include the files referenced by the manifest:

- `skills/get-started/SKILL.md`, with valid name and description fields in the YAML header.
- The four icon files and screenshot under `assets/`.
- Exactly one remote MCP server named notes, configured in `mcp.json` for Agent Plugins or `.mcp.json` for Codex, using the matching configuration that follows.

Use your own accessible demo and review attachment URLs. The example.com links show the expected shape and aren’t working submission materials. If your plugin contains only skills, omit review and the MCP configuration, and omit `mcpServers` from the Codex manifest.

Use this companion `mcp.json` for the Agent Plugins example:

```json
{
  "$schema": "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json",
  "mcpServers": {
    "notes": {
      "type": "streamable-http",
      "url": "https://example.com/mcp"
    }
  }
}
```

For the Codex example, save this as `.mcp.json` at the plugin root. This format omits the Agent Plugins schema:

```json
{
  "mcpServers": {
    "notes": {
      "url": "https://example.com/mcp"
    }
  }
}
```

#### Agent Plugins format

Save this complete manifest as plugin.json at the plugin root:

```json
{
  "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
  "name": "acme-notes",
  "version": "1.0.0",
  "description": "Search and summarize notes from your Acme workspace.",
  "author": {
    "name": "Acme",
    "email": "support@example.com",
    "url": "https://example.com"
  },
  "homepage": "https://example.com/notes",
  "repository": "https://github.com/example/acme-notes",
  "license": "MIT",
  "keywords": ["notes", "search", "productivity"],
  "extensions": {
    "com.openai": {
      "interface": {
        "displayName": "Acme Notes",
        "shortDescription": "Find and summarize your notes",
        "longDescription": "Search notes in your Acme workspace, open matching notes, and summarize decisions with links to the source. Acme Notes only accesses notes available to your connected account.",
        "developerName": "Acme",
        "category": "Productivity",
        "capabilities": ["Search notes", "Read notes"],
        "websiteURL": "https://example.com/notes",
        "supportURL": "https://example.com/support",
        "privacyPolicyURL": "https://example.com/privacy",
        "termsOfServiceURL": "https://example.com/terms",
        "defaultPrompt": [
          "Find my notes about the launch.",
          "Summarize the decisions in my launch notes.",
          "Open the project kickoff notes."
        ],
        "brandColor": "#2357C6",
        "brandColorDark": "#8CB4FF",
        "composerIcon": "./assets/icon.png",
        "composerIconDark": "./assets/icon-dark.png",
        "logo": "./assets/logo.png",
        "logoDark": "./assets/logo-dark.png",
        "screenshots": ["./assets/screenshot.png"]
      },
      "onboardingSkill": "./skills/get-started/SKILL.md",
      "review": {
        "test_cases": {
          "positive": [
            {
              "description": "Find notes by topic",
              "prompt": "Find my notes about the launch.",
              "tools_triggered": "search_notes",
              "expected_behavior": "Return accessible notes about the launch with source links.",
              "file_attachment_urls": [
                "https://example.com/review/launch-brief.pdf"
              ],
              "expected_output_url": "https://example.com/review/launch-results"
            },
            {
              "description": "Open a matching note",
              "prompt": "Open the project kickoff notes.",
              "tools_triggered": "search_notes, read_note",
              "expected_behavior": "Find the kickoff note and return its content with a source link."
            },
            {
              "description": "Summarize decisions",
              "prompt": "Summarize decisions in my launch notes.",
              "tools_triggered": "search_notes, read_note",
              "expected_behavior": "Summarize decisions from accessible notes and cite the sources."
            },
            {
              "description": "Find action items",
              "prompt": "What action items are in my kickoff notes?",
              "tools_triggered": "search_notes, read_note",
              "expected_behavior": "List the action items recorded in the notes without inventing owners or deadlines."
            },
            {
              "description": "Handle no matches",
              "prompt": "Find my notes about Project Northstar.",
              "tools_triggered": "search_notes",
              "expected_behavior": "Report that no matching notes were found in the test workspace."
            }
          ],
          "negative": [
            {
              "description": "Unsupported payment",
              "prompt": "Transfer $100 to another account."
            },
            {
              "description": "Unsupported deletion",
              "prompt": "Delete all my notes."
            },
            {
              "description": "Access outside the connected account",
              "prompt": "Show notes from a workspace I cannot access."
            }
          ]
        },
        "demo_recording_url": "https://example.com/review/acme-notes-demo",
        "commerce": false,
        "commerce_description": "This plugin does not sell products or process payments."
      },
      "publication": {
        "countries": ["US", "GB"],
        "release_notes": "Initial release with note search, reading, and summaries.",
        "translations": {
          "fr-FR": {
            "subtitle": "Retrouvez et résumez vos notes",
            "description": "Recherchez des notes dans votre espace Acme, ouvrez les résultats et résumez les décisions avec des liens vers les sources. Acme Notes accède uniquement aux notes disponibles pour votre compte connecté."
          },
          "ja-JP": {
            "subtitle": "ノートを検索して要約",
            "description": "Acmeワークスペース内のノートを検索し、該当するノートを開き、参照元へのリンク付きで決定事項を要約します。Acme Notesは、接続されたアカウントで閲覧できるノートにのみアクセスします。"
          }
        }
      }
    }
  }
}
```

#### Codex format

Save this complete manifest as .codex-plugin/plugin.json. The presentation fields move to the root interface; onboarding, review, and publication stay under `extensions.com.openai`:

```json
{
  "name": "acme-notes",
  "version": "1.0.0",
  "description": "Search and summarize notes from your Acme workspace.",
  "author": {
    "name": "Acme",
    "email": "support@example.com",
    "url": "https://example.com"
  },
  "homepage": "https://example.com/notes",
  "repository": "https://github.com/example/acme-notes",
  "license": "MIT",
  "keywords": ["notes", "search", "productivity"],
  "skills": "./skills/",
  "mcpServers": "./.mcp.json",
  "interface": {
    "displayName": "Acme Notes",
    "shortDescription": "Find and summarize your notes",
    "longDescription": "Search notes in your Acme workspace, open matching notes, and summarize decisions with links to the source. Acme Notes only accesses notes available to your connected account.",
    "developerName": "Acme",
    "category": "Productivity",
    "capabilities": ["Search notes", "Read notes"],
    "websiteURL": "https://example.com/notes",
    "supportURL": "https://example.com/support",
    "privacyPolicyURL": "https://example.com/privacy",
    "termsOfServiceURL": "https://example.com/terms",
    "defaultPrompt": [
      "Find my notes about the launch.",
      "Summarize the decisions in my launch notes.",
      "Open the project kickoff notes."
    ],
    "brandColor": "#2357C6",
    "brandColorDark": "#8CB4FF",
    "composerIcon": "./assets/icon.png",
    "composerIconDark": "./assets/icon-dark.png",
    "logo": "./assets/logo.png",
    "logoDark": "./assets/logo-dark.png",
    "screenshots": ["./assets/screenshot.png"]
  },
  "extensions": {
    "com.openai": {
      "onboardingSkill": "./skills/get-started/SKILL.md",
      "review": {
        "test_cases": {
          "positive": [
            {
              "description": "Find notes by topic",
              "prompt": "Find my notes about the launch.",
              "tools_triggered": "search_notes",
              "expected_behavior": "Return accessible notes about the launch with source links.",
              "file_attachment_urls": [
                "https://example.com/review/launch-brief.pdf"
              ],
              "expected_output_url": "https://example.com/review/launch-results"
            },
            {
              "description": "Open a matching note",
              "prompt": "Open the project kickoff notes.",
              "tools_triggered": "search_notes, read_note",
              "expected_behavior": "Find the kickoff note and return its content with a source link."
            },
            {
              "description": "Summarize decisions",
              "prompt": "Summarize decisions in my launch notes.",
              "tools_triggered": "search_notes, read_note",
              "expected_behavior": "Summarize decisions from accessible notes and cite the sources."
            },
            {
              "description": "Find action items",
              "prompt": "What action items are in my kickoff notes?",
              "tools_triggered": "search_notes, read_note",
              "expected_behavior": "List the action items recorded in the notes without inventing owners or deadlines."
            },
            {
              "description": "Handle no matches",
              "prompt": "Find my notes about Project Northstar.",
              "tools_triggered": "search_notes",
              "expected_behavior": "Report that no matching notes were found in the test workspace."
            }
          ],
          "negative": [
            {
              "description": "Unsupported payment",
              "prompt": "Transfer $100 to another account."
            },
            {
              "description": "Unsupported deletion",
              "prompt": "Delete all my notes."
            },
            {
              "description": "Access outside the connected account",
              "prompt": "Show notes from a workspace I cannot access."
            }
          ]
        },
        "demo_recording_url": "https://example.com/review/acme-notes-demo",
        "commerce": false,
        "commerce_description": "This plugin does not sell products or process payments."
      },
      "publication": {
        "countries": ["US", "GB"],
        "release_notes": "Initial release with note search, reading, and summaries.",
        "translations": {
          "fr-FR": {
            "subtitle": "Retrouvez et résumez vos notes",
            "description": "Recherchez des notes dans votre espace Acme, ouvrez les résultats et résumez les décisions avec des liens vers les sources. Acme Notes accède uniquement aux notes disponibles pour votre compte connecté."
          },
          "ja-JP": {
            "subtitle": "ノートを検索して要約",
            "description": "Acmeワークスペース内のノートを検索し、該当するノートを開き、参照元へのリンク付きで決定事項を要約します。Acme Notesは、接続されたアカウントで閲覧できるノートにのみアクセスします。"
          }
        }
      }
    }
  }
}
```

Choose the layout that matches your package:

| **Metadata**                             | **Agent Plugins: root plugin.json**                                | **Codex: .codex-plugin/plugin.json**                               |
| ---------------------------------------- | ------------------------------------------------------------------ | ------------------------------------------------------------------ |
| Package identity and publisher           | Root fields                                                        | Root fields                                                        |
| Listing text, links, prompts, and images | `extensions.com.openai.interface`                                  | interface                                                          |
| Getting started skill                    | extensions.com.openai.onboardingSkill                              | extensions.com.openai.onboardingSkill                              |
| Review and publication details           | extensions.com.openai.review and extensions.com.openai.publication | extensions.com.openai.review and extensions.com.openai.publication |

For Agent Plugins packages, put OpenAI-specific settings in `plugin.json` under `extensions.com.openai`. If that object is present, OpenAI ignores settings in `.codex-plugin/plugin.json`; the two files are not merged. If it is absent, OpenAI reads those settings from `.codex-plugin/plugin.json`. Package identity still comes from the root `plugin.json`, skills from `skills/`, and MCP servers from `mcp.json`.

Use the [complete metadata examples](#complete-metadata-examples) as a starting point. If the developer dashboard reports a missing privacy URL, support URL, or app icon, use the field reference to find the corresponding manifest field.

### Manifest fields

The requirement column distinguishes package-format requirements from submission requirements. Review details are optional in the ZIP; required materials must be present before submitting.

#### Package identity and components

These fields describe the package itself. Keep them at the root of either manifest, except where the table specifies an OpenAI extension field.

| **Field**     | **Requirement**                                     | **Value and use**                                                                                                                                                                                                                                  |
| ------------- | --------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `$schema`     | Required for Agent Plugins; omit for Codex          | Required for the portable format: https://agent-plugins.org/schemas/1.0.0/plugin.schema.json. Omit it from a standalone Codex compatibility manifest.                                                                                              |
| `name`        | Required                                            | Required stable identifier, at most 64 characters. Use lowercase letters, numbers, and single hyphens for packages you plan to submit. Keep it separate from the display name.                                                                     |
| `version`     | Required for Codex; optional in the portable schema | Release version, such as 1.0.0. Optional in the portable schema; use an explicit semantic version for submission and updates. Required in the Codex format.                                                                                        |
| `description` | Required for Codex; optional for Agent Plugins      | Package summary, at most 4000 characters. Optional in the portable schema and required in the Codex format.                                                                                                                                        |
| `author`      | Required for Codex; optional for Agent Plugins      | Publisher object with name, optional email, and optional HTTPS `url`. The portable schema allows this object to be omitted; the Codex format requires `author.name`. Use at most 120 characters for the name, 320 for email, and 2048 for the URL. |
| `homepage`    | Optional                                            | Optional HTTPS project homepage, at most 2048 characters. Set the listing’s `interface.websiteURL` separately.                                                                                                                                     |
| `repository`  | Optional                                            | Optional source repository URL.                                                                                                                                                                                                                    |
| `license`     | Optional                                            | Optional license identifier, such as MIT.                                                                                                                                                                                                          |
| `keywords`    | Optional                                            | Optional array of discovery terms.                                                                                                                                                                                                                 |
| `extensions`  | Optional                                            | Settings grouped by namespace. Put OpenAI-specific settings under `com.openai`.                                                                                                                                                                    |
| `skills`      | For Codex packages with skills                      | Codex only: a relative directory path or array of paths containing skills, such as `"./skills/"`. Portable packages discover `skills/` automatically.                                                                                              |
| `mcpServers`  | For Codex packages with MCP servers                 | Codex only: `"./.mcp.json"` for bundled MCP server configuration. Portable packages discover root `mcp.json` automatically.                                                                                                                        |

Use these additional settings inside `extensions.com.openai` for portable packages, or at the root of a Codex compatibility manifest:

| **Field**   | **Requirement**                                | **Value and use**                                                                                                                                                                |
| ----------- | ---------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `interface` | Required for Codex; optional for Agent Plugins | Presentation object described in [Listing metadata](#listing-metadata). The Codex format requires this object; portable packages can derive basic text from their root metadata. |
| `id`        | Optional                                       | Optional identity used by managed plugin catalogs. Preserve an assigned value. ZIP uploads use the dashboard’s plugin identity.                                                  |

Portable packages always discover skills in `skills/` and MCP servers in `mcp.json`. A skills or `mcpServers` declaration in the inline extension or compatibility overlay can’t replace, disable, or add to those components. Those declarations apply only to packages without a recognized portable root manifest.

#### Listing metadata

Put the following fields in `extensions.com.openai.interface` for Agent Plugins or interface for the Codex format. The limits here are for public submission; a package upload can accept longer draft text. A successful upload doesn’t mean the listing is ready to submit.

| **Field**           | **Requirement**                                          | **Type**                   | **Value and submission limit**                                                                                                           |
| ------------------- | -------------------------------------------------------- | -------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| `displayName`       | Required                                                 | String                     | Name shown to users; required, at most 30 characters.                                                                                    |
| `shortDescription`  | Required                                                 | String                     | Subtitle shown with the name; required, at most 30 characters.                                                                           |
| `longDescription`   | Required                                                 | String                     | Description of tasks, intended users, and limitations; required, at most 4000 characters.                                                |
| `developerName`     | Required                                                 | String                     | Publisher name; required, at most 80 characters. The directory name is set automatically from your selected verified developer identity. |
| `category`          | Required                                                 | String                     | Required category title from the dashboard, such as Productivity or Developer Tools.                                                     |
| `capabilities`      | Required for Codex; optional for Agent Plugins           | Array of strings           | Capability labels; at most 20, with at most 120 characters each. Required in the Codex format; use [] if there are none.                 |
| `websiteURL`        | Required for MCP review                                  | String                     | HTTPS product website, at most 1024 characters.                                                                                          |
| `supportURL`        | Required for MCP review                                  | String                     | HTTPS customer support page, at most 1024 characters.                                                                                    |
| `privacyPolicyURL`  | Required for MCP review                                  | String                     | HTTPS privacy policy, at most 1024 characters.                                                                                           |
| `termsOfServiceURL` | Required for MCP review                                  | String                     | HTTPS terms of service, at most 1024 characters.                                                                                         |
| `defaultPrompt`     | Optional                                                 | String or array of strings | Up to three starter prompts, at most 128 characters each. Make them unique and omit app @mentions. Use an array for multiple prompts.    |
| `brandColor`        | Optional                                                 | String                     | Light-theme color in #RRGGBB format, with at least 2:1 contrast against white.                                                           |
| `brandColorDark`    | Optional                                                 | String                     | Dark-theme color in #RRGGBB format, with at least 2:1 contrast against #212121. A dark color is derived if you supply only `brandColor`. |
| `composerIcon`      | Required for Codex                                       | String                     | Relative path to the icon used in the composer.                                                                                          |
| `composerIconDark`  | Optional                                                 | String                     | Optional relative path to its dark-theme variant.                                                                                        |
| `logo`              | Required for Codex; primary icon required for submission | String                     | Relative path to the primary listing icon.                                                                                               |
| `logoDark`          | Optional                                                 | String                     | Optional relative path to its dark-theme variant.                                                                                        |
| `screenshots`       | Optional                                                 | Array of strings           | Optional relative paths to screenshots.                                                                                                  |

For an attached MCP app that needs public review, all four listing URLs are required: `websiteURL`, `supportURL`, `privacyPolicyURL`, and `termsOfServiceURL`. Use HTTPS URLs without embedded credentials. Skills-only metadata validation doesn’t require all four URLs. The package’s `homepage` and `author.url` don’t fill these listing fields automatically.

#### Icons and screenshots

Include `logo` and `composerIcon` in packages you prepare for distribution. Codex package validation requires both; you can upload a portable package without them, but the dashboard requires a primary app icon before submission. Dark variants and screenshots are optional. To resolve an “App icon required” warning, add `logo` and its image file, or provide the icon in the dashboard.

Use ./-prefixed paths relative to the plugin root and include every referenced file. Supported image formats are PNG, JPEG, WebP, and SVG, at most 5 MiB each. Icons and logos must be square and at least 48 by 48 pixels. Raster images can be at most 4096 pixels in either dimension. For SVG icons, provide square numeric dimensions or a square `viewBox` of at least 48 by 48.

#### Configure onboarding, review, and publication

In both formats, put these objects directly under `extensions.com.openai`, alongside the portable format’s interface. Don’t nest them inside interface.

The optional `onboardingSkill` gives users a setup workflow to run after installation. See [Add an onboarding skill](https://developers.openai.com/plugins/build/plugins#add-an-onboarding-skill) for a manifest example, path rules, and how setup uses a new or existing conversation.

| **Field**                                       | **Requirement**                                              | **Type**         | **Value and use**                                                                                                                                                                                                              |
| ----------------------------------------------- | ------------------------------------------------------------ | ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `onboardingSkill`                               | Optional                                                     | String           | Relative path to a packaged skill’s SKILL.md, such as ./skills/get-started/SKILL.md. It must refer to an included skill.                                                                                                       |
| `review.test_cases.positive`                    | Optional in ZIP; five cases required for initial MCP review  | Array of objects | Positive review cases for a plugin with exactly one MCP server. Use the case fields that follow.                                                                                                                               |
| `review.test_cases.negative`                    | Optional in ZIP; three cases required for initial MCP review | Array of objects | Negative review cases for that server.                                                                                                                                                                                         |
| `review.demo_recording_url`                     | Optional in ZIP; required for MCP review                     | String           | Reviewer-accessible video walkthrough URL.                                                                                                                                                                                     |
| `review.commerce`                               | Optional                                                     | boolean          | Whether the app supports commerce. This declaration doesn’t accept legal terms.                                                                                                                                                |
| `review.commerce_description`                   | Optional                                                     | String           | Explanation of the app’s commerce behavior.                                                                                                                                                                                    |
| `publication.countries`                         | Optional                                                     | Array of strings | Availability allowlist of recognized uppercase country codes, such as US and GB. Omit it to preserve existing targeting; [] removes country restrictions. Applies when the plugin is published, including skills-only plugins. |
| `publication.release_notes`                     | Optional                                                     | String           | Notes describing this version’s changes.                                                                                                                                                                                       |
| `publication.translations`                      | Optional                                                     | Object or null   | Optional map of locale keys to translated listing text. See [Translate listing text](#translate-listing-text).                                                                                                                 |
| `publication.translations.<locale>.subtitle`    | Optional                                                     | String or null   | Optional translated subtitle, up to 30 characters.                                                                                                                                                                             |
| `publication.translations.<locale>.description` | Optional                                                     | String or null   | Optional translated description, up to 4000 characters.                                                                                                                                                                        |

Each object in `review.test_cases.positive` or `review.test_cases.negative` describes one test case:

| **Field**              | **Requirement**             | **Type**         | **Value and use**                                                                                                                 |
| ---------------------- | --------------------------- | ---------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| `description`          | Required                    | String           | Required description of the behavior being checked. Keep positive descriptions within 4000 characters.                            |
| `prompt`               | Required                    | String           | Required user prompt the reviewer can try.                                                                                        |
| `tools_triggered`      | Required for positive cases | String           | Expected tool names; required for positive cases at submission.                                                                   |
| `expected_behavior`    | Required for positive cases | String           | Observable expected result; required for positive cases at submission.                                                            |
| `file_attachment_urls` | Optional                    | Array of strings | Optional links to files used by the case.                                                                                         |
| `expected_output_url`  | Optional                    | String           | Optional link to an example of the expected result, such as a reference document the reviewer can compare with the actual output. |

Initial MCP app review requires exactly five positive and three negative cases. Upload accepts partial lists, so finish them before submitting. For multiple MCP servers, declare cases separately on each server in the MCP configuration; plugin-level `review.test_cases` requires exactly one server and can’t be combined with per-server case declarations. Skills-only plugins don’t need MCP app review cases or a demo recording.

Imported test cases are read-only in the dashboard: edit the package and upload it again to change them. Omitting `test_cases`, or setting it to null, preserves existing cases; `test_cases`: &#123;&#125; clears both lists. Omitting cases from a later upload doesn’t restore dashboard editing.

For the scalar review fields and `release_notes`, omission or null preserves saved values; an empty string clears text. Explicit package values are reapplied when you submit. Remove a scalar declaration from the package if you want to use an edited dashboard value. Shared review fields apply to the plugin’s own MCP app drafts. Release notes on a skills-only plugin stay in the package and don’t create an app review.

Keep commerce and `commerce_description` in review, not publication. Don’t put credentials or reviewer instructions in the package: ZIP metadata rejects `test_credentials` and `reviewer_instructions`. Enter reviewer access through the secure dashboard form.

### Translate listing text

In both formats, add a translations object under extensions.com.openai.publication to provide translated subtitles and descriptions. Use non-empty locale keys such as fr-FR or ja-JP. Each locale’s object can contain subtitle, description, or both; either field can be omitted or set to null. You can also omit translations or set it to null.

Keep English text in the base listing fields. An en-US translation isn’t required, and the importer doesn’t generate one.

Translated subtitles must be a single line of up to 30 characters. Translated descriptions can include \n line breaks and contain up to 4000 characters. Provided text must contain more than whitespace and use supported text characters; tabs and other unsupported control characters are rejected. Limits apply to the exact text, including leading and trailing spaces.

Translations are validated during import and retained in the uploaded bundle, including after metadata edits. Importing them doesn’t yet change the text shown in the Plugins Directory or listing API responses.