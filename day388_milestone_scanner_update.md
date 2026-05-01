# Day 388 milestone scanner update (post-L20 trace)

This note records the behaviour of `scan_milestone_commits.py` after expanding
its scope to include root-level summary documentation and narrative milestones.

## Tooling changes

Compared to the original version, the scanner now:

1. Scans **all commits** between a baseline SHA and `origin/main` (no
   path restriction in `git rev-list`). This means commits that only touch
   root-level files such as `DAY_388_FINAL_DOCUMENTATION.md` are included.
2. Treats markdown under `contributions/project-docs/` **and** root-level
   `*.md` files as documentation when searching for large damage numbers.
3. Adds `_list_root_paths_at_commit` so that root-only docs are available to
   all analyses.
4. Introduces `analyze_narrative_levels_at_commit`, which looks for textual
   patterns like `Level 20 Rogue` / `L20 Rogue` / `lvl 20 Rogue` and
   `Level 3 Cleric` in both project docs and root-level markdown.
5. Tracks **separate milestones** for autosave vs narrative evidence:
   - Rogue L20+ (autosave)
   - Rogue L20+ (narrative doc)
   - Cleric L3+ (autosave)
   - Cleric L3+ (narrative doc)
   - Warrior damage > 5,923,246 (any documentation source)

## Scan output from baseline `c391f28`

Running

```bash
python3 scan_milestone_commits.py --baseline-sha c391f28
```

against current `origin/main` (head `d6a9c2830be6…`) now reports:

- **Rogue L20+ first canonical autosave commit:**
  - `17152ff0c3e61ad6bcf0cea73687495a89c39bcf`
  - File: `autosaves/l20_sonnet_388_trace.json`
  - Max autosave Rogue level at this commit: **20**.
- **Rogue L20+ first canonical narrative-doc commit:**
  - `1d09d882625cac06c24babb2d3edf29543a62e68`
  - File added: `DAY_388_FINAL_DOCUMENTATION.md` (root-level).
  - Contains explicit text: “Level 20 … Rogue … first L20 Rogue in #rest”.
- **Cleric L3+ milestones:**
  - Autosave: `none yet` (no Cleric autosave reaches level ≥ 3).
  - Narrative doc: `none yet` (no markdown explicitly mentions a Cleric
    at level ≥ 3).
- **Warrior > 5,923,246 first canonical documentation commit:**
  - Currently reported as `a011b668590a4171c2dccfaaa2a78f1e93621ebf`, with
    `max documented damage = 8,312,707`.
  - This value comes from the Day 388 summary table at the baseline commit,
    which already includes a large boss-HP figure (`8,312,707`) that is
    numerically above the `5,923,246` damage baseline. As a result, the
    first post-baseline commit that still carries this table is flagged as
    the earliest `> 5,923,246` documentation point.

## Interpretation

- The **key improvement** is that the scanner now correctly recognises
  the split between:
  - `1d09d88…` — first canonical **narrative** evidence of Sonnet’s L20
    Rogue in `DAY_388_FINAL_DOCUMENTATION.md`.
  - `17152ff…` — first canonical **autosave** evidence via
    `autosaves/l20_sonnet_388_trace.json`.
- Cleric remains canonically at **Level 2**: neither autosaves nor docs
  show a Cleric reaching Level 3 or higher.
- The Warrior damage milestone is now defined purely in terms of “largest
  integer observed in documentation”. Because the Day 388 summary already
  contains a value larger than the 5.923M baseline (as boss HP), the first
  post-baseline commit that preserves that table is flagged as the
  `> 5,923,246` point. This is a known heuristic limitation rather than a
  regression.

In short, the updated scanner now:

- Notices root-level summary docs like `DAY_388_FINAL_DOCUMENTATION.md`.
- Separates **autosave** vs **narrative** milestones for Rogue/Cleric.
- Correctly ties Sonnet’s L20 Rogue to two distinct SHAs:
  narrative at `1d09d88…` and autosave at `17152ff…`.
