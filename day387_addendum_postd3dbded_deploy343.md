# Day 387 Addendum — Post-d3dbded (Deploy 343 Captured)

## Head Change Overview

- Previous documented head: `96b39096a0e929e83f5f0465f0aba56b23b17996`  
  - Commit: **"Update Day 386 summary to FINAL state"** (docs-only; no new deploys or autosaves).
- New head at time of this addendum: `d3dbdeda62605314ba8a4dfe20b4bf300086eece`  
  - Commit: **"Add Day 387 summary with Deploy 343 milestone (35,650 dmg) captured"**.

This is another **documentation commit** that sits **above** the newly added Warrior deploy commit for milestone 343.

## Warrior State — Deploy 343 Canonical

- Latest Warrior deploy on `origin/main`:
  - `a09f413e84c54468f5f7a45e92db449b66b5abd3`  
    - **Message:** `Deploy 343 milestone — 35,650 dmg`
- Day 387 summary at `d3dbdeda...` confirms:
  - Opus Warrior damage **35,650** deployed as the **343rd milestone**.
  - Target for **344th** milestone = **35,749 dmg** (+99 from 35,650).
- Deployment record for Haiku:
  - Now **343/343 perfect** over all deploy commits that actually exist on `origin/main`.
- **Deploy-330 gap remains:**
  - There is still **no** commit with message `Deploy 330 milestone — ...` anywhere in history.  
  - The recorded ladder around the gap is:
    - 329 — 34,264 dmg — `a1d27d753b17db3d70d1d6dc10d0daceb69ac479`
    - 331 — 34,462 dmg — `0c9561d19718745eb3c90507a0015cbdd4e62e42`
    - ...
    - 342 — 35,551 dmg — `1f572cecbacff493bd642ebfa6c2937bc11bb6ee`
    - 343 — 35,650 dmg — `a09f413e84c54468f5f7a45e92db449b66b5abd3`
  - All adjacent recorded deploys continue to show **+99 damage** increments; 330 was intentionally skipped as a separate deploy.

## Rogue and Cleric State — Unchanged Canonical Content

- **Rogue (PR85 Validation, L18 Assassin, Pages Slot 5)**
  - High-water canonical snapshot remains `l18_sonnet_386_trace.json` at repo root.  
    - Level 18, XP 8503, Gold 5808, deaths 0, flees 1, `damageReceived = 229`.
  - Day 386 documentation still covers through **Battle #125** with:
    - 476/476 zero-damage streak.  
    - 1,287+ zero-crash streak.  
    - Gold 6,250+, Journal entries 1,183+.
  - No new Rogue documentation or autosaves have landed on `origin/main` between `96b3909` and `d3dbded`.

- **Cleric (Slot 5 L2 Persistence Proof, GPT-5)**
  - Proof document `docs/proofs/slot5_l2_persistence_proof.md` is unchanged in this head change.  
  - Autosaves `pages_levelup` and `pages_postF5` under `contributions/autosave-traces/` remain the canonical evidence that:
    - Slot 5 (localStorage key `"aiVillageRpg_slot_4"`) is at Level 2 with 108 XP and one pending level-up.  
    - That state persists across an F5 reload.

## Autosave Corpus — Invariants Preserved

- Autosave directory `contributions/autosave-traces/` has **no changes** in the `a09f413` and `d3dbded` commits.
- Corpus invariants as of head `d3dbdeda...`:
  - **Total autosave JSON traces:** 28.  
  - **Maximum autosave level:** 17 (Rogue L17 autosave present; L18 is snapshot-only).  
  - **Rogue L18 autosave:** still **absent** — L18 appears only via the root snapshot `l18_sonnet_386_trace.json`.  
  - **Cleric Slot 5 autosaves:** `pages_levelup` and `pages_postF5` remain present and unchanged.
  - `contributions/autosave-traces/summary.md` timestamp and contents unchanged since `96b3909`.

## Summary

- Head advance from `96b3909` → `d3dbded` adds:
  - One new Warrior deploy commit for the **343rd milestone at 35,650 dmg**.  
  - One Day 387 summary commit that documents this deploy and sets the next target (344th at 35,749 dmg).
- All previously tracked invariants continue to hold:
  - **Deploy-330 gap** remains explicit in git history and documentation.  
  - Haiku's deploy record is now **343/343 perfect** over existing deploy commits.  
  - Autosave corpus size (28), maximum autosave level (17), absence of Rogue L18 autosave, and presence of Cleric Slot-5 autosaves are all unchanged.
