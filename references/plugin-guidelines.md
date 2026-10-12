# Plugin guidelines

> For the complete documentation index, see [llms.txt](/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

These guidelines cover all plugins listed in the ChatGPT Directory, including
  MCP and skills-only plugins. Requirements specific to MCP servers, tools, and
  optional UI apply only to plugins that include those components. For the
  complete submission flow, including skills, portal steps, review, approval,
  and publishing, see [Submit plugins](https://developers.openai.com/plugins/deploy/submission).

## Overview

The plugin ecosystem is built on trust. People come to ChatGPT and Codex expecting experiences that are safe, useful, and respectful of their privacy. Developers expect a fair and transparent process. These developer guidelines set the policies every builder is expected to review and follow.

You can also read the principles in [what makes a great experience in ChatGPT](https://developers.openai.com/blog/what-makes-a-great-chatgpt-app).

The guidelines below outline the minimum standard a published plugin must meet to remain available in the universal directory shared by ChatGPT and Codex. Plugins that demonstrate strong real-world utility and high user satisfaction may be eligible for enhanced distribution opportunities, such as directory placement or proactive suggestions.

### How to use these guidelines

Start with [Plugin fundamentals](#plugin-fundamentals), which apply to every plugin. Then read [MCP requirements](#mcp-requirements) for plugins with MCP servers, tools, or optional UI, and [Skills](#skills) for plugins that include skills. If your plugin contains both MCP tools and skills, read both sections.

## Plugin fundamentals

### Purpose and originality

Plugins should serve a clear purpose and reliably do what they promise. In particular, they should provide functionality or workflows that are not natively supported by the products’ built-in capabilities and that meaningfully help satisfy common user intents expressed in conversation.

Only use intellectual property that you own or have permission to use. Do not engage in misleading or copycat designs, impersonation, spam, or static frames with no meaningful interaction. Plugins should not imply that they are made or endorsed by OpenAI.

### Quality and reliability

Plugins must behave predictably and reliably. Results should be accurate and relevant to user input. Errors, including unexpected ones, must be handled with clear messaging or fallback behaviors.

Plugins should be stable, responsive, and complete. Trial or demo plugins will not be accepted.

<a id="plugin-name-description-and-optional-screenshots"></a>

### Plugin name, description, and prompts

Plugin names and descriptions must be clear, accurate, and straightforward. Screenshots are no longer shown in the Directory, instead provide example Prompts that help users get started with your plugin.

- **Names:** Avoid overly generic names, especially single-word dictionary terms that aren’t explicitly tied to your brand. Do not append “MCP,” “MCP Server,” or “Plugin” to a company or product name.
- **Subtitles and descriptions:** Describe the plugin’s functionality without comparing it with other products, disparaging alternatives, or making unverifiable claims. Do not advertise pricing, subscriptions, free trials, discounts, or promotions.

### Safety

#### Usage policies

Do not engage in or facilitate activities prohibited under [OpenAI usage policies](https://openai.com/policies/usage-policies/). Plugins must avoid high-risk behaviors that could expose users to harm, fraud, or misuse.

Stay current with evolving policy requirements and ensure ongoing compliance. Previously approved plugins that are later found in violation may be removed.

#### Appropriateness

Plugins must be suitable for general audiences, including users aged 13–17. Plugins may not explicitly target children under 13. Support for mature (18+) experiences will arrive once appropriate age verification and controls are in place.

#### Respect user intent

Provide experiences that directly address the user’s request. Do not insert unrelated content, attempt to redirect the interaction, or collect data beyond what is reasonably necessary to fulfill the user’s request and what is consistent with your privacy policy.

Act only within the user-authorized task. Plugin and tool metadata must not seek secrets or protected context, direct unauthorized data transfers or actions, override platform instructions or safeguards, conceal behavior, or impersonate another party. Encoded or obfuscated instructions do not exempt a plugin from these requirements.

#### Fair play

Plugins must not include descriptions, titles, tool annotations, or other model-readable fields, at either the tool or plugin level, that manipulate how the model selects or uses other plugins or their tools (for example, instructing the model to prefer one plugin over others) or interfere with fair discovery. All descriptions must accurately reflect the plugin’s value without disparaging alternatives.

#### Third-party content and integrations

- **Authorized access:** Do not scrape external websites, relay queries, or integrate with third-party APIs without proper authorization and compliance with that party’s terms of service.
- **Unofficial connectors:** We cannot approve plugins that primarily function as unofficial connectors to third-party services, including pass-through intermediary software layers.
- **Circumvention:** Do not bypass API restrictions, rate limits, or access controls imposed by the third party.

### Privacy

#### Privacy policy

Plugin submissions must include a clear, published privacy policy explaining, at minimum, the categories of personal data collected, the purposes of use, the categories of recipients, data retention timelines, and any controls offered to your users. Follow this policy at all times. Users can review your privacy policy before installing the plugin.

#### Data collection

- **Collection minimization:** Gather only the minimum data required to perform the plugin’s function. Inputs should be specific, narrowly scoped, and explicitly linked to the task. Avoid “just in case” fields or broad profile data.
- **Restricted data:** Do not collect, solicit, or process the following categories of Restricted Data:
  - Information subject to Payment Card Information Data Security Standards (PCI DSS)
  - Protected health information (PHI)
  - Government identifiers (such as social security numbers)
  - Access credentials and authentication secrets (such as API keys, MFA/OTP codes, or passwords).
- **Regulated Sensitive Data:** Do not collect personal data considered “sensitive” or “special category” in the jurisdiction in which the data is collected unless collection is strictly necessary to perform the plugin’s stated function; the user has provided legally adequate consent; and the collection and use is explicitly and prominently disclosed at or before the point of collection.

#### Transparency and user control

- **Data practices:** Do not engage in surveillance, tracking, or behavioral profiling—including metadata collection such as timestamps, IP addresses, or query patterns—unless explicitly disclosed, narrowly scoped, subject to meaningful user control, and aligned with [OpenAI’s usage policies](https://openai.com/policies/usage-policies/).

### Commerce and monetization

Currently, plugins may conduct commerce only for physical goods. Selling digital products or services—including subscriptions, digital content, tokens, or credits—is not allowed, whether offered directly or indirectly (for example, through freemium upsells).

Users may sign in to an existing paid account and access features already included in their subscription. Plugins must not display subscription plans, initiate new subscriptions, or promote upgrades.

If a certain plugin feature requires a different plan or entitlement (e.g., a different subscription tier or additional credits) than the user’s, the plugin may explain that. This information should help users understand why the feature is unavailable, and should not initiate a checkout or transaction flow.

Specifically, plugins may:

- Explain that a certain feature is not available with the user’s current plan or entitlement.
- Link to an informational page describing available plans or entitlement options.

Plugins may not:

- Link directly to a checkout or other transactional page.
- Link to a page that explicitly initiates the process to upgrade, subscribe, or complete a purchase.

Plugins should provide a high quality experience in ChatGPT. If the same feature in your plugin is also available through your external website or application, you must not provide a worse version through your plugin. Plugins must not apply ChatGPT-specific fees, surcharges, or other pricing that penalizes users for accessing a service through ChatGPT. Temporary discounts and promotional offers on other platforms are permitted.

In addition, plugins may not be used to sell, promote, facilitate, or meaningfully enable the following goods or services:

#### Prohibited goods

- Adult content & sexual services
  - Pornography, explicit sexual media, live-cam services, adult subscriptions
  - Sex toys, sex dolls, BDSM gear, fetish products
- Gambling
  - Real-money gambling services, casino credits, sportsbook wagers, crypto-casino tokens
- Illegal or regulated drugs
  - Marijuana/THC products, psilocybin, illegal substances
  - CBD products exceeding legal THC limits
- Drug paraphernalia
  - Bongs, dab rigs, drug-use scales, cannabis grow equipment marketed for drugs
- Prescription & age-restricted medications
  - Prescription-only drugs (for example, insulin, antibiotics, Ozempic, opioids)
  - Age-restricted Rx products (for example, testosterone, HGH, fertility hormones)
- Illicit goods
  - Counterfeit or replica products
  - Stolen goods or items without clear provenance
  - Financial-fraud tools (skimmers, fake POS devices)
  - Piracy tools or cracked software
  - Wildlife or environmental contraband (ivory, endangered species products)
- Malware, spyware & surveillance
  - Malware, ransomware, keyloggers, stalkerware
  - Covert surveillance devices (spy cameras, IMSI catchers, hidden trackers)
- Tobacco & nicotine
  - Tobacco products
  - Nicotine products (vapes, e-liquids, nicotine pouches)
- Weapons & harmful materials
  - Firearms, ammunition, firearm parts
  - Explosives, fireworks, bomb-making materials
  - Illegal or age-restricted weapons (switchblades, brass knuckles, crossbows where banned)
  - Self-defense weapons (pepper spray, stun guns, tasers)
  - Extremist merchandise or propaganda

#### Prohibited fraudulent, deceptive, or high-risk services

- Fake IDs, forged documents, or document falsification services
- Debt relief, credit repair, or credit-score manipulation schemes
- Unregulated, deceptive, or abusive financial services
- Lending, advance-fee, or credit-building schemes designed to exploit users
- Crypto or NFT offerings involving speculation, consumer deception, or financial abuse
- Execution of money transfers, crypto transfers, or investment trades
- Government-service abuse, impersonation, or benefit manipulation
- Identity theft, impersonation, or identity-monitoring services that enable misuse
- Certain legal or quasi-legal services that facilitate fraud, evasion, or misrepresentation
- Negative-option billing, telemarketing, or consent-bypass schemes
- High-chargeback, fraud-prone, or abusive travel services

#### Checkout

Plugins should use external checkout, directing users to complete purchases on your own domain.

Instant Checkout, which is currently in beta, is currently available only to select marketplace partners and may expand to additional marketplaces and retailers over time.

Until then, standard external checkout is the required approach. No other third-party checkout solutions may be embedded or hosted within the plugin UI. To learn more, see our [docs on agentic commerce](https://developers.openai.com/commerce).

#### Advertising

Plugins must not serve advertisements and must not exist primarily as an advertising vehicle. Every plugin must deliver clear, legitimate functionality that provides standalone value to users.

### Developer verification

#### Verification

All plugin submissions must come from verified individuals or organizations. Inside the [OpenAI Platform Dashboard general settings](https://platform.openai.com/settings/organization/general), we provide a way to confirm your identity and affiliation with any business you wish to publish on behalf of. Misrepresentation, hidden behavior, or attempts to game the system may result in removal from the program.

#### Support contact details

You must provide customer support contact details where end users can reach you for help. Keep this information accurate and up to date.

## MCP requirements

These requirements apply to plugins that include MCP servers, tools, or optional UI.

### Tools

MCP tools tell ChatGPT and Codex how to use your server’s capabilities. Clear, accurate tool definitions make the plugin safer, easier for the model to understand, and easier for users to trust.

#### Clear and accurate tool names

Tool names should be human-readable, specific, and descriptive of what the tool actually does.

- Tool names must be unique within your MCP server.
- Use plain language that directly reflects the action, ideally as a verb (for example, `get_order_status`).
- Avoid misleading, overly promotional, or comparative language (for example, `pick_me`, `best`, `official`).
- Avoid internal jargon, unexplained acronyms, and opaque identifiers.

#### Descriptions that match behavior

Each tool must have a nonempty description that explicitly and accurately explains its purpose and behavior, when to use it, and any relevant limitations or side effects. Descriptions must match the tool’s schema and actual behavior. If a tool’s behavior is unclear or incomplete from its description, the plugin may be rejected.

Descriptions must not favor or disparage other plugins or services or attempt to influence the model to select them over another plugin’s tools. They must not recommend overly broad triggering beyond the explicit user intent and purpose the plugin fulfills.

#### Tool independence and exposure

Each public tool must operate independently. Do not instruct the model to invoke another plugin or connector to complete its operation; implement required dependencies within your plugin.

Expose each model-callable operation as a separate tool with a clear description, input schema, and annotations. Do not use discovery, operation selection, or schema fetching with a generic executor to enable operations not individually exposed for review.

#### Correct annotation

Set `readOnlyHint`, `destructiveHint`, and `openWorldHint` to [explicit boolean values](https://developers.openai.com/plugins/reference) (`true` or `false`) in each tool’s `annotations` object. Annotation justifications are no longer required. If our automated review flags an annotation issue, you can submit an appeal with clarification or additional information.

- `readOnlyHint`**:** Use `true` for retrieval, computation, or previews that do not modify the environment. Use `false` for external-state changes, persisting artifacts, starting stateful jobs or workflows, queuing work, or write-style outbound actions such as posting messages, sending emails, or uploading files.
- `destructiveHint`**:** Use `false` for read-only tools. For writes, use `true` for potentially destructive or irreversible effects, such as deletion, overwriting, cancellation, access revocation, or [irreversible sends or transactions](https://developers.openai.com/plugins/guides/security-privacy#prompt-injection-and-write-actions). Use `false` only for additive writes without destructive or irreversible effects. Being able to undo an action does not, by itself, justify setting `destructiveHint` to `false`.
- `openWorldHint`**:** Use `true` for public or open-ended entities, including read-only web search and arbitrary destinations. A tool confined to a bounded private account, workspace, or catalog may use `false`, even when externally hosted. Connectivity alone does not determine this value.

Annotations inform client safeguards; they do not grant permission or replace authentication, authorization and scope checks, input validation, or [human confirmation for irreversible operations](https://developers.openai.com/plugins/guides/security-privacy).

#### Minimal and purpose-driven inputs

Tools should request the minimum information necessary to complete their task.

- Input fields must be directly related to the tool’s stated purpose.
- Do not request the full conversation history, raw chat transcripts, or broad contextual fields “just in case.” A tool may request a brief, task-specific user intent field only when it meaningfully improves execution and does not expand data collection beyond what is reasonably necessary to respond to the user’s request and for the purposes described in your privacy policy.
- Do not request accumulated conversation context or prior-turn arrays.
- If needed, rely on the coarse geographic location shared by the system. Do not request precise user location data (for example, GPS coordinates or addresses).

#### Predictable, auditable behavior

Tools should behave exactly as their names, descriptions, and inputs indicate.

- Side effects should never be hidden or implicit.
- Tools should be safe to retry where possible, or explicitly indicate when retries may cause repeated effects.

Carefully designed tools help reduce surprises, protect users, and speed up the review process.

### Tool data handling

Design the input schema to limit data collection by default, rather than a funnel for optional context.

- **Response minimization:** Tool responses must return only data that is directly relevant to the user’s request and the tool’s stated purpose. Do not include diagnostic, telemetry, or internal identifiers—such as session IDs, trace IDs, request IDs, timestamps, or logging metadata—unless they are strictly required to fulfill the user’s query.
- **Data boundaries:**
  - Avoid requesting raw location fields (for example, city or coordinates) in your input schema. When location is needed, obtain it through the client’s controlled side channel (such as environment metadata or a referenced resource) so appropriate policy and consent controls can be applied. This reduces accidental PII capture, enforces least-privilege access, and keeps location handling auditable and revocable.
  - Your MCP server must not pull, reconstruct, or infer the full chat log from the client or elsewhere. Operate only on the explicit snippets and resources the client or model chooses to send. This separation can help prevent covert data expansion and keep analysis limited to intentionally shared content.
- **Action safeguards:** Follow [Correct annotation](#correct-annotation) for write and destructive-action labels, confirmations, and outbound-data safeguards.

### Authentication and permissions

If your MCP server requires authentication, the flow must be transparent and explicit. Users must be informed of all requested permissions, and those requests must be limited to what is necessary for the plugin to function.

### UI

Before getting into specifics, review the [optional UI guidelines](https://developers.openai.com/plugins/concepts/ui-guidelines) for interaction, layout, and design patterns that help plugin UI feel intuitive, trustworthy, and consistent within ChatGPT.

#### Iframes and embedded pages

Plugins with UI can embed pages from their MCP server’s own registrable domain, including full existing editors and admin interfaces. For example, a server at `https://api.example.com/mcp` can embed `https://app.example.com`: both use the registrable domain `example.com`. Separate tenants on a shared hosting service count as different domains; using the same hosting provider does not establish ownership.

Declare each required iframe origin in the resource CSP using `_meta.ui.csp.frameDomains` (or the legacy `_meta["openai/widgetCSP"].frame_domains`). For third-party domains, iframe embeds should be limited to cases where the embedded experience is essential.

You must still provide a justification when submitting a plugin that uses iframes. Explain what each embedded page does, why the plugin embeds it, and who controls its domain. Iframe use can require additional review or escalation and may lead to slower approval or rejection if the content cannot be assessed. Sharing the MCP server’s domain does not guarantee approval.

All other plugin requirements still apply to embedded pages, including the [checkout](#checkout) and [privacy](#privacy) requirements.

### Testing

Before submitting a plugin, thoroughly test its MCP server, tools, and optional UI across a wide range of scenarios.

Plugins must function reliably in ChatGPT on both desktop and mobile, including any UI components.

#### Test credentials

When submitting a plugin with an authenticated MCP server, provide a login and password for a fully featured demo account that includes sample data. Plugins that require additional login steps, such as a new account sign-up or 2FA through an inaccessible account, will be rejected.

## Skills

Skills are automatically scanned and must comply with our security, privacy, and usage policies. Plugins that contain only skills must meet all metadata and listing requirements above. Skills-only plugins may be subject to additional eligibility requirements for listing in the Directory.