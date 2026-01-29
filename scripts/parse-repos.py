#!/usr/bin/env python3
"""
解析多行文本格式的仓库版本配置

格式: repo=version 或 repo=version:changelog_path，每行一个
示例:
    wujihandpy=1.5.0
    wuji-retargeting-private=0.2.0:public/CHANGELOG.md
"""
import json
import re
import sys
from pathlib import PurePosixPath


def parse_repos(input_text):
    """
    解析格式: repo1=1.5.0\nrepo2=2.0.0:public/CHANGELOG.md
    返回: [{"repo": "repo1", "version": "1.5.0", "changelog_path": "CHANGELOG.md"}, ...]
    """
    result = []

    for line_num, line in enumerate(input_text.strip().split('\n'), 1):
        line = line.strip()

        # 跳过空行和注释
        if not line or line.startswith('#'):
            continue

        # 匹配 repo=version（支持点号，如 .github）
        match = re.match(r'^([a-zA-Z0-9_.-]+)\s*=\s*(.+)$', line)
        if not match:
            raise ValueError(f"第 {line_num} 行格式错误: {line}\n正确格式: repo=version")

        repo, value = match.groups()
        value = value.strip()

        # 拆分 version 和可选的 changelog_path
        if ':' in value:
            version, changelog_path = value.split(':', 1)
            version = version.strip()
            changelog_path = changelog_path.strip()
        else:
            version = value
            changelog_path = "CHANGELOG.md"

        # 验证版本号格式 (X.Y.Z 或 X.Y.Z-suffix)
        if not re.match(r'^\d+\.\d+\.\d+(-[a-zA-Z0-9.]+)?$', version):
            raise ValueError(
                f"第 {line_num} 行版本号格式错误: {version}\n"
                f"正确格式: X.Y.Z 或 X.Y.Z-suffix (如 1.5.0 或 1.5.0-hotfix.1)"
            )

        # 验证 changelog_path
        path = PurePosixPath(changelog_path)
        if path.is_absolute() or ".." in path.parts:
            raise ValueError(f"第 {line_num} 行 CHANGELOG 路径必须为仓库内相对路径且不得包含 .. : {changelog_path}")
        if not changelog_path.endswith('.md'):
            raise ValueError(f"第 {line_num} 行 CHANGELOG 路径必须以 .md 结尾: {changelog_path}")

        result.append({"repo": repo.strip(), "version": version, "changelog_path": changelog_path})

    if not result:
        raise ValueError("未找到有效的仓库配置，请至少提供一个 repo=version 行")

    # 检查重复仓库
    repo_names = [item["repo"] for item in result]
    duplicates = set([x for x in repo_names if repo_names.count(x) > 1])
    if duplicates:
        raise ValueError(f"仓库名重复: {', '.join(duplicates)}")

    # 限制最多 10 个仓库
    if len(result) > 10:
        raise ValueError(f"单次最多支持 10 个仓库，当前: {len(result)} 个")

    return result


if __name__ == "__main__":
    try:
        input_text = sys.stdin.read()
        result = parse_repos(input_text)
        print(json.dumps(result))
    except ValueError as e:
        print(f"❌ 错误: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ 未知错误: {e}", file=sys.stderr)
        sys.exit(1)
