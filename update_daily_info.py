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
import random
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


def generate_short_info() -> tuple[str, str]:
    """Generate a short, fun info pair for daily logs.

    Returns a tuple like (role, mood) that is later rendered as
    "role | mood" in the daily log.
    """
    roles = [
        "Game Developer",
        "AI Enthusiast",
        "Pythonista",
        "Maker",
        "Open Source Lover",
    ]
    moods = [
        "Always curious",
        "Keep learning",
        "Ship small, ship often",
        "Build > Talk",
        "Stay positive",
    ]
    return random.choice(roles), random.choice(moods)


def update_short_info(content: str) -> str:
    """Optionally update a short-info block in README if markers exist.

    This is a safe no-op unless future markers like
    "<!-- SHORT-INFO:START -->" and "<!-- SHORT-INFO:END -->" are added.
    """
    # Currently no dedicated short-info markers in the repository.
    # Return content unchanged to avoid NameError and keep behavior stable.
    return content


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
    
    # 更新簡短資訊（若未配置相關區塊則不變更）
    updated = update_short_info(updated)

    if updated != original:
        path.write_text(updated, encoding="utf-8")
        return True
    return False


def write_daily_log(log_dir: Path, date_str: str, timestamp: str, short_info: tuple[str, str] | None = None) -> bool:
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / f"{date_str}.md"
    header = f"# 每日更新 - {date_str}\n"
    body = (
        f"- 時間：{timestamp}\n"
        f"- 狀態：更新 README 時間戳\n"
    )
    if short_info:
        left, right = short_info
        body += f"- 簡短資訊：{left} | {right}\n"
    content = header + "\n" + body

    if log_file.exists():
        existing = log_file.read_text(encoding="utf-8")
        if existing.strip() == content.strip():
            return False
    log_file.write_text(content, encoding="utf-8")
    return True


class DailyUpdater:
    """Object-oriented interface for the daily updater.

    Exposes convenient attributes for troubleshooting docs/tests:
      - current_time: datetime in configured timezone
      - date_str: YYYY-MM-DD
      - time_str: HH:MM
    """

    def __init__(self, config: Optional[Config] | None = None):
        self.config = config or load_config()
        self.root = ROOT
        self._set_now()

    def _set_now(self) -> None:
        tz = self.config.update_config.timezone
        self.current_time = now_in_tz(tz)
        self.date_str = self.current_time.strftime("%Y-%m-%d")
        self.time_str = self.current_time.strftime("%H:%M")
        self.timestamp_display = f"{self.date_str} {self.time_str} ({tz})"

    def refresh_time(self) -> None:
        self._set_now()

    def update_readme(self, path: Optional[Path] = None) -> bool:
        uc = self.config.update_config
        if path is None:
            # Choose the first README-like file from configured list
            candidates = [p for p in uc.files_to_update if Path(p).name.lower() == "readme.md"]
            target = Path(candidates[0]) if candidates else Path("README.md")
            path = (self.root / target).resolve()
        return update_readme(
            path,
            timestamp=self.timestamp_display,
            start=uc.readme_marker_start,
            end=uc.readme_marker_end,
            title=uc.readme_timestamp_title,
        )

    def write_daily_log(self, short_info: tuple[str, str] = None) -> bool:
        uc = self.config.update_config
        log_dir = self.root / uc.log_dir
        return write_daily_log(log_dir, self.date_str, self.timestamp_display, short_info)

    def run(self) -> bool:
        # Refresh time at run start
        self.refresh_time()
        uc = self.config.update_config
        changed = False
        # 產生簡短資訊並寫入日誌
        short_info = generate_short_info()
        # 更新 README 與每日紀錄
        changed |= self.update_readme()
        changed |= self.write_daily_log(short_info)
        return changed


def main() -> int:
    updater = DailyUpdater()
    changed = updater.run()
    if changed:
        print(f"✅ 已更新內容於 {updater.timestamp_display}")
    else:
        print(f"ℹ️ 無變更需要更新（{updater.timestamp_display}）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
