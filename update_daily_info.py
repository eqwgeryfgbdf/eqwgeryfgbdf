#!/usr/bin/env python3
"""
Daily updater script

- Updates a timestamp block in README.md between markers
  <!-- DAILY-UPDATE:START --> and <!-- DAILY-UPDATE:END -->.
- Writes/updates a daily log file under the configured log directory.

Configuration is loaded from config.json (if present). Sensible defaults
are used when keys are missing.
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional

try:
    # Python 3.9+
    from zoneinfo import ZoneInfo
except Exception:  # pragma: no cover
    ZoneInfo = None  # type: ignore


ROOT = Path(__file__).resolve().parent


@dataclass
class UpdateConfig:
    timezone: str = "Asia/Taipei"
    log_dir: str = "daily_logs"
    files_to_update: List[str] = None  # type: ignore
    readme_marker_start: str = "<!-- DAILY-UPDATE:START -->"
    readme_marker_end: str = "<!-- DAILY-UPDATE:END -->"
    readme_timestamp_title: str = "## 📅 自動更新時間"

    def __post_init__(self):
        if self.files_to_update is None:
            self.files_to_update = ["README.md"]


@dataclass
class Config:
    update_config: UpdateConfig
    commit_message_template: str = "🤖 每日自動更新 - {date} {time} (Asia/Taipei)"


def load_config() -> Config:
    cfg_path = ROOT / "config.json"
    if not cfg_path.exists():
        return Config(update_config=UpdateConfig())

    with cfg_path.open("r", encoding="utf-8") as f:
        raw = json.load(f)

    uc_raw = raw.get("update_config", {}) if isinstance(raw, dict) else {}
    uc = UpdateConfig(
        timezone=uc_raw.get("timezone", "Asia/Taipei"),
        log_dir=uc_raw.get("log_dir", "daily_logs"),
        files_to_update=uc_raw.get("files_to_update", ["README.md"]),
        readme_marker_start=uc_raw.get("readme_marker_start", "<!-- DAILY-UPDATE:START -->"),
        readme_marker_end=uc_raw.get("readme_marker_end", "<!-- DAILY-UPDATE:END -->"),
        readme_timestamp_title=uc_raw.get("readme_timestamp_title", "## 📅 自動更新時間"),
    )
    return Config(
        update_config=uc,
        commit_message_template=raw.get(
            "commit_message_template",
            "🤖 每日自動更新 - {date} {time} (Asia/Taipei)",
        ),
    )


def now_in_tz(tz_name: str) -> datetime:
    if ZoneInfo is None:
        return datetime.utcnow()
    try:
        return datetime.now(ZoneInfo(tz_name))
    except Exception:
        return datetime.utcnow()


def ensure_marker_block(content: str, title: str, start: str, end: str) -> str:
    if start in content and end in content:
        return content
    block = (
        f"\n\n{title}\n\n"
        f"{start}\n"
        f"(尚未更新)\n"
        f"{end}\n"
    )
    # Append to end
    return content.rstrip() + block + "\n"


def update_readme(path: Path, timestamp: str, start: str, end: str, title: str) -> bool:
    if not path.exists():
        return False
    original = path.read_text(encoding="utf-8")
    content = ensure_marker_block(original, title, start, end)

    # Replace everything between markers (single-line content)
    pattern = re.compile(
        rf"({re.escape(start)})([\s\S]*?)({re.escape(end)})",
        re.MULTILINE,
    )
    replacement = rf"\1\n最後更新：{timestamp}\n\3"
    updated = pattern.sub(replacement, content)

    if updated != original:
        path.write_text(updated, encoding="utf-8")
        return True
    return False


def write_daily_log(log_dir: Path, date_str: str, timestamp: str) -> bool:
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / f"{date_str}.md"
    header = f"# 每日更新 - {date_str}\n"
    body = (
        f"- 時間：{timestamp}\n"
        f"- 狀態：更新 README 時間戳\n"
    )
    content = header + "\n" + body

    if log_file.exists():
        existing = log_file.read_text(encoding="utf-8")
        if existing.strip() == content.strip():
            return False
    log_file.write_text(content, encoding="utf-8")
    return True


def main() -> int:
    cfg = load_config()
    uc = cfg.update_config

    now = now_in_tz(uc.timezone)
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M")
    ts_display = f"{date_str} {time_str} ({uc.timezone})"

    changed = False
    for file_rel in uc.files_to_update:
        p = (ROOT / file_rel).resolve()
        if p.name.lower() == "readme.md":
            changed |= update_readme(
                p,
                timestamp=ts_display,
                start=uc.readme_marker_start,
                end=uc.readme_marker_end,
                title=uc.readme_timestamp_title,
            )

    changed |= write_daily_log(ROOT / uc.log_dir, date_str, ts_display)

    if changed:
        print(f"✅ 已更新內容於 {ts_display}")
    else:
        print(f"ℹ️ 無變更需要更新（{ts_display}）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

