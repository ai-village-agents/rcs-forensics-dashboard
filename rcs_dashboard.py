"""RCS Forensics Dashboard

Read-only summary tooling for the Rest Collaboration Showcase repository.

This script expects a local checkout of `rest-collaboration-showcase` and
emits a concise status report. It never mutates that repository.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import List

RCS_PATH = Path.home() / "rest-collaboration-showcase"


@dataclass
class WarriorMilestone:
    sha: str
    message: str
    damage: int | None = None


def _run(cmd: List[str], cwd: Path | None = None) -> str:
    """Run a command and return stdout as text (read-only helper)."""

    result = subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        check=False,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def list_autosave_json_paths_from_origin() -> List[str]:
    """Return autosave trace JSON paths from origin/main."""

    out = _run([
        "git",
        "ls-tree",
        "-r",
        "--name-only",
        "origin/main",
        "--",
        "contributions/autosave-traces",
    ], cwd=RCS_PATH)
    return [line for line in out.splitlines() if line.endswith(".json")]


def get_recent_warrior_milestones(n: int = 15) -> List[WarriorMilestone]:
    """Return the most recent Warrior milestone deploy commits from origin/main."""

    log_output = _run([
        "git",
        "log",
        "--oneline",
        "origin/main",
        "--grep",
        "Deploy ",
        "--grep",
        "milestone",
        "--grep",
        "dmg",
        "-i",
        f"-n{n}",
    ], cwd=RCS_PATH)

    milestones: List[WarriorMilestone] = []
    for line in log_output.splitlines():
        if not line.strip():
            continue
        parts = line.split(maxsplit=1)
        if len(parts) != 2:
            continue
        sha, msg = parts
        damage_match = re.search(r"([0-9,]+)\s*dmg", msg, re.IGNORECASE)
        damage = None
        if damage_match:
            damage_str = damage_match.group(1).replace(",", "")
            try:
                damage = int(damage_str)
            except ValueError:
                damage = None
        milestones.append(WarriorMilestone(sha=sha, message=msg, damage=damage))
    return milestones


def get_warrior_damage_summary(milestones: List[WarriorMilestone]) -> dict:
    """Compute simple stats for milestones that include damage totals."""

    with_damage = [m for m in milestones if m.damage is not None]
    if not with_damage:
        return {}

    latest_damage = with_damage[0].damage  # newest entry from git log
    min_damage = min(m.damage for m in with_damage if m.damage is not None)
    max_damage = max(m.damage for m in with_damage if m.damage is not None)

    if latest_damage is None:
        return {}

    return {
        "count": len(with_damage),
        "min_damage": min_damage,
        "max_damage": max_damage,
        "latest_damage": latest_damage,
        "delta_from_oldest_to_latest": latest_damage - min_damage,
    }


def get_autosave_trace_count() -> int:
    """Return the number of JSON files in contributions/autosave-traces."""

    paths = list_autosave_json_paths_from_origin()
    return len(paths)


def get_autosave_stats() -> dict:
    """Return aggregate stats for autosave traces."""

    autosave_paths = list_autosave_json_paths_from_origin()
    if not autosave_paths:
        return {"total": 0, "levels": {}, "autoSaveReasons": {}}

    level_counter: Counter = Counter()
    reason_counter: Counter = Counter()
    parsed_files = 0

    for path in autosave_paths:
        try:
            raw = _run(["git", "show", f"origin/main:{path}"], cwd=RCS_PATH)
            data = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if not isinstance(data, dict):
            continue

        parsed_files += 1

        level = data.get("level")
        if level is not None:
            try:
                level_counter[int(level)] += 1
            except (TypeError, ValueError):
                pass

        reason = data.get("autoSaveReason")
        reason_key = reason if reason else "<missing>"
        reason_counter[reason_key] += 1

    return {
        "total": parsed_files,
        "levels": dict(level_counter),
        "autoSaveReasons": dict(reason_counter),
    }


def grep_autosave_for(pattern: str) -> bool:
    """Return True if `pattern` appears anywhere under autosave-traces."""

    out = _run([
        "git",
        "grep",
        "-n",
        pattern,
        "origin/main",
        "--",
        "contributions/autosave-traces",
    ], cwd=RCS_PATH)
    return bool(out.strip())


def generate_text_report() -> str:
    """Generate a plain-text status report."""

    lines: List[str] = []

    lines.append("RCS FORENSICS DASHBOARD (read-only)\n")

    # Warrior milestones
    lines.append("== Warrior Milestone Deploys (recent) ==")
    milestones = get_recent_warrior_milestones()
    if not milestones:
        lines.append("(no matching milestone deploy commits found)")
    else:
        for m in milestones:
            lines.append(f"- {m.sha}  {m.message}")

    lines.append("\n== Warrior Damage Summary ==")
    summary = get_warrior_damage_summary(milestones)
    if not summary:
        lines.append("(no damage information available)")
    else:
        lines.append(f"Latest damage: {summary['latest_damage']}")
        lines.append(f"Min damage (window): {summary['min_damage']}")
        lines.append(f"Max damage (window): {summary['max_damage']}")
        lines.append(f"Delta (oldest to latest): {summary['delta_from_oldest_to_latest']}")
        lines.append(f"Samples: {summary['count']}")

    # Autosave corpus overview
    lines.append("\n== Autosave Corpus ==")
    count = get_autosave_trace_count()
    lines.append(f"Total autosave JSON files: {count}")

    stats = get_autosave_stats()
    if stats["total"] == 0:
        lines.append("No readable autosave traces for detailed stats.")
    else:
        lines.append("Level distribution:")
        for level, c in sorted(stats["levels"].items(), key=lambda item: item[0]):
            lines.append(f"  - L{level}: {c} traces")

        lines.append("Auto-save reasons:")
        for reason, c in sorted(stats["autoSaveReasons"].items(), key=lambda item: item[0]):
            lines.append(f"  - {reason}: {c}")

    # Key presence/absence checks
    checks = {
        "Rogue L16 (l16_sonnet)": "l16_sonnet",
        "Rogue L17 (l17_sonnet)": "l17_sonnet",
        "Cleric L2 pages_levelup": "pages_levelup",
        "Cleric L2 pages_postF5": "pages_postF5",
    }
    for label, pat in checks.items():
        present = grep_autosave_for(pat)
        status = "present" if present else "ABSENT"
        lines.append(f"- {label}: {status}")

    return "\n".join(lines) + "\n"


def generate_markdown_report() -> str:
    """Generate a Markdown-formatted status report."""

    lines: List[str] = []

    lines.append("# RCS Forensics Dashboard (read-only)\n")

    # Warrior section
    lines.append("## Warrior Milestone Deploys (recent)")
    milestones = get_recent_warrior_milestones()
    if not milestones:
        lines.append("_No matching milestone deploy commits found._")
    else:
        lines.append("\n| SHA | Message |\n| --- | ------- |")
        for m in milestones:
            lines.append(f"| `{m.sha}` | {m.message} |")

    lines.append("\n### Warrior Damage Summary")
    summary = get_warrior_damage_summary(milestones)
    if not summary:
        lines.append("No damage information available for recent milestones.")
    else:
        lines.append(f"- Latest damage: {summary['latest_damage']}")
        lines.append(f"- Min damage (window): {summary['min_damage']}")
        lines.append(f"- Max damage (window): {summary['max_damage']}")
        lines.append(f"- Delta (oldest to latest): {summary['delta_from_oldest_to_latest']}")
        lines.append(f"- Samples: {summary['count']}")

    # Autosave corpus section
    lines.append("\n## Autosave Corpus Summary")
    count = get_autosave_trace_count()
    lines.append(f"- **Total autosave JSON files:** {count}")

    stats = get_autosave_stats()
    if stats["total"] == 0:
        lines.append("No readable autosave traces available for detailed statistics.")
    else:
        lines.append("\n### Level Distribution")
        for level, c in sorted(stats["levels"].items(), key=lambda item: item[0]):
            lines.append(f"- L{level}: {c} traces")

        lines.append("\n### Auto-save Reasons")
        for reason, c in sorted(stats["autoSaveReasons"].items(), key=lambda item: item[0]):
            lines.append(f"- {reason}: {c}")

    checks = {
        "Rogue L16 (l16_sonnet)": "l16_sonnet",
        "Rogue L17 (l17_sonnet)": "l17_sonnet",
        "Cleric L2 pages_levelup": "pages_levelup",
        "Cleric L2 pages_postF5": "pages_postF5",
    }
    lines.append("\n### Key Trace Presence")
    lines.append("\n| Trace | Status |\n| ----- | ------ |")
    for label, pat in checks.items():
        present = grep_autosave_for(pat)
        status = "present" if present else "ABSENT"
        lines.append(f"| {label} | {status} |")

    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="RCS Forensics Dashboard (read-only)")
    parser.add_argument(
        "--markdown",
        action="store_true",
        help="emit a Markdown report instead of plain text",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="optional path to write the report to (defaults to stdout)",
    )
    args = parser.parse_args()

    if args.markdown:
        report = generate_markdown_report()
    else:
        report = generate_text_report()

    if args.output:
        args.output.write_text(report, encoding="utf-8")
    else:
        print(report, end="")


if __name__ == "__main__":  # pragma: no cover
    main()
