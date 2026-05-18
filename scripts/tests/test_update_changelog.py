"""
update-changelog.py 单元测试 — 重点覆盖日历版号 vs SemVer 的日期追加差异

运行方式: python3 -m pytest scripts/tests/test_update_changelog.py
"""
import importlib.util
import sys
from pathlib import Path

import pytest

_SCRIPT = Path(__file__).resolve().parents[1] / "update-changelog.py"
_spec = importlib.util.spec_from_file_location("update_changelog", _SCRIPT)
update_changelog_mod = importlib.util.module_from_spec(_spec)
sys.modules["update_changelog"] = update_changelog_mod
_spec.loader.exec_module(update_changelog_mod)

update_changelog = update_changelog_mod.update_changelog
_is_calendar_version = update_changelog_mod._is_calendar_version


_BASE_CHANGELOG = """# Changelog

## [Unreleased]

### Added

- something
"""


@pytest.mark.parametrize(
    "version,expected",
    [
        ("2026.05.18", True),
        ("2026.5.18", True),
        ("2026.05.1", True),
        ("1.5.0", False),
        ("0.11.0", False),
        ("1.5.0-rc.1", False),
        ("26.05.18", False),   # 年份不足四位
        ("2026.05", False),    # 缺少日
    ],
)
def test_is_calendar_version(version, expected):
    assert _is_calendar_version(version) is expected


def test_calendar_version_omits_date(tmp_path):
    f = tmp_path / "CHANGELOG.md"
    f.write_text(_BASE_CHANGELOG, encoding="utf-8")

    result = update_changelog(str(f), "2026.05.18")
    assert result["success"], result["message"]

    content = f.read_text(encoding="utf-8")
    assert "## [2026.05.18]" in content
    assert "## [2026.05.18] -" not in content       # 不应追加日期
    assert "## [Unreleased]" in content              # 新占位符已插回


def test_calendar_version_ignores_explicit_date(tmp_path, capsys):
    f = tmp_path / "CHANGELOG.md"
    f.write_text(_BASE_CHANGELOG, encoding="utf-8")

    result = update_changelog(str(f), "2026.05.18", release_date="2099-01-01")
    assert result["success"], result["message"]

    content = f.read_text(encoding="utf-8")
    assert "## [2026.05.18]" in content
    assert "2099" not in content
    captured = capsys.readouterr()
    assert "已忽略传入的 release_date" in captured.err


def test_semver_still_appends_date(tmp_path):
    f = tmp_path / "CHANGELOG.md"
    f.write_text(_BASE_CHANGELOG, encoding="utf-8")

    result = update_changelog(str(f), "1.5.0", release_date="2026-05-18")
    assert result["success"], result["message"]

    content = f.read_text(encoding="utf-8")
    assert "## [1.5.0] - 2026-05-18" in content
