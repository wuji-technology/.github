# Auto Release from CHANGELOG

解析 CHANGELOG.md 并自动创建 GitHub Release 的 Composite Action。

## 特性

- ✅ **分类映射**: Added→New Features, Changed→Improvements, Fixed→Bug Fixes
- ✅ **CAUTION 警告块**: Removed/Deprecated/Security 显示为警告
- ✅ **中英文支持**: 支持中文分类（新增/变更/修复/移除/废弃/安全）
- ✅ **Full Changelog 链接**: 自动生成版本对比链接
- ✅ **Upsert 模式**: 已存在的 Release 会更新而非报错
- ✅ **预发布版本支持**: 支持 `1.0.0-rc4` 格式的版本号
- ✅ **CRLF 兼容**: 自动处理 Windows 换行符

## 使用方式

```yaml
name: Auto Release

on:
  push:
    tags:
      - 'v*'

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
| `prerelease` | 否 | `true` | 是否标记为预发布 |

## 输出

| 输出 | 说明 |
|-----|------|
| `version` | 发布的版本号 |
| `release-url` | Release 页面 URL |
| `body` | 解析后的 Release Notes 内容 |
| `tag` | Git tag 名称 |

## 高级用法

### 上传 Release Assets

```yaml
- uses: wuji-technology/.github/actions/auto-release@v1
  with:
    github-token: ${{ secrets.GITHUB_TOKEN }}

- name: Upload assets
  run: gh release upload ${{ github.ref_name }} dist/*.whl dist/*.tar.gz
  env:
    GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### 同步到其他仓库

```yaml
- uses: wuji-technology/.github/actions/auto-release@v1
  id: release
  with:
    github-token: ${{ secrets.GITHUB_TOKEN }}

- name: Sync to public repo
  uses: actions/github-script@v7
  with:
    github-token: ${{ secrets.RELEASE_TOKEN }}
    script: |
      await github.rest.repos.createRelease({
        owner: context.repo.owner,
        repo: 'public-repo-name',
        tag_name: '${{ steps.release.outputs.tag }}',
        name: '${{ steps.release.outputs.tag }}',
        body: `${{ steps.release.outputs.body }}`,
        prerelease: true
      });
```

## CHANGELOG 格式要求

支持 [Keep a Changelog](https://keepachangelog.com/) 格式：

```markdown
## [1.0.0] - 2026-01-27

### Added
- 新功能 A
- 新功能 B

### Fixed
- 修复问题 A

### Removed
- 移除旧 API
```

## Release 输出示例

```markdown
## v1.0.0 (2026-01-27)

### New Features
- 新功能 A
- 新功能 B

### Bug Fixes
- 修复问题 A

> [!CAUTION]
> - **Removed**: 移除旧 API

---

**Full Changelog**: [v0.9.0...v1.0.0](https://github.com/owner/repo/compare/v0.9.0...v1.0.0)
```

## 分类映射规则

| CHANGELOG 分类 | Release 分类 | 警告 |
|---------------|-------------|------|
| Added / 新增 | New Features | - |
| Changed / 变更 | Improvements | - |
| Fixed / 修复 | Bug Fixes | - |
| Removed / 移除 | CAUTION | ⚠️ |
| Deprecated / 废弃 | CAUTION | ⚠️ |
| Security / 安全 | CAUTION | ⚠️ |
