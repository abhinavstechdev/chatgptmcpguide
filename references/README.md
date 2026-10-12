# OpenAI Plugins and Apps Documentation Index

This directory contains the complete scraped documentation from [https://developers.openai.com/plugins](https://developers.openai.com/plugins).

## Master Documentation Sets
- [`llms-full.txt`](./llms-full.txt): Complete single-file export containing all guide sections and references.
- [`reference.md`](./reference.md): Complete schema, component bridge, and UI metadata specification.
- [`plugin-guidelines.md`](./plugin-guidelines.md): Requirements and policies for all plugins published in the ChatGPT Directory.
- [`quickstart.md`](./quickstart.md): Quickstart guide to connecting an MCP server in ChatGPT Work.
- [`siwc-full.txt`](./siwc-full.txt): Complete documentation export for Sign in with ChatGPT (SIWC).

## Core Concepts
- [`concepts/plugins.md`](./concepts/plugins.md): Architectural model: Plugins = Skills + MCP Servers + Optional UI.
- [`concepts/mcp-server.md`](./concepts/mcp-server.md): How MCP servers provide live external tool execution.
- [`concepts/skills.md`](./concepts/skills.md): How skills encode repeatable agent workflows.
- [`concepts/ui-guidelines.md`](./concepts/ui-guidelines.md): Human interface and interaction guidelines for ChatGPT UI components.

## Planning
- [`plan/use-case.md`](./plan/use-case.md): Framework for brainstorming plugin user workflows and outcomes.
- [`plan/tools.md`](./plan/tools.md): Principles for defining focused, model-friendly MCP tools.

## Building Plugins & MCP Servers
- [`build/mcp-server.md`](./build/mcp-server.md): Constructing MCP servers in TypeScript and Python FastMCP.
- [`build/app-quickstart.md`](./build/app-quickstart.md): End-to-end quickstart for MCP servers with UI.
- [`build/chatgpt-ui.md`](./build/chatgpt-ui.md): Implementing UI resources using the MCP Apps standard and bridge.
- [`build/skills.md`](./build/skills.md): Authoring skills with instructions, scripts, and evaluation criteria.
- [`build/auth.md`](./build/auth.md): Authentication guide: OAuth 2.1, PKCE, API keys, and SIWC.
- [`build/plugins.md`](./build/plugins.md): Assembling skills and MCP servers into portable Agent Plugins packages.
- [`build/extensions.md`](./build/extensions.md): Building native-feeling plugins, canvas integrations, and extensions.
- [`build/mcp-events.md`](./build/mcp-events.md): Webhooks, SSE events, and pub/sub notifications.
- [`build/monetization.md`](./build/monetization.md): Checkout API and in-chat transaction reference.
- [`build/examples.md`](./build/examples.md): Links to official OpenAI sample repositories.

## Deployment & Submission
- [`deploy/connect-chatgpt.md`](./deploy/connect-chatgpt.md): Testing MCP servers and plugins in ChatGPT Work.
- [`deploy/submission.md`](./deploy/submission.md): Packaging, uploading, and submitting to the universal directory.
- [`deploy/app-review.md`](./deploy/app-review.md): Production review requirements for remote MCP servers.
- [`deploy/submission-errors.md`](./deploy/submission-errors.md): Directory submission validation errors and error code catalog.
- [`deploy/troubleshooting.md`](./deploy/troubleshooting.md): Diagnosing MCP connection and runtime errors.

## Protocol Guides & Conversion Specs
- [`guides/product-checkout-conversion-spec.md`](./guides/product-checkout-conversion-spec.md): E-commerce purchase conversion flow specification.
- [`guides/restaurant-reservation-conversion-spec.md`](./guides/restaurant-reservation-conversion-spec.md): Table reservation flow specification.
- [`guides/local-services-request-quote-conversion-spec.md`](./guides/local-services-request-quote-conversion-spec.md): Quote-request conversion specification.
- [`guides/optimize-metadata.md`](./guides/optimize-metadata.md): Enhancing discovery and model routing via metadata.
- [`guides/security-privacy.md`](./guides/security-privacy.md): Security architecture, domain verification, and data handling.
- [`guides/submit-claude-plugin.md`](./guides/submit-claude-plugin.md): Step-by-step conversion of Claude Code plugins to OpenAI plugins.
