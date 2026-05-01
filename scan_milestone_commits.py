"""Scan RCS history for first canonical milestone commits.

This script is read-only: it shells out to git against a local checkout of
 and never mutates that repository.

Milestones tracked (relative to the Day 388 baseline):
- First commit where any Rogue autosave reaches level >= 20.
- First commit where any Cleric autosave reaches level >= 3.
- First commit where any documentation (project-docs or root-level summary markdown)
  records Warrior damage > 5,923,246.
- First commit where any documentation text explicitly mentions Rogue L20+ or
  Cleric L3+ (narrative milestone evidence).
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional, Tuple

RCS_PATH = Path.home() / "rest-collaboration-showcase"
BASELINE_DEFAULT = "c391f28"  # Day 388 final summary
WARRIOR_BASELINE_DAMAGE = 5_923_246


@dataclass
class AutosaveLevels:
    rogue_max: Optional[int]
    cleric_max: Optional[int]


def _run_git(cmd: List[str]) -> subprocess.CompletedProcess:
    """Run a git command with capture_output=True against RCS_PATH by default."""

    return subprocess.run(
        cmd,
        cwd=str(RCS_PATH),
        capture_output=True,
        text=True,
    )


def _git_stdout(cmd: List[str]) -> str:
    """Return stdout for a git command; empty string on error."""

    cp = _run_git(cmd)
    if cp.returncode != 0:
        return ""
    return cp.stdout.strip()


def get_origin_head() -> str:
    sha = _git_stdout(["git", "rev-parse", "origin/main"])
    return sha.strip()


def rev_list_since(baseline_sha: str, head_sha: str) -> List[str]:
    """Return commits after baseline up to head."""

    out = _git_stdout(
        [
            "git",
            "rev-list",
            "--reverse",
            f"{baseline_sha}..{head_sha}",
        ]
    )
    return [line.strip() for line in out.splitlines() if line.strip()]


def _list_paths_at_commit(sha: str, prefix: str, suffix: str) -> List[str]:
    """List paths under a prefix at a commit, filtered by suffix (e.g. .json)."""

    out = _git_stdout(
        [
            "git",
            "ls-tree",
            "-r",
            "--name-only",
            sha,
            "--",
            prefix,
        ]
    )
    return [p for p in out.splitlines() if p.endswith(suffix)]


def _list_root_paths_at_commit(sha: str, suffix: str) -> List[str]:
    """List root-level paths at a commit filtered by suffix."""

    out = _git_stdout(
        [
            "git",
            "ls-tree",
            "--name-only",
            sha,
        ]
    )
    return [p for p in out.splitlines() if "/" not in p and p.endswith(suffix)]


def _load_json_at(sha: str, path: str):  # type: ignore[no-untyped-def]
    cp = _run_git(["git", "show", f"{sha}:{path}"])
    if cp.returncode != 0:
        return None
    try:
        return json.loads(cp.stdout)
    except json.JSONDecodeError:
        return None


def analyze_autosaves_at_commit(sha: str) -> AutosaveLevels:
    """Return maximum Rogue and Cleric levels present in autosaves at a commit."""

    rogue_max: Optional[int] = None
    cleric_max: Optional[int] = None

    json_paths: List[str] = []
    json_paths.extend(_list_paths_at_commit(sha, "autosaves", ".json"))
    json_paths.extend(
        _list_paths_at_commit(sha, "contributions/autosave-traces", ".json")
    )

    for path in json_paths:
        data = _load_json_at(sha, path)
        if not isinstance(data, dict):
            continue

        player = None
        save = data.get("save")
        if isinstance(save, dict):
            p = save.get("player")
            if isinstance(p, dict):
                player = p

        if player is None and isinstance(data.get("player"), dict):
            player = data["player"]

        if player is None:
            continue

        # Extract level
        level_raw = player.get("level") or data.get("level")
        try:
            level = int(level_raw) if level_raw is not None else None
        except (TypeError, ValueError):
            level = None

        if level is None:
            continue

        # Extract class text
        class_raw = (
            player.get("className")
            or player.get("classId")
            or player.get("class_id")
            or player.get("class")
        )
        class_text = str(class_raw).lower() if class_raw is not None else ""

        if "rogue" in class_text or "assassin" in class_text:
            rogue_max = level if rogue_max is None else max(rogue_max, level)
        if "cleric" in class_text:
            cleric_max = level if cleric_max is None else max(cleric_max, level)

    return AutosaveLevels(rogue_max=rogue_max, cleric_max=cleric_max)


def analyze_warrior_damage_at_commit(sha: str) -> Optional[int]:
    """Return the maximum integer (damage-like) value in markdown docs at a commit."""

    doc_paths: List[str] = []
    doc_paths.extend(_list_paths_at_commit(sha, "contributions/project-docs", ".md"))
    doc_paths.extend(_list_paths_at_commit(sha, "contributions/project-docs", ".txt"))
    doc_paths.extend(_list_root_paths_at_commit(sha, ".md"))
    doc_paths.extend(_list_root_paths_at_commit(sha, ".txt"))

    if not doc_paths:
        return None

    max_val: Optional[int] = None
    number_re = re.compile(r"\b[0-9][0-9,]{3,}\b")
    include_keywords = ("damage", "dmg", "gain", "opus", "warrior")
    exclude_keywords = ("hp", "health", "boss")

    for path in doc_paths:
        cp = _run_git(["git", "show", f"{sha}:{path}"])
        if cp.returncode != 0:
            continue
        for line in cp.stdout.splitlines():
            lowered = line.lower()
            if any(skip in lowered for skip in exclude_keywords):
                continue
            if not any(key in lowered for key in include_keywords):
                continue

            for m in number_re.findall(line):
                try:
                    v = int(m.replace(",", ""))
                except ValueError:
                    continue
                if max_val is None or v > max_val:
                    max_val = v

    return max_val


def analyze_narrative_levels_at_commit(sha: str) -> AutosaveLevels:
    """Return max Rogue and Cleric levels explicitly mentioned in markdown docs."""

    doc_paths: List[str] = []
    doc_paths.extend(_list_paths_at_commit(sha, "contributions/project-docs", ".md"))
    doc_paths.extend(_list_paths_at_commit(sha, "contributions/project-docs", ".txt"))
    doc_paths.extend(_list_root_paths_at_commit(sha, ".md"))
    doc_paths.extend(_list_root_paths_at_commit(sha, ".txt"))

    if not doc_paths:
        return AutosaveLevels(rogue_max=None, cleric_max=None)

    rogue_max: Optional[int] = None
    cleric_max: Optional[int] = None
    rogue_re = re.compile(
        r"(?i)\b(?:level|lvl|l)\s*([0-9]{1,2})\s*(?:rogue|assassin)"
    )
    cleric_re = re.compile(r"(?i)\b(?:level|lvl|l)\s*([0-9]{1,2})\s*cleric")

    for path in doc_paths:
        cp = _run_git(["git", "show", f"{sha}:{path}"])
        if cp.returncode != 0:
            continue
        text = cp.stdout

        for m in rogue_re.finditer(text):
            try:
                val = int(m.group(1))
            except (TypeError, ValueError):
                continue
            rogue_max = val if rogue_max is None else max(rogue_max, val)

        for m in cleric_re.finditer(text):
            try:
                val = int(m.group(1))
            except (TypeError, ValueError):
                continue
            cleric_max = val if cleric_max is None else max(cleric_max, val)

    return AutosaveLevels(rogue_max=rogue_max, cleric_max=cleric_max)


def scan_milestone_commits(baseline_sha: str) -> None:
    head_sha = get_origin_head()
    commits = rev_list_since(baseline_sha, head_sha)

    print(f"== Milestone scan (baseline {baseline_sha} -> head {head_sha}) ==")
    if not commits:
        print("No commits found after baseline.")
        return

    first_rogue_autosave: Optional[Tuple[str, int]] = None
    first_rogue_narrative: Optional[Tuple[str, int]] = None
    first_cleric_autosave: Optional[Tuple[str, int]] = None
    first_cleric_narrative: Optional[Tuple[str, int]] = None
    first_warrior: Optional[Tuple[str, int]] = None

    for sha in commits:
        autos = analyze_autosaves_at_commit(sha)
        narr = analyze_narrative_levels_at_commit(sha)
        dmg_max = analyze_warrior_damage_at_commit(sha)

        if (
            first_rogue_autosave is None
            and autos.rogue_max is not None
            and autos.rogue_max >= 20
        ):
            first_rogue_autosave = (sha, autos.rogue_max)

        if (
            first_rogue_narrative is None
            and narr.rogue_max is not None
            and narr.rogue_max >= 20
        ):
            first_rogue_narrative = (sha, narr.rogue_max)

        if (
            first_cleric_autosave is None
            and autos.cleric_max is not None
            and autos.cleric_max >= 3
        ):
            first_cleric_autosave = (sha, autos.cleric_max)

        if (
            first_cleric_narrative is None
            and narr.cleric_max is not None
            and narr.cleric_max >= 3
        ):
            first_cleric_narrative = (sha, narr.cleric_max)

        if (
            first_warrior is None
            and dmg_max is not None
            and dmg_max > WARRIOR_BASELINE_DAMAGE
        ):
            first_warrior = (sha, dmg_max)

    if first_rogue_autosave is None:
        print("Rogue L20+ first canonical autosave commit: none yet.")
    else:
        sha, lvl = first_rogue_autosave
        print(
            f"Rogue L20+ first canonical autosave commit: {sha} "
            f"(Rogue max autosave level = {lvl})."
        )

    if first_rogue_narrative is None:
        print("Rogue L20+ first canonical narrative-doc commit: none yet.")
    else:
        sha, lvl = first_rogue_narrative
        print(
            f"Rogue L20+ first canonical narrative-doc commit: {sha} "
            f"(Rogue max documented level = {lvl})."
        )

    if first_cleric_autosave is None:
        print("Cleric L3+ first canonical autosave commit: none yet.")
    else:
        sha, lvl = first_cleric_autosave
        print(
            f"Cleric L3+ first canonical autosave commit: {sha} "
            f"(Cleric max autosave level = {lvl})."
        )

    if first_cleric_narrative is None:
        print("Cleric L3+ first canonical narrative-doc commit: none yet.")
    else:
        sha, lvl = first_cleric_narrative
        print(
            f"Cleric L3+ first canonical narrative-doc commit: {sha} "
            f"(Cleric max documented level = {lvl})."
        )

    if first_warrior is None:
        print("Warrior >5,923,246 first canonical documentation commit: none yet.")
    else:
        sha, dmg = first_warrior
        print(
            f"Warrior >5,923,246 first canonical documentation commit: {sha} "
            f"(max documented damage = {dmg})."
        )


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Scan rest-collaboration-showcase history for first canonical "
            "Rogue L20, Cleric L3+, and Warrior>5.923M commits "
            "(docs/autosaves/proofs plus root-level summary docs)."
        )
    )
    parser.add_argument(
        "--baseline-sha",
        default=BASELINE_DEFAULT,
        help=(
            "Baseline SHA to start scanning after. Default is the Day 388 "
            "final summary commit (c391f28)."
        ),
    )
    args = parser.parse_args()

    scan_milestone_commits(args.baseline_sha)


if __name__ == "__main__":  # pragma: no cover
    main()
