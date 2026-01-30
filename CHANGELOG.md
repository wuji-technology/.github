# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

- Add Feishu notification to `centralized-release.yml` with colored status headers and repository links

## [1.0.2] - 2026-01-30

### Fixed

- Fix `parse-repos.py` to handle space-separated input (GitHub Actions converts newlines to spaces)

## [1.0.1] - 2026-01-30

### Added

- Auto-update major version tag (e.g., `v1`) when releasing patch/minor versions in `auto-release.yml`

### Fixed

- Fix multiline repository input being collapsed into single line in `centralized-release.yml`
- Fix `update-changelog.py` adding extra blank lines when inserting Unreleased section

## [1.0.0] - 2026-01-30

### Added

- `auto-release-on-pr.yml` workflow for creating tags on PR merge with `auto-release` label
- `auto-release.yml` workflow for creating GitHub Release on tag push
- Support custom CHANGELOG path in centralized release (`repo=version:changelog_path`)
- Centralized multi-version release workflow (`centralized-release.yml`)
- `parse-repos.py` script for parsing multi-line repo=version input
- `update-changelog.py` script for updating CHANGELOG with version info
- `feishu-notify.py` script for sending Feishu webhook notifications
- Feishu notification support in `auto-release` action with release notes
- `release_date` parameter for scheduling release dates
- GitHub App token authentication for better security
- `auto-release` composite action for automated GitHub Releases
- Repository README and `.gitignore`
