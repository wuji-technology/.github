#!/usr/bin/env python3
"""
解析多行文本格式的仓库版本配置

格式: repo=version，每行一个
示例:
    wujihandpy=1.5.0
    wujihandros2=2.0.0
"""
import json
import re
import sys


def parse_repos(input_text):
    """
    解析格式: repo1=1.5.0\nrepo2=2.0.0
    返回: [{"repo": "repo1", "version": "1.5.0"}, ...]
    """
    result = []

    for line_num, line in enumerate(input_text.strip().split('\n'), 1):
        line = line.strip()

        # 跳过空行和注释
        if not line or line.startswith('#'):
            continue

        # 匹配 repo=version
        match = re.match(r'^([a-zA-Z0-9_-]+)\s*=\s*(.+)$', line)
        if not match:
            raise ValueError(f"第 {line_num} 行格式错误: {line}\n正确格式: repo=version")

        repo, version = match.groups()
        version = version.strip()

        # 验证版本号格式 (X.Y.Z 或 X.Y.Z-suffix)
        if not re.match(r'^\d+\.\d+\.\d+(-[a-zA-Z0-9.]+)?$', version):
            raise ValueError(
                f"第 {line_num} 行版本号格式错误: {version}\n"
                f"正确格式: X.Y.Z 或 X.Y.Z-suffix (如 1.5.0 或 1.5.0-hotfix.1)"
            )

        result.append({"repo": repo.strip(), "version": version})

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
