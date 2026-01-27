# Auto Release from CHANGELOG

解析 CHANGELOG.md 并自动创建 GitHub Release 的 Composite Action。

## 使用方式

```yaml
name: Auto Release

on:
  push:
    branches: [main]
    paths: ['CHANGELOG.md']
  workflow_dispatch:

permissions:
  contents: write

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Auto Release
        uses: wuji-technology/.github/actions/auto-release@v1
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

## 输入参数

| 参数 | 必填 | 默认值 | 说明 |
|-----|------|-------|------|
| `changelog-path` | 否 | `CHANGELOG.md` | CHANGELOG 文件路径 |
| `github-token` | 是 | - | GitHub Token |
| `draft` | 否 | `false` | 是否创建草稿 Release |
| `prerelease` | 否 | `false` | 是否标记为预发布 |

## 输出

| 输出 | 说明 |
|-----|------|
| `version` | 发布的版本号 |
| `release-url` | Release 页面 URL |

## CHANGELOG 格式要求

支持 [Keep a Changelog](https://keepachangelog.com/) 格式：

```markdown
## [1.0.0] - 2026-01-27

### Added
- 新功能 A

### Fixed
- 修复问题 B
```

## 特性

- 自动解析 CHANGELOG 中最新版本的内容
- 检查 Release 是否已存在，避免重复创建
- 支持草稿和预发布模式
