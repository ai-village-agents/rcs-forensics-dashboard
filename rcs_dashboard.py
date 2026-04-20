"""RCS Forensics Dashboard

Read-only summary tooling for the Rest Collaboration Showcase repository.

This script expects a local checkout of `rest-collaboration-showcase` and
emits a concise status report. It never mutates that repository.
"""

from __future__ import annotations

import argparse
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import List

RCS_PATH = Path.home() / "rest-collaboration-showcase"


@dataclass
class WarriorMilestone:
    sha: str
    message: str


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
        milestones.append(WarriorMilestone(sha=sha, message=msg))
    return milestones


def get_autosave_trace_count() -> int:
    """Return the number of JSON files in contributions/autosave-traces."""

    autosave_dir = RCS_PATH / "contributions" / "autosave-traces"
    if not autosave_dir.is_dir():
        return 0
    return len(list(autosave_dir.glob("*.json")))


def grep_autosave_for(pattern: str) -> bool:
    """Return True if `pattern` appears anywhere under autosave-traces."""

    autosave_dir = RCS_PATH / "contributions" / "autosave-traces"
    if not autosave_dir.is_dir():
        return False
    out = _run([
        "grep",
        "-R",
        pattern,
        str(autosave_dir),
    ])
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

    # Autosave corpus overview
    lines.append("\n== Autosave Corpus ==")
    count = get_autosave_trace_count()
    lines.append(f"Total autosave JSON files: {count}")

    # Key presence/absence checks
    checks = {
        "Rogue L16 (l16_sonnet)": "l16_sonnet",
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

    # Autosave corpus section
    lines.append("\n## Autosave Corpus Summary")
    count = get_autosave_trace_count()
    lines.append(f"- **Total autosave JSON files:** {count}")

    checks = {
        "Rogue L16 (l16_sonnet)": "l16_sonnet",
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
