# .github

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Centralized GitHub configuration repository for [wuji-technology](https://github.com/wuji-technology) organization. This repository contains shared workflows, reusable actions, organization profile, and automation scripts.

## Table of Contents

- [Repository Structure](#repository-structure)
- [Features](#features)
- [Usage](#usage)
- [Contact](#contact)

## Repository Structure

```text
├── .github/
│   └── workflows/
│       ├── centralized-release.yml
│       └── update-profile.yml
├── actions/
│   └── auto-release/
├── profile/
│   └── README.md
├── scripts/
│   ├── feishu-notify.py
│   ├── parse-repos.py
│   ├── update-changelog.py
│   └── update-readme.py
├── repos-config.yml
└── README.md
```

### Directory Description

| Directory | Description |
|-----------|-------------|
| `.github/workflows/` | Organization-wide GitHub Actions workflows |
| `actions/` | Reusable composite actions for use across repositories |
| `profile/` | Organization profile README displayed on GitHub |
| `scripts/` | Python automation scripts for release and profile management |
| `repos-config.yml` | Configuration file defining public repositories |

## Features

### Centralized Release Automation

Batch release workflow that updates CHANGELOG.md and creates release PRs across multiple repositories.

```yaml
# Trigger via workflow_dispatch with:
repositories: |
  wujihandpy=1.5.0
  wujihandros2=2.0.0
```

### Auto Release Action

Reusable action that parses CHANGELOG.md and creates GitHub Releases with formatted release notes.

```yaml
- uses: wuji-technology/.github/actions/auto-release@main
  with:
    github-token: ${{ secrets.GITHUB_TOKEN }}
    feishu-webhook: ${{ secrets.FEISHU_RELEASE_WEBHOOK }}  # Optional
```

### Organization Profile

Automatically updated profile README with repository descriptions pulled from `repos-config.yml`.

## Usage

### Adding a New Public Repository

1. Add the repository to `repos-config.yml`:

```yaml
repos:
  - name: your-repo-name
    description: "Your description here."
```

2. Run the `update-profile` workflow to update the organization README.

### Creating Releases

1. Trigger `centralized-release.yml` workflow with repository and version info
2. Review and merge the generated PR
3. Release is automatically created with notes from CHANGELOG.md
4. Feishu notification is sent (if webhook configured)

## Contact

For any questions, please contact dev@wuji.tech.
