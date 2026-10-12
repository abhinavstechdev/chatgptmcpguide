# ChatGPT MCP Guide Skill (`chatgptmcpguide`)

A comprehensive Antigravity / Agentic skill and reference toolkit for building **ChatGPT Plugins**, **Model Context Protocol (MCP) Servers**, and interactive **MCP Apps UI** components based on the official [OpenAI Plugins Guide](https://developers.openai.com/plugins).

---

## 📦 What's Inside

- **`SKILL.md`**: Master agent instruction guide covering architecture, decoupled UI patterns, JSON-RPC postMessage bridge, OAuth 2.1 RFC 9728 discovery, directory limits, and submission requirements.
- **`references/`**: 32 unabridged markdown files scraped directly from [developers.openai.com/plugins](https://developers.openai.com/plugins), including the master `llms-full.txt` and `reference.md`.
- **`templates/`**:
  - `manifests/`: Production-ready `plugin.json`, `mcp.json`, and `marketplace.json` catalogs.
  - `servers/typescript/`: Complete TypeScript MCP server with decoupled data & render tools.
  - `servers/python/`: Complete Python FastMCP server with tool annotations.
  - `ui/`: Production MCP Apps HTML widget with dual-protocol support (JSON-RPC over `postMessage` + `window.openai`).
  - `skills/`: Sample bundled workflow skill.
- **`scripts/`**:
  - `validate_plugin.py`: Pre-submission validation CLI that enforces OpenAI character limits, schema constraints, and safety annotations.
  - `scrape_openai_docs.py`: Automation script to re-fetch and update documentation from OpenAI.

---

## 🚀 Quick Usage

### 1. Validate a Plugin Before Submission
Check your plugin manifest, character limits, categories, and starter prompts:

```bash
python scripts/validate_plugin.py path/to/my-plugin
```

### 2. Scaffold a New Plugin
Copy the templates from `templates/manifests/`:
```bash
mkdir -p my-plugin/skills/setup
cp templates/manifests/plugin.json my-plugin/
cp templates/manifests/mcp.json my-plugin/
cp templates/skills/sample-skill/SKILL.md my-plugin/skills/setup/
```

### 3. Re-scrape or Update Documentation
To synchronize with the latest docs from OpenAI:
```bash
python scripts/scrape_openai_docs.py
```

---

## 📚 Key Technical Rules

1. **Decoupled Data vs. Render Pattern**: Always separate data query tools (which return raw `structuredContent` for model reasoning) from render tools (which attach `_meta.ui.resourceUri`).
2. **Directory Listing Limits**:
   - `displayName`: Max 30 chars, single line.
   - `shortDescription`: Max 30 chars, single line.
   - `longDescription`: Max 4,000 chars.
   - `defaultPrompt`: Max 3 prompts, <= 128 chars each, no `@mentions`.
3. **Safety Hints**: Every MCP tool must specify `readOnlyHint`, `openWorldHint`, and `destructiveHint` with justifications.
4. **Screenshots**: Allowed ONLY if the MCP server provides UI. Must be exactly 706px wide, 400–860px high.

---

## 📄 License
MIT
