#!/usr/bin/env python3
"""
Fetch repository descriptions from GitHub API and update profile/README.md.
"""

import os
import re
import yaml
import requests

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
ORG_NAME = "wuji-technology"
CONFIG_PATH = "repos-config.yml"
README_PATH = "profile/README.md"


def load_config():
    """Load repository configuration from YAML file."""
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_repo_description(repo_name: str) -> str:
    """Fetch repository description from GitHub API."""
    url = f"https://api.github.com/repos/{ORG_NAME}/{repo_name}"
    headers = {"Accept": "application/vnd.github.v3+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    data = response.json()
    return data.get("description") or ""


def update_readme(descriptions: dict[str, str]) -> int:
    """Update README.md with new descriptions. Returns number of replacements made."""
    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    replacements_made = 0
    for repo_name, description in descriptions.items():
        # Match pattern: <a href=".../{repo_name}" ...> repo_name </a> <br> OLD_DESCRIPTION </td>
        # Replace OLD_DESCRIPTION with new description
        pattern = (
            rf'(<a\s+href="https://github\.com/{ORG_NAME}/{re.escape(repo_name)}"\s+target="_blank">\s*'
            rf'{re.escape(repo_name)}\s*</a>\s*<br>\s*)'
            rf'(.*?)'
            rf'(\s*</td>)'
        )

        replacement = rf'\g<1>{description} \g<3>'
        new_content, count = re.subn(pattern, replacement, content, flags=re.DOTALL | re.IGNORECASE)
        if count > 0:
            content = new_content
            replacements_made += count
        else:
            print(f"  Warning: No match found for {repo_name} in README")

    print(f"\nMade {replacements_made} replacements out of {len(descriptions)} repositories")
    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(content)

    return replacements_made


def main():
    """Main entry point: fetch descriptions and update README."""
    config = load_config()
    descriptions = {}

    # Collect all repos from config
    all_repos = []
    for category in config.get("categories", []):
        all_repos.extend(category.get("repos", []))

    print(f"Fetching descriptions for {len(all_repos)} repositories...")

    for repo_name in all_repos:
        try:
            desc = get_repo_description(repo_name)
            descriptions[repo_name] = desc
            print(f"  {repo_name}: {desc[:60]}..." if len(desc) > 60 else f"  {repo_name}: {desc}")
        except requests.RequestException as e:
            print(f"  {repo_name}: Failed to fetch - {e}")
            continue

    print(f"\nUpdating {README_PATH}...")
    update_readme(descriptions)
    print("Done!")


if __name__ == "__main__":
    main()
