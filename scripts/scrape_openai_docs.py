#!/usr/bin/env python3
"""
Scraper script for OpenAI Plugins and Apps documentation.
Fetches all documentation pages from https://developers.openai.com/plugins
and saves them as Markdown into the references/ directory.
"""

import os
import urllib.request
import sys

URL_MAPPING = {
    'llms-full.txt': 'https://developers.openai.com/plugins/llms-full.txt',
    'reference.md': 'https://developers.openai.com/plugins/reference.md',
    'plugin-guidelines.md': 'https://developers.openai.com/plugins/plugin-guidelines.md',
    'quickstart.md': 'https://developers.openai.com/plugins/quickstart.md',
    'siwc-full.txt': 'https://developers.openai.com/siwc/llms-full.txt',
    'build/chatgpt-ui.md': 'https://developers.openai.com/plugins/build/chatgpt-ui.md',
    'build/auth.md': 'https://developers.openai.com/plugins/build/auth.md',
    'build/mcp-server.md': 'https://developers.openai.com/plugins/build/mcp-server.md',
    'build/skills.md': 'https://developers.openai.com/plugins/build/skills.md',
    'build/monetization.md': 'https://developers.openai.com/plugins/build/monetization.md',
    'build/examples.md': 'https://developers.openai.com/plugins/build/examples.md',
    'build/mcp-events.md': 'https://developers.openai.com/plugins/build/mcp-events.md',
    'build/app-quickstart.md': 'https://developers.openai.com/plugins/build/app-quickstart.md',
    'build/plugins.md': 'https://developers.openai.com/plugins/build/plugins.md',
    'build/extensions.md': 'https://developers.openai.com/plugins/build/extensions.md',
    'concepts/mcp-server.md': 'https://developers.openai.com/plugins/concepts/mcp-server.md',
    'concepts/plugins.md': 'https://developers.openai.com/plugins/concepts/plugins.md',
    'concepts/skills.md': 'https://developers.openai.com/plugins/concepts/skills.md',
    'concepts/ui-guidelines.md': 'https://developers.openai.com/plugins/concepts/ui-guidelines.md',
    'deploy/connect-chatgpt.md': 'https://developers.openai.com/plugins/deploy/connect-chatgpt.md',
    'deploy/submission-errors.md': 'https://developers.openai.com/plugins/deploy/submission-errors.md',
    'deploy/app-review.md': 'https://developers.openai.com/plugins/deploy/app-review.md',
    'deploy/troubleshooting.md': 'https://developers.openai.com/plugins/deploy/troubleshooting.md',
    'deploy/submission.md': 'https://developers.openai.com/plugins/deploy/submission.md',
    'guides/local-services-request-quote-conversion-spec.md': 'https://developers.openai.com/plugins/guides/local-services-request-quote-conversion-spec.md',
    'guides/optimize-metadata.md': 'https://developers.openai.com/plugins/guides/optimize-metadata.md',
    'guides/product-checkout-conversion-spec.md': 'https://developers.openai.com/plugins/guides/product-checkout-conversion-spec.md',
    'guides/restaurant-reservation-conversion-spec.md': 'https://developers.openai.com/plugins/guides/restaurant-reservation-conversion-spec.md',
    'guides/security-privacy.md': 'https://developers.openai.com/plugins/guides/security-privacy.md',
    'guides/submit-claude-plugin.md': 'https://developers.openai.com/plugins/guides/submit-claude-plugin.md',
    'plan/use-case.md': 'https://developers.openai.com/plugins/plan/use-case.md',
    'plan/tools.md': 'https://developers.openai.com/plugins/plan/tools.md',
}

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    references_dir = os.path.join(os.path.dirname(script_dir), 'references')
    os.makedirs(references_dir, exist_ok=True)

    print(f"Scraping OpenAI documentation to: {references_dir}")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

    success_count = 0
    total_count = len(URL_MAPPING)

    for rel_path, url in URL_MAPPING.items():
        dest = os.path.join(references_dir, rel_path.replace('/', os.sep))
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req) as resp:
                data = resp.read()
                with open(dest, 'wb') as f:
                    f.write(data)
            print(f"[OK] {rel_path} ({len(data)} bytes)")
            success_count += 1
        except Exception as e:
            print(f"[FAIL] {url} -> {e}", file=sys.stderr)

    print(f"\nDone! Scraped {success_count}/{total_count} files successfully.")

if __name__ == '__main__':
    main()
