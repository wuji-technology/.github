#!/usr/bin/env python3
"""
更新 CHANGELOG.md，将 Unreleased 替换为指定版本

符合 Keep a Changelog 规范
"""
import re
import argparse
from datetime import date
from pathlib import Path


def update_changelog(file_path, version, release_date=None):
    """
    更新 CHANGELOG.md

    Args:
        file_path: CHANGELOG.md 路径
        version: 版本号 (如 1.5.0)
        release_date: 发布日期 (默认今天，格式 YYYY-MM-DD)

    Returns:
        {"success": bool, "message": str}
    """
    if release_date is None:
        release_date = date.today().strftime('%Y-%m-%d')

    file_path = Path(file_path)
    if not file_path.exists():
        return {"success": False, "message": f"文件不存在: {file_path}"}

    try:
        content = file_path.read_text(encoding='utf-8')
    except Exception as e:
        return {"success": False, "message": f"读取文件失败: {e}"}

    # 检查 Unreleased 章节（支持中英文）
    unreleased_pattern = r'## (?:\[)?(?:Unreleased|未发布)(?:\])?'
    if not re.search(unreleased_pattern, content, re.IGNORECASE):
        return {"success": False, "message": "未找到 Unreleased 或 未发布 章节"}

    # 检查版本是否已存在
    version_pattern = rf'## \[{re.escape(version)}\]'
    if re.search(version_pattern, content):
        return {"success": False, "message": f"版本 {version} 已存在"}

    # 替换 Unreleased（第一个匹配项）
    content_new = re.sub(
        unreleased_pattern,
        f'## [{version}] - {release_date}',
        content,
        count=1,
        flags=re.IGNORECASE
    )

    # 在顶部添加新的 Unreleased 占位符
    # 找到第一个 ## 标题的位置（应该是刚才替换的版本标题）
    match = re.search(r'\n## ', content_new)
    if match:
        insert_pos = match.start()
        before = content_new[:insert_pos]
        after = content_new[insert_pos:]
        content_new = f"{before}\n\n## [Unreleased]\n{after}"
    else:
        # 如果没有找到，说明文件格式可能有问题，但还是尝试添加
        content_new = f"## [Unreleased]\n\n{content_new}"

    # 写回文件
    try:
        file_path.write_text(content_new, encoding='utf-8')
    except Exception as e:
        return {"success": False, "message": f"写入文件失败: {e}"}

    return {
        "success": True,
        "message": f"成功: Unreleased → [{version}] - {release_date}"
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='更新 CHANGELOG.md，将 Unreleased 替换为指定版本'
    )
    parser.add_argument('--file', required=True, help='CHANGELOG.md 路径')
    parser.add_argument('--version', required=True, help='版本号 (如 1.5.0)')
    parser.add_argument('--date', help='发布日期 YYYY-MM-DD (默认今天)', default=None)

    args = parser.parse_args()
    result = update_changelog(args.file, args.version, args.date)

    if result['success']:
        print(f"✅ {result['message']}")
        exit(0)
    else:
        print(f"❌ {result['message']}")
        exit(1)
