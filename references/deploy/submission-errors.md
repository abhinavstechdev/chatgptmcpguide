# Plugin submission errors

> For the complete documentation index, see [llms.txt](/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Plugins submitted to the public directory are held to a higher standard than
plugins installed in a workspace. Directory submissions must pass the shared
package checks and the additional checks for listing fields, review materials,
MCP tools, skills, assets, and images. This reference also covers shared
package checks, such as MCP server references, that can appear outside the submission
portal.

Use the error code returned during submission to find the matching requirement.
Errors block submission. Warnings don't block submission, but you should review
them before continuing.

Non-empty values can't contain only whitespace. Supported text excludes control
characters, Unicode line or paragraph separators, and unsupported invisible
formatting characters. HTTPS URLs must include a host and contain no embedded
credentials or unsupported characters.

## Final directory submission

A package can pass upload validation and still fail final directory submission.
Final submission uses stricter listing limits and checks MCP configuration,
skill scans, test cases, and policy attestations.

| Field             | Final submission rule                                                                                                                                                                    |
| ----------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Package name      | Required; at most 64 characters. Start with an ASCII letter or digit and use only ASCII letters, digits, `_`, and `-`.                                                                   |
| Version           | Required; use a semantic version of at most 64 characters.                                                                                                                               |
| Display name      | Required; one line; at most 30 characters.                                                                                                                                               |
| Short description | Required; one line; at most 30 characters.                                                                                                                                               |
| Long description  | Required; at most 4,000 characters. Line breaks are allowed.                                                                                                                             |
| Developer name    | Required; one line; at most 80 characters.                                                                                                                                               |
| Category          | Required; choose a supported category listed in the [Listing and interface errors](#listing-and-interface-errors) section.                                                               |
| Capabilities      | At most 20. Each capability must be non-empty, one line, and at most 120 characters.                                                                                                     |
| Starter prompts   | At most 3. Each prompt must be non-empty, unique after Unicode and whitespace normalization, one line, at most 128 characters, and contain no MCP server `@mention`.                     |
| URLs              | Required for remote MCP submissions; optional for ZIP uploads, for skills-only plugins. Website, support, privacy policy, and terms URLs must use HTTPS and be at most 1,024 characters. |
| Brand colors      | Optional six-digit hex colors. The light color must have at least 2:1 contrast against white, and the dark color must have at least 2:1 contrast against `#212121`.                      |

Every plugin submission also requires:

- Passing safety and security scans for every bundled skill. Scans can take up
  to 2 hours.
- A verified developer or business identity and all required policy
  attestations.

For a remote MCP plugin, final submission also requires:

- Website, support, privacy policy, and terms URLs that meet the rules above.
- A demo-recording URL that shows the main use cases and tools across supported
  platforms.
- Exactly five positive test cases, three negative test cases, and release
  notes.
- A production HTTPS MCP server URL, a completed domain-verification challenge,
  and a successful, current tool scan.
- Explicit `readOnlyHint`, `openWorldHint`, and `destructiveHint` values and a
  justification for each value on every MCP tool.
- Reviewer-ready demo credentials when the server uses OAuth.
- Screenshots only when the MCP server provides custom UI. If you add
  screenshots, provide one PNG or JPEG image for every starter prompt. Each
  screenshot must be exactly 706 pixels wide and 400–860 pixels tall.

### Final metadata errors

In these error names, `subtitle` means short description and `description`
means long description.

| Name                                              | Requirement                                                                                             |
| ------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| `submission_display_name_required`                | Display name is required, non-empty, and single-line.                                                   |
| `submission_display_name_too_long`                | Display name must be 30 characters or fewer.                                                            |
| `submission_display_name_character_unsupported`   | Display name must use supported text and fit on one line.                                               |
| `submission_subtitle_required`                    | Short description is required, non-empty, and single-line.                                              |
| `submission_subtitle_too_long`                    | Short description must be 30 characters or fewer.                                                       |
| `submission_subtitle_character_unsupported`       | Short description must use supported text and fit on one line.                                          |
| `submission_description_required`                 | Long description is required and must be non-empty. Line breaks are allowed.                            |
| `submission_description_too_long`                 | Long description must be 4,000 characters or fewer.                                                     |
| `submission_description_character_unsupported`    | Long description must use supported text. Line breaks are allowed.                                      |
| `submission_developer_name_required`              | Developer name is required, non-empty, and single-line.                                                 |
| `submission_developer_name_too_long`              | Developer name must be 80 characters or fewer.                                                          |
| `submission_developer_name_character_unsupported` | Developer name must use supported text and fit on one line.                                             |
| `plugin_capability_invalid`                       | Each capability must be non-empty, use supported text, fit on one line, and be 120 characters or fewer. |
| `plugin_default_prompt_mention`                   | Starter prompts must not contain MCP server `@mentions`.                                                |
| `plugin_default_prompt_duplicate`                 | Starter prompts must be unique after Unicode and whitespace normalization.                              |

### MCP and review errors

These errors apply to remote MCP submissions.

| Name                                | Requirement                                                                                                                                                                       |
| ----------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `annotations_required`              | Every MCP tool must set `readOnlyHint`, `openWorldHint`, and `destructiveHint` accurately.                                                                                        |
| `justification_required`            | Every MCP tool annotation must include a justification for its read-only, open-world, or destructive behavior.                                                                    |
| `scan_required`                     | MCP tools must have a successful, current scan of the production MCP server.                                                                                                      |
| `domain_verification_required`      | The exact verification token must be hosted at the generated `/.well-known/openai-apps-challenge` URL on the MCP host or an allowed parent host, and **Verify Domain** must pass. |
| `frame_domain_explanation_required` | Every external frame domain reported by the MCP tool scan must have an explanation of why the UI needs it and what content it provides.                                           |
| `screenshots_not_allowed`           | Screenshots are allowed only when the current MCP tool scan reports a UI output template.                                                                                         |

## Archive errors

### ZIP upload errors and warnings

The portal's **Skills only** path accepts skill ZIP packages. Errors block the
upload; warnings require confirmation.

| Name                                | Requirement                                                                                                                                               |
| ----------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `plugin_name_mismatch`              | The package name in an update must match the existing plugin name.                                                                                        |
| `plugin_version_unchanged`          | A new release must use a different manifest `version`; reusing the published version requires confirmation.                                               |
| `mcp_configuration_excluded`        | Skills-only uploads exclude `mcpServers`, `mcp.json`, and `.mcp.json`. Submit a remote MCP server through **With MCP**.                                   |
| `app_configuration_excluded`        | Skills-only ZIP uploads must not include `apps` or `.app.json`; plugins with MCP servers must use **With MCP**.                                           |
| `screenshot_configuration_excluded` | Skills-only ZIP uploads must not include `interface.screenshots`; screenshots require **With MCP** and custom UI.                                         |
| `claude_format_normalized`          | `.claude-plugin/plugin.json` is converted to `.codex-plugin/plugin.json`, with missing interface defaults and normalized text fields added by the portal. |
| `manifest_normalized`               | The portal saves the normalized manifest as `.codex-plugin/plugin.json`; changed fields require confirmation.                                             |
| `developer_name_defaulted`          | The listing’s developer name is set automatically from your selected verified developer identity, regardless of the name in your ZIP.                     |

### ZIP structure and limit errors

| Name                                          | Requirement                                                                                      |
| --------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| `archive_empty`                               | Archive must not be empty.                                                                       |
| `archive_too_large`                           | Compressed ZIP must be 100 MB or less.                                                           |
| `archive_format_not_zip`                      | Archive must be a valid, uncorrupted ZIP file.                                                   |
| `archive_member_path_empty`                   | Archive entry path must not be empty.                                                            |
| `archive_member_path_has_outer_whitespace`    | Archive entry path must not begin or end with whitespace.                                        |
| `archive_member_path_has_backslash`           | Archive entry path must use `/`, not backslashes.                                                |
| `archive_member_path_absolute`                | Archive entry path must be relative to the archive root.                                         |
| `archive_member_path_has_empty_segment`       | Archive entry path must not contain empty segments.                                              |
| `archive_member_path_has_parent_segment`      | Archive entry path must not contain `..` segments.                                               |
| `archive_member_path_too_deep`                | Archive entry path must contain at most 20 segments, including the filename.                     |
| `archive_member_path_too_long`                | Archive entry path must be within the supported path-length limit.                               |
| `archive_member_path_normalization_collision` | Archive entry paths must remain unique after case and Unicode normalization.                     |
| `archive_member_type_unsupported`             | Archive entries must be regular files or directories.                                            |
| `archive_member_too_large`                    | Archive entry must not exceed 100 MiB.                                                           |
| `archive_member_path_duplicate`               | Archive entry path must be unique.                                                               |
| `archive_member_path_type_conflict`           | A file path cannot also be a directory or contain another archive entry.                         |
| `archive_too_many_entries`                    | Archive must not contain more than 5,000 entries.                                                |
| `archive_uncompressed_too_large`              | Extracted archive must not exceed 512 MiB.                                                       |
| `archive_member_unreadable`                   | Every archive entry must be readable, must not be encrypted, and must use supported compression. |

## Plugin root errors

| Name                           | Requirement                                                                                         |
| ------------------------------ | --------------------------------------------------------------------------------------------------- |
| `plugin_root_missing`          | The selected path must exist and be a directory containing a plugin.                                |
| `archive_plugin_files_missing` | A skills-only ZIP must contain a supported plugin manifest and at least one valid skill.            |
| `plugin_root_ambiguous`        | ZIP must contain exactly one plugin root, either at the archive root or in one top-level directory. |
| `plugin_root_has_siblings`     | A ZIP with a top-level plugin directory must not contain sibling files.                             |

## Plugin manifest errors

| Name                                        | Requirement                                                                                                                                                                                                            |
| ------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `plugin_manifest_missing`                   | ZIP must contain root `plugin.json` with a supported Agent Plugins schema, `.codex-plugin/plugin.json`, `.agent-plugin/plugin.json`, or `.claude-plugin/plugin.json` at the root or in its single top-level directory. |
| `plugin_manifest_not_file`                  | Plugin manifest must be a regular JSON file.                                                                                                                                                                           |
| `plugin_manifest_unreadable`                | Plugin manifest must be readable UTF-8 text.                                                                                                                                                                           |
| `plugin_manifest_json_malformed`            | Plugin manifest must contain valid JSON; malformed syntax is reported with a line number.                                                                                                                              |
| `plugin_manifest_root_not_object`           | Plugin manifest must contain a JSON object at the top level.                                                                                                                                                           |
| `codex_manifest_parent_not_directory`       | `.codex-plugin` must be a directory.                                                                                                                                                                                   |
| `codex_manifest_path_not_file`              | `.codex-plugin/plugin.json` must be a regular JSON file.                                                                                                                                                               |
| `plugin_id_wrong_type`                      | `id` must be a string when provided.                                                                                                                                                                                   |
| `plugin_id_empty`                           | `id` must be non-empty when provided.                                                                                                                                                                                  |
| `plugin_name_missing`                       | `name` is required.                                                                                                                                                                                                    |
| `plugin_name_wrong_type`                    | `name` must be a string.                                                                                                                                                                                               |
| `plugin_name_empty`                         | `name` must be non-empty.                                                                                                                                                                                              |
| `plugin_name_too_long`                      | `name` must be 64 characters or fewer.                                                                                                                                                                                 |
| `plugin_name_format`                        | `name` must start with an ASCII letter or digit and contain only ASCII letters, digits, `_`, or `-`.                                                                                                                   |
| `plugin_version_missing`                    | `version` is required.                                                                                                                                                                                                 |
| `plugin_version_wrong_type`                 | `version` must be a string.                                                                                                                                                                                            |
| `plugin_version_empty`                      | `version` must be a non-empty semantic-version string, such as `1.0.0`.                                                                                                                                                |
| `plugin_version_not_semver`                 | `version` must use semantic versioning, such as `1.0.0`.                                                                                                                                                               |
| `plugin_version_too_long`                   | `version` must be 64 characters or fewer.                                                                                                                                                                              |
| `plugin_description_missing`                | `description` is required.                                                                                                                                                                                             |
| `plugin_description_wrong_type`             | `description` must be a string.                                                                                                                                                                                        |
| `plugin_description_empty`                  | `description` must be non-empty.                                                                                                                                                                                       |
| `plugin_description_too_long`               | `description` must be 1,024 characters or fewer.                                                                                                                                                                       |
| `plugin_description_character_unsupported`  | `description` must use supported text. Line breaks are allowed.                                                                                                                                                        |
| `plugin_developer_missing`                  | `author.name` is required. `interface.developerName` is also required and is reported separately.                                                                                                                      |
| `plugin_author_wrong_type`                  | `author` must be an object.                                                                                                                                                                                            |
| `plugin_author_name_wrong_type`             | `author.name` must be a string.                                                                                                                                                                                        |
| `plugin_author_name_empty`                  | `author.name` must be non-empty.                                                                                                                                                                                       |
| `plugin_author_name_too_long`               | `author.name` must be 120 characters or fewer.                                                                                                                                                                         |
| `plugin_author_name_character_unsupported`  | `author.name` must use supported text.                                                                                                                                                                                 |
| `plugin_author_email_wrong_type`            | `author.email` must be a string when provided.                                                                                                                                                                         |
| `plugin_author_email_empty`                 | `author.email` must be non-empty when provided.                                                                                                                                                                        |
| `plugin_author_email_too_long`              | `author.email` must be 320 characters or fewer.                                                                                                                                                                        |
| `plugin_author_email_character_unsupported` | `author.email` must use supported text.                                                                                                                                                                                |
| `plugin_author_url_wrong_type`              | `author.url` must be a string when provided.                                                                                                                                                                           |
| `plugin_author_url_empty`                   | `author.url` must be non-empty when provided.                                                                                                                                                                          |
| `plugin_author_url_not_https`               | `author.url` must be an HTTPS URL.                                                                                                                                                                                     |
| `plugin_author_url_has_credentials`         | `author.url` must not contain credentials.                                                                                                                                                                             |
| `plugin_author_url_too_long`                | `author.url` must be 2,048 characters or fewer.                                                                                                                                                                        |
| `plugin_author_url_character_unsupported`   | `author.url` must use supported text.                                                                                                                                                                                  |

## Listing and interface errors

The plugin manifest's `interface` object defines the public listing shown to
users. It lives in `.codex-plugin/plugin.json` and uses fields such as
`displayName` and `shortDescription`:

```json
{
  "interface": {
    "displayName": "Example Plugin",
    "shortDescription": "Summarize documents",
    "longDescription": "Summarize and organize documents.",
    "developerName": "Example",
    "category": "Productivity",
    "capabilities": ["Summarize documents"]
  }
}
```

The four listing URLs (website, privacy policy, terms, and support) are
optional for ZIP uploads, for skills-only
plugins. They are required for remote MCP submissions. Their length limit is
2,048 characters for package validation and 1,024 characters for final
directory submission.

| Name                                             | Requirement                                                                                                                                                                                                                                     |
| ------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `plugin_interface_wrong_type`                    | The plugin manifest's `interface` field must be a JSON object.                                                                                                                                                                                  |
| `plugin_display_name_wrong_type`                 | `interface.displayName` must be a string.                                                                                                                                                                                                       |
| `plugin_display_name_empty`                      | `interface.displayName` is required and must be non-empty.                                                                                                                                                                                      |
| `plugin_display_name_too_long`                   | `interface.displayName` must be 80 characters or fewer for package validation and 30 characters or fewer for final directory submission.                                                                                                        |
| `plugin_display_name_character_unsupported`      | `interface.displayName` must use supported text.                                                                                                                                                                                                |
| `plugin_short_description_missing`               | `interface.shortDescription` is required, must fit on one line, and must be 240 characters or fewer for package validation and 30 characters or fewer for final directory submission.                                                           |
| `plugin_short_description_wrong_type`            | `interface.shortDescription` must be a string.                                                                                                                                                                                                  |
| `plugin_short_description_empty`                 | `interface.shortDescription` must be non-empty.                                                                                                                                                                                                 |
| `plugin_short_description_too_long`              | `interface.shortDescription` must be 240 characters or fewer for package validation and 30 characters or fewer for final directory submission.                                                                                                  |
| `plugin_short_description_character_unsupported` | `interface.shortDescription` must use supported text.                                                                                                                                                                                           |
| `plugin_long_description_wrong_type`             | `interface.longDescription` must be a string.                                                                                                                                                                                                   |
| `plugin_long_description_empty`                  | `interface.longDescription` is required and must be non-empty.                                                                                                                                                                                  |
| `plugin_long_description_too_long`               | `interface.longDescription` must be 4,000 characters or fewer.                                                                                                                                                                                  |
| `plugin_long_description_character_unsupported`  | `interface.longDescription` must use supported text. Line breaks are allowed.                                                                                                                                                                   |
| `plugin_developer_name_wrong_type`               | `interface.developerName` must be a string.                                                                                                                                                                                                     |
| `plugin_developer_name_empty`                    | `interface.developerName` is required and must be non-empty.                                                                                                                                                                                    |
| `plugin_developer_name_too_long`                 | `interface.developerName` must be 120 characters or fewer for package validation and 80 characters or fewer for final directory submission.                                                                                                     |
| `plugin_developer_name_character_unsupported`    | `interface.developerName` must use supported text.                                                                                                                                                                                              |
| `plugin_category_wrong_type`                     | `interface.category` must be a string.                                                                                                                                                                                                          |
| `plugin_category_empty`                          | `interface.category` must be non-empty when provided; omit it to use `Other`.                                                                                                                                                                   |
| `plugin_category_unknown`                        | `interface.category` must be `Productivity`, `Creativity`, `Developer Tools`, `Business & Operations`, `Data & Analytics`, `Communication`, `Education & Research`, `Security`, `Finance`, `Healthcare`, `Travel`, `Entertainment`, or `Other`. |
| `plugin_category_character_unsupported`          | `interface.category` must use supported text.                                                                                                                                                                                                   |
| `plugin_capabilities_wrong_type`                 | `interface.capabilities` must be a list of strings.                                                                                                                                                                                             |
| `plugin_capabilities_too_many`                   | `interface.capabilities` must contain 20 entries or fewer.                                                                                                                                                                                      |
| `plugin_capability_wrong_type`                   | Each `interface.capabilities` entry must be a string.                                                                                                                                                                                           |
| `plugin_capability_empty`                        | Each `interface.capabilities` entry must be non-empty when provided.                                                                                                                                                                            |
| `plugin_capability_too_long`                     | Each `interface.capabilities` entry must be 120 characters or fewer.                                                                                                                                                                            |
| `plugin_capability_character_unsupported`        | Each `interface.capabilities` entry must use supported text.                                                                                                                                                                                    |
| `plugin_website_url_wrong_type`                  | `interface.websiteURL` must be a string when provided.                                                                                                                                                                                          |
| `plugin_website_url_empty`                       | `interface.websiteURL` must be non-empty when provided.                                                                                                                                                                                         |
| `plugin_website_url_format`                      | `interface.websiteURL` must be an HTTPS URL.                                                                                                                                                                                                    |
| `plugin_website_url_too_long`                    | `interface.websiteURL` must meet the listing URL length limits.                                                                                                                                                                                 |
| `plugin_privacy_policy_url_wrong_type`           | `interface.privacyPolicyURL` must be a string when provided.                                                                                                                                                                                    |
| `plugin_privacy_policy_url_empty`                | `interface.privacyPolicyURL` must be non-empty when provided.                                                                                                                                                                                   |
| `plugin_privacy_policy_url_format`               | `interface.privacyPolicyURL` must be an HTTPS URL.                                                                                                                                                                                              |
| `plugin_privacy_policy_url_too_long`             | `interface.privacyPolicyURL` must meet the listing URL length limits.                                                                                                                                                                           |
| `plugin_terms_of_service_url_wrong_type`         | `interface.termsOfServiceURL` must be a string when provided.                                                                                                                                                                                   |
| `plugin_terms_of_service_url_empty`              | `interface.termsOfServiceURL` must be non-empty when provided.                                                                                                                                                                                  |
| `plugin_terms_of_service_url_format`             | `interface.termsOfServiceURL` must be an HTTPS URL.                                                                                                                                                                                             |
| `plugin_terms_of_service_url_too_long`           | `interface.termsOfServiceURL` must meet the listing URL length limits.                                                                                                                                                                          |
| `plugin_support_url_wrong_type`                  | `interface.supportURL` must be a string when provided.                                                                                                                                                                                          |
| `plugin_support_url_empty`                       | `interface.supportURL` must be non-empty when provided.                                                                                                                                                                                         |
| `plugin_support_url_format`                      | `interface.supportURL` must be an HTTPS URL.                                                                                                                                                                                                    |
| `plugin_support_url_too_long`                    | `interface.supportURL` must meet the listing URL length limits.                                                                                                                                                                                 |
| `plugin_homepage_wrong_type`                     | `homepage` must be a string when provided.                                                                                                                                                                                                      |
| `plugin_homepage_empty`                          | `homepage` must be non-empty when provided.                                                                                                                                                                                                     |
| `plugin_homepage_format`                         | `homepage` must be an HTTPS URL.                                                                                                                                                                                                                |
| `plugin_homepage_too_long`                       | `homepage` must be 2,048 characters or fewer.                                                                                                                                                                                                   |
| `plugin_brand_color_wrong_type`                  | `interface.brandColor` must be a string when provided.                                                                                                                                                                                          |
| `plugin_brand_color_empty`                       | `interface.brandColor` must be non-empty when provided.                                                                                                                                                                                         |
| `plugin_brand_color_format`                      | `interface.brandColor` must be a six-digit hex color, such as `#1ABCFE`.                                                                                                                                                                        |
| `plugin_brand_color_dark_wrong_type`             | `interface.brandColorDark` must be a string when provided.                                                                                                                                                                                      |
| `plugin_brand_color_dark_empty`                  | `interface.brandColorDark` must be non-empty when provided.                                                                                                                                                                                     |
| `plugin_brand_color_dark_format`                 | `interface.brandColorDark` must be a six-digit hex color, such as `#1ABCFE`.                                                                                                                                                                    |
| `plugin_brand_color_contrast`                    | `interface.brandColor` must have at least 2:1 contrast against white.                                                                                                                                                                           |
| `plugin_brand_color_dark_contrast`               | `interface.brandColorDark` must have at least 2:1 contrast against `#212121`.                                                                                                                                                                   |
| `plugin_default_prompt_wrong_type`               | `interface.defaultPrompt` must be a string or list of strings.                                                                                                                                                                                  |
| `plugin_default_prompt_too_many`                 | `interface.defaultPrompt` must contain at most three prompts.                                                                                                                                                                                   |
| `plugin_default_prompt_entry_wrong_type`         | Each `interface.defaultPrompt` entry must be a string.                                                                                                                                                                                          |
| `plugin_default_prompt_empty`                    | Each `interface.defaultPrompt` entry must be non-empty when provided.                                                                                                                                                                           |
| `plugin_default_prompt_too_long`                 | Each `interface.defaultPrompt` entry must be 512 characters or fewer for package validation and 128 characters or fewer for final directory submission.                                                                                         |
| `plugin_default_prompt_character_unsupported`    | Each `interface.defaultPrompt` entry must use supported text and fit on one line.                                                                                                                                                               |

## Plugin content errors

| Name                               | Requirement                                                                                                                      |
| ---------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| `plugin_skills_path_wrong_type`    | `skills` must be a string path for the root `skills/` directory.                                                                 |
| `plugin_skills_path_empty`         | `skills` must be a non-empty path to the root `skills/` directory when provided.                                                 |
| `plugin_skills_path_unsupported`   | `skills` must resolve to the root `skills/` directory.                                                                           |
| `plugin_skills_directory_missing`  | A declared root `skills/` directory must exist.                                                                                  |
| `plugin_skills_path_not_directory` | Root `skills/` must be a directory when declared.                                                                                |
| `plugin_apps_path_wrong_type`      | `apps` must be a string path for the root `.app.json`.                                                                           |
| `plugin_apps_path_empty`           | `apps` must be a non-empty path to the root `.app.json` when provided.                                                           |
| `plugin_apps_path_unsupported`     | `apps` must resolve to the root `.app.json`.                                                                                     |
| `plugin_apps_file_missing`         | A declared root `.app.json` file must exist.                                                                                     |
| `plugin_apps_path_not_file`        | Root `.app.json` must be a regular file when declared.                                                                           |
| `plugin_mcp_path_wrong_type`       | `mcpServers` must be a string path for the root `.mcp.json`.                                                                     |
| `plugin_mcp_path_empty`            | `mcpServers` must be a nonempty path. Set it to `./.mcp.json` or remove the field.                                               |
| `plugin_mcp_path_unsupported`      | `mcpServers` must resolve to the root `.mcp.json`.                                                                               |
| `plugin_mcp_file_missing`          | `mcpServers` declares the root `.mcp.json`, but that file doesn't exist.                                                         |
| `plugin_mcp_path_not_file`         | Root `.mcp.json` must be a regular file.                                                                                         |
| `plugin_runtime_surface_missing`   | A skills-only ZIP must contain at least one valid skill. Local and workspace packages can also reference an eligible MCP server. |

## MCP manifest errors

These errors apply to the compatibility `.mcp.json` file. For portable packages,
ingestion derives this file and `.codex-plugin/plugin.json` from root
`plugin.json` and `mcp.json`. The component-path errors above can also refer to
these generated files. Fix the source portable configuration; don't rename
`mcp.json` to `.mcp.json` just because a compatibility diagnostic names it.

| Name                          | Requirement                                                                                   |
| ----------------------------- | --------------------------------------------------------------------------------------------- |
| `mcp_manifest_unreadable`     | `.mcp.json` must be readable UTF-8 text.                                                      |
| `mcp_manifest_json_malformed` | `.mcp.json` must contain valid JSON; malformed syntax is reported with a line number.         |
| `mcp_manifest_wrong_type`     | `.mcp.json` must contain a JSON object at the top level.                                      |
| `mcp_servers_missing`         | `.mcp.json` must contain the top-level `mcpServers` field.                                    |
| `mcp_servers_wrong_type`      | `mcpServers` must be an object.                                                               |
| `mcp_server_name_empty`       | Every MCP server name must contain at least one non-whitespace character.                     |
| `mcp_server_wrong_type`       | Each `mcpServers.<server-name>` value must be an object containing that server's declaration. |

## Skill errors

| Name                                      | Requirement                                                                                   |
| ----------------------------------------- | --------------------------------------------------------------------------------------------- |
| `skill_manifest_missing`                  | Skill must contain a `SKILL.md` file.                                                         |
| `skill_bundle_too_large`                  | Each compressed skill bundle must be within the MiB limit reported in the error.              |
| `skill_directory_hidden`                  | Skill directory names must not begin with `.`.                                                |
| `skill_manifest_nested`                   | Each skill directory must be an immediate child of `skills/`.                                 |
| `skill_manifest_not_regular_file`         | `SKILL.md` must be a regular file.                                                            |
| `skill_manifest_unreadable`               | `SKILL.md` must be readable.                                                                  |
| `skill_manifest_invalid_utf8`             | `SKILL.md` must contain valid UTF-8.                                                          |
| `skill_frontmatter_missing`               | `SKILL.md` must start with YAML front matter between `---` lines.                             |
| `skill_frontmatter_unclosed`              | `SKILL.md` YAML front matter must end with `---`.                                             |
| `skill_frontmatter_yaml_malformed`        | `SKILL.md` front matter must contain valid YAML.                                              |
| `skill_frontmatter_wrong_type`            | `SKILL.md` front matter must contain a YAML mapping.                                          |
| `skill_name_missing`                      | `name` is required and must not be empty.                                                     |
| `skill_name_wrong_type`                   | `name` must be a string.                                                                      |
| `skill_name_empty`                        | `name` must be non-empty.                                                                     |
| `skill_name_character_unsupported`        | Skill front matter `name` must use supported text.                                            |
| `skill_description_missing`               | `description` is required and must not be empty.                                              |
| `skill_description_wrong_type`            | `description` must be a string.                                                               |
| `skill_description_empty`                 | `description` must be non-empty.                                                              |
| `skill_description_too_long`              | `description` must be 1,024 characters or fewer.                                              |
| `skill_description_character_unsupported` | Skill front matter `description` must use supported text.                                     |
| `skill_body_empty`                        | Skill instructions must not be empty.                                                         |
| `skill_identity_too_long`                 | The combined plugin and skill name (`plugin-name:skill-name`) must be 64 characters or fewer. |
| `skill_identity_duplicate`                | Each skill `name` must be unique within the plugin.                                           |

## Skill agent metadata errors

A bundled skill can define its own `interface` in
`skills/<skill>/agents/openai.yaml`. This controls how the skill appears to
users and is separate from the plugin manifest's `interface`. Skill interface
fields use snake_case:

```yaml
interface:
  display_name: "Summarize documents"
  short_description: "Summarize a document"
  icon_small: "./assets/icon.png"
  default_prompt: "Summarize the selected document."
```

| Name                                               | Requirement                                                                                                                                                                        |
| -------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `skill_agent_not_regular_file`                     | `agents/openai.yaml` must be a regular file.                                                                                                                                       |
| `skill_agent_unreadable`                           | `agents/openai.yaml` must be readable.                                                                                                                                             |
| `skill_agent_invalid_utf8`                         | `agents/openai.yaml` must contain valid UTF-8.                                                                                                                                     |
| `skill_agent_yaml_malformed`                       | `agents/openai.yaml` must contain valid YAML.                                                                                                                                      |
| `skill_agent_top_level_wrong_type`                 | `agents/openai.yaml` must contain a YAML mapping at the top level.                                                                                                                 |
| `skill_agent_interface_missing`                    | `interface` is required in `agents/openai.yaml` when that file is included.                                                                                                        |
| `skill_agent_interface_wrong_type`                 | `interface` in `agents/openai.yaml` must be a YAML mapping.                                                                                                                        |
| `skill_agent_display_name_missing`                 | `interface.display_name` is required and must not be empty.                                                                                                                        |
| `skill_agent_display_name_wrong_type`              | `interface.display_name` must be a string.                                                                                                                                         |
| `skill_agent_display_name_empty`                   | `interface.display_name` must not be empty.                                                                                                                                        |
| `skill_agent_short_description_missing`            | `interface.short_description` is required and must not be empty.                                                                                                                   |
| `skill_agent_short_description_wrong_type`         | `interface.short_description` must be a string.                                                                                                                                    |
| `skill_agent_short_description_empty`              | `interface.short_description` must not be empty.                                                                                                                                   |
| `skill_agent_icon_small_wrong_type`                | `interface.icon_small` must be a non-empty relative file path when provided.                                                                                                       |
| `skill_agent_icon_small_empty`                     | `interface.icon_small` must be a non-empty relative file path when provided, such as `assets/icon.png`.                                                                            |
| `skill_agent_icon_large_wrong_type`                | `interface.icon_large` must be a non-empty relative file path when provided.                                                                                                       |
| `skill_agent_icon_large_empty`                     | `interface.icon_large` must be a non-empty relative file path when provided, such as `assets/icon.png`.                                                                            |
| `skill_agent_brand_color_wrong_type`               | `interface.brand_color` must be a string when provided.                                                                                                                            |
| `skill_agent_brand_color_empty`                    | `interface.brand_color` must be a non-empty six-digit hex color when provided, such as `#1ABCFE`.                                                                                  |
| `skill_agent_brand_color_format`                   | `interface.brand_color` must be a six-digit hex color, such as `#1ABCFE`.                                                                                                          |
| `skill_agent_default_prompt_wrong_type`            | `interface.default_prompt` must be a string when provided.                                                                                                                         |
| `skill_agent_default_prompt_empty`                 | `interface.default_prompt` must be non-empty when provided.                                                                                                                        |
| `skill_agent_policy_wrong_type`                    | `policy` must be a YAML mapping when provided.                                                                                                                                     |
| `skill_agent_allow_implicit_invocation_wrong_type` | `policy` may contain only `products` and `allow_implicit_invocation`. `products` must contain `CHAT`, `CODEX`, or both, and `allow_implicit_invocation` must be `true` or `false`. |
| `skill_agent_dependencies_wrong_type`              | `dependencies` must be a YAML mapping; only `tools` is supported.                                                                                                                  |
| `skill_agent_dependency_unsupported`               | Only `dependencies.tools` is supported in `agents/openai.yaml`.                                                                                                                    |

## Asset path errors

| Name                                        | Requirement                                                                                                                                     |
| ------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| `declared_asset_path_wrong_type`            | The named asset field must be a file path string.                                                                                               |
| `declared_asset_path_empty`                 | The named asset field must not be empty.                                                                                                        |
| `declared_asset_path_has_outer_whitespace`  | The named asset field must not begin or end with whitespace.                                                                                    |
| `declared_asset_path_has_control_character` | The named asset field must not contain characters U+0000–U+001F or U+007F.                                                                      |
| `branding_asset_path_missing_root_prefix`   | The named asset field must start with `./`.                                                                                                     |
| `declared_asset_path_unsafe`                | The named asset field must be a relative path inside the plugin and must not contain an absolute path, drive prefix, or `..` traversal segment. |
| `declared_asset_path_outside_package`       | The named asset field must reference a file inside the plugin.                                                                                  |
| `declared_asset_file_missing`               | The named asset field references a file that does not exist.                                                                                    |
| `declared_asset_not_regular_file`           | The named asset field must reference a file, not a directory or special file.                                                                   |

## Image errors

Directory branding images must use a supported file type and meet the size and
dimension limits below. These rules apply to packaged branding assets;
starter-prompt screenshots use the separate portal limits listed above.

| Name                                      | Requirement                                                                |
| ----------------------------------------- | -------------------------------------------------------------------------- |
| `plugin_logo_path_missing`                | `interface.logo` is required and must reference a square image.            |
| `plugin_composer_icon_path_missing`       | `interface.composerIcon` is required and must reference a square image.    |
| `image_file_unreadable`                   | Image file must be readable.                                               |
| `image_file_too_large`                    | Image must not exceed 5 MiB.                                               |
| `image_file_format_unsupported`           | Image filename must end in `.png`, `.jpg`, `.jpeg`, `.webp`, or `.svg`.    |
| `raster_image_decode_failed`              | Raster image must be a PNG, JPEG, or WebP file that can be decoded safely. |
| `raster_image_extension_content_mismatch` | Image filename extension must match the detected image format.             |
| `raster_image_not_square`                 | Image must be square.                                                      |
| `raster_image_dimensions_too_small`       | Image dimensions must be at least 48×48 pixels.                            |
| `raster_image_dimensions_too_large`       | Image dimensions must not exceed 4,096×4,096 pixels.                       |
| `svg_xml_malformed`                       | SVG must contain valid UTF-8 XML.                                          |
| `svg_root_element_invalid`                | SVG root element must be `<svg>`.                                          |
| `svg_dimensions_missing`                  | SVG must define a numeric `viewBox` or numeric `width` and `height`.       |
| `svg_dimensions_not_numeric`              | SVG dimensions must be numeric and omit units and percentages.             |
| `svg_dimensions_not_positive`             | SVG width and height must be positive finite numbers.                      |
| `svg_dimensions_not_square`               | SVG dimensions must be square.                                             |
| `svg_dimensions_too_small`                | SVG dimensions must be at least 48×48 pixels.                              |

<a id="app-reference-errors"></a>

## MCP server reference errors

The shared package checks validate `.app.json` when a plugin references
registered MCP servers. The submission portal doesn't publish references to
existing integrations. A **Skills only** upload removes `.app.json`. Use
**With MCP** to submit the MCP server directly.

For local or workspace packages, the top-level `apps` object maps each MCP
server alias to a registered server entry. These configuration names and error
codes retain their literal `app` spelling.

| Name                            | Requirement                                                                                                                                                         |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `app_manifest_unreadable`       | `.app.json` must be readable UTF-8 text.                                                                                                                            |
| `app_manifest_json_malformed`   | `.app.json` contains malformed JSON near the reported line.                                                                                                         |
| `app_manifest_wrong_type`       | `.app.json` must contain a JSON object at the top level.                                                                                                            |
| `app_entries_missing`           | `apps` is required.                                                                                                                                                 |
| `app_entries_wrong_type`        | `apps` must be an object.                                                                                                                                           |
| `app_entry_wrong_type`          | Each server entry must be an object.                                                                                                                                |
| `app_id_missing`                | Each server entry's `id` is required.                                                                                                                               |
| `app_id_wrong_type`             | Each server entry's `id` must be a string.                                                                                                                          |
| `app_id_format`                 | Each server entry's `id` must begin with `asdk_app_`, `connector_`, or `templated_apps_`, followed by a letter or digit and then only letters, digits, `_`, or `-`. |
| `app_entry_optional_wrong_type` | Each server entry's `optional` value must be `true` or `false` when provided.                                                                                       |
| `app_entry_required_wrong_type` | Each server entry's `required` value must be `true` or `false` when provided.                                                                                       |
| `app_not_eligible`              | A local or workspace package must reference an eligible, available MCP server. Directory submissions must use **With MCP** and submit the MCP server directly.      |

## Package warnings

These warnings identify package content that validation ignores or normalizes.
They don't block submission. Review them to confirm the submitted plugin
contains the expected files and settings.

| Name                              | Requirement                                                                                                                                  |
| --------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| `duplicate_app_reference`         | Each server ID in `.app.json` must be referenced once; duplicate references are treated as one server.                                       |
| `undeclared_app_manifest_ignored` | A root `.app.json` is imported only when the plugin-manifest `apps` field is set to `./.app.json`.                                           |
| `undeclared_mcp_manifest_ignored` | A root `.mcp.json` is imported only when the plugin-manifest `mcpServers` field is set to `./.mcp.json`.                                     |
| `skill_file_ignored`              | Files directly under `skills/` aren't imported as skills; each skill must be in a directory containing `SKILL.md`.                           |
| `skill_symlink_ignored`           | Symbolic links directly under `skills/` aren't imported as skills; each skill must be a real directory containing `SKILL.md`.                |
| `skill_frontmatter_adjusted`      | Skill `name` and `description` are normalized during import by trimming outer whitespace and collapsing internal whitespace.                 |
| `skill_metadata_ignored`          | Skill interface settings must use the `interface` mapping in `agents/openai.yaml`; `metadata` in `SKILL.md` doesn't configure the interface. |

## Next steps

After resolving all validation errors, return to
[Submit plugins](https://developers.openai.com/plugins/deploy/submission) to complete the submission.