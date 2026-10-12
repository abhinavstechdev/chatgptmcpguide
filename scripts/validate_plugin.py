#!/usr/bin/env python3
"""
Validator CLI for OpenAI ChatGPT / Codex Plugins and MCP configuration.
Checks plugin manifests, schemas, limits, and submission rules against
official OpenAI Plugin Guidelines.
"""

import os
import sys
import json
import re
import argparse

if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

ALLOWED_CATEGORIES = {
    "Productivity", "Developer Tools", "Design", "Education",
    "Finance", "Lifestyle", "News", "Entertainment",
    "Utilities", "Health & Fitness", "Shopping", "Business"
}

NAME_REGEX = re.compile(r'^[a-zA-Z0-9][a-zA-Z0-9_-]{0,63}$')

def validate_plugin(plugin_dir):
    errors = []
    warnings = []

    print(f"Validating plugin at: {plugin_dir}\n")

    # 1. Check plugin.json
    manifest_path = os.path.join(plugin_dir, "plugin.json")
    compat_path = os.path.join(plugin_dir, ".codex-plugin", "plugin.json")

    active_manifest = None
    if os.path.isfile(manifest_path):
        active_manifest = manifest_path
        print("[OK] Found root plugin.json (portable format)")
    elif os.path.isfile(compat_path):
        active_manifest = compat_path
        warnings.append("Using legacy .codex-plugin/plugin.json. Consider migrating to root plugin.json with extensions.com.openai.")
    else:
        errors.append("Missing manifest: Neither plugin.json nor .codex-plugin/plugin.json was found.")
        return errors, warnings

    try:
        with open(active_manifest, "r", encoding="utf-8") as f:
            manifest = json.load(f)
    except Exception as e:
        errors.append(f"Invalid JSON in {active_manifest}: {e}")
        return errors, warnings

    # Package name
    name = manifest.get("name")
    if not name:
        errors.append("submission_name_required: Plugin 'name' is required.")
    elif not NAME_REGEX.match(name):
        errors.append(f"submission_name_invalid: Name '{name}' must start with alphanumeric, contain only alphanumeric, '-', or '_', and be <= 64 characters.")
    else:
        print(f"[OK] Package name: {name}")

    # Version
    version = manifest.get("version")
    if not version:
        errors.append("submission_version_required: Plugin 'version' is required.")
    elif len(version) > 64:
        errors.append("submission_version_too_long: Version must be <= 64 characters.")
    else:
        print(f"[OK] Version: {version}")

    # Description
    desc = manifest.get("description")
    if not desc or not desc.strip():
        errors.append("submission_description_required: Root 'description' is required.")

    # Extensions / interface validation
    oai_ext = manifest.get("extensions", {}).get("com.openai", {})
    interface = oai_ext.get("interface", {}) or manifest.get("interface", {})

    if interface:
        # Display name
        d_name = interface.get("displayName")
        if not d_name:
            errors.append("submission_display_name_required: interface.displayName is required.")
        elif "\n" in d_name:
            errors.append("submission_display_name_multiline: interface.displayName must be single-line.")
        elif len(d_name) > 30:
            errors.append(f"submission_display_name_too_long: interface.displayName ('{d_name}') is {len(d_name)} chars (max 30).")
        else:
            print(f"[OK] Display Name: {d_name} ({len(d_name)}/30 chars)")

        # Short description / Subtitle
        s_desc = interface.get("shortDescription")
        if not s_desc:
            errors.append("submission_subtitle_required: interface.shortDescription is required.")
        elif "\n" in s_desc:
            errors.append("submission_subtitle_multiline: interface.shortDescription must be single-line.")
        elif len(s_desc) > 30:
            errors.append(f"submission_subtitle_too_long: interface.shortDescription is {len(s_desc)} chars (max 30).")
        else:
            print(f"[OK] Short Description: {s_desc} ({len(s_desc)}/30 chars)")

        # Long description
        l_desc = interface.get("longDescription")
        if not l_desc:
            warnings.append("interface.longDescription is recommended for directory listings.")
        elif len(l_desc) > 4000:
            errors.append(f"submission_description_too_long: interface.longDescription is {len(l_desc)} chars (max 4000).")

        # Developer name
        dev_name = interface.get("developerName")
        if not dev_name:
            errors.append("submission_developer_name_required: interface.developerName is required.")
        elif len(dev_name) > 80:
            errors.append(f"submission_developer_name_too_long: interface.developerName is {len(dev_name)} chars (max 80).")

        # Category
        cat = interface.get("category")
        if not cat:
            errors.append("submission_category_required: interface.category is required.")
        elif cat not in ALLOWED_CATEGORIES:
            warnings.append(f"interface.category '{cat}' is not in standard list: {sorted(ALLOWED_CATEGORIES)}")

        # Starter prompts
        prompts = interface.get("defaultPrompt", [])
        if isinstance(prompts, list):
            if len(prompts) > 3:
                errors.append(f"submission_starter_prompts_exceeded: Found {len(prompts)} starter prompts (max 3 allowed).")
            seen_prompts = set()
            for p in prompts:
                if "\n" in p:
                    errors.append(f"submission_starter_prompt_multiline: Starter prompt '{p}' must be single-line.")
                if len(p) > 128:
                    errors.append(f"submission_starter_prompt_too_long: Starter prompt '{p}' is {len(p)} chars (max 128).")
                if "@" in p:
                    errors.append(f"plugin_default_prompt_mention: Starter prompt '{p}' must not contain '@' mentions.")
                if p.strip() in seen_prompts:
                    errors.append(f"plugin_default_prompt_duplicate: Duplicate starter prompt '{p}'.")
                seen_prompts.add(p.strip())
            print(f"[OK] Starter Prompts: {len(prompts)} valid prompts")

        # Capabilities
        caps = interface.get("capabilities", [])
        if isinstance(caps, list):
            if len(caps) > 20:
                errors.append(f"submission_capabilities_exceeded: Found {len(caps)} capabilities (max 20 allowed).")
            for c in caps:
                if len(c) > 120 or "\n" in c:
                    errors.append(f"plugin_capability_invalid: Capability '{c}' must be single-line and <= 120 chars.")

        # URLs
        for url_field in ["websiteURL", "privacyPolicyURL", "termsOfServiceURL"]:
            val = interface.get(url_field)
            if val:
                if not val.startswith("https://"):
                    errors.append(f"submission_url_invalid: {url_field} must use HTTPS: '{val}'")
                if len(val) > 1024:
                    errors.append(f"submission_url_too_long: {url_field} must be <= 1024 chars.")

    # 2. Check mcp.json
    mcp_path = os.path.join(plugin_dir, "mcp.json")
    if os.path.isfile(mcp_path):
        print("[OK] Found mcp.json")
        try:
            with open(mcp_path, "r", encoding="utf-8") as f:
                mcp_data = json.load(f)
            servers = mcp_data.get("mcpServers", {})
            if not servers:
                warnings.append("mcp.json has empty 'mcpServers' map.")
            for sname, sconfig in servers.items():
                stype = sconfig.get("type")
                if stype not in ["streamable-http", "sse", "stdio"]:
                    warnings.append(f"Server '{sname}' has unusual transport type: '{stype}'.")
                surl = sconfig.get("url")
                if surl and not surl.startswith("https://") and not surl.startswith("http://localhost"):
                    warnings.append(f"Server '{sname}' URL should be HTTPS in production: '{surl}'")
                auth = sconfig.get("extensions", {}).get("com.openai", {}).get("auth", {})
                if auth:
                    atype = auth.get("type")
                    if atype not in ["none", "oauth", "api_key", "mixed"]:
                        errors.append(f"Invalid auth.type '{atype}' in server '{sname}'. Must be none, oauth, api_key, or mixed.")
                    if "clientSecret" in str(auth):
                        errors.append(f"CRITICAL SECURITY: Never put clientSecret in mcp.json for server '{sname}'.")
        except Exception as e:
            errors.append(f"Invalid JSON in mcp.json: {e}")

    # 3. Check skills/
    skills_dir = os.path.join(plugin_dir, "skills")
    if os.path.isdir(skills_dir):
        skill_subdirs = [d for d in os.listdir(skills_dir) if os.path.isdir(os.path.join(skills_dir, d))]
        print(f"[OK] Found skills/ with {len(skill_subdirs)} skill(s)")
        for sname in skill_subdirs:
            skill_md = os.path.join(skills_dir, sname, "SKILL.md")
            if not os.path.isfile(skill_md):
                errors.append(f"Missing SKILL.md in skill directory: skills/{sname}")
            else:
                with open(skill_md, "r", encoding="utf-8") as sf:
                    scontent = sf.read()
                if not scontent.startswith("---"):
                    warnings.append(f"skills/{sname}/SKILL.md is missing YAML frontmatter header (---).")
                if "Claude" in scontent and "OpenAI" not in scontent:
                    warnings.append(f"skills/{sname}/SKILL.md mentions 'Claude'. Use model-neutral terms for OpenAI compatibility.")

    # Print summary
    print("\n----------------- SUMMARY -----------------")
    if errors:
        print(f"[FAIL] {len(errors)} ERROR(S) FOUND:")
        for err in errors:
            print(f"  • {err}")
    else:
        print("✅ No blocking errors found!")

    if warnings:
        print(f"\n[WARN]  {len(warnings)} WARNING(S):")
        for w in warnings:
            print(f"  • {w}")

    return errors, warnings

def main():
    parser = argparse.ArgumentParser(description="Validate an OpenAI ChatGPT/Codex Plugin")
    parser.add_argument("path", nargs="?", default=".", help="Path to plugin directory (default: current directory)")
    args = parser.parse_args()

    errors, _ = validate_plugin(os.path.abspath(args.path))
    sys.exit(1 if errors else 0)

if __name__ == '__main__':
    main()
