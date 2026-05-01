# Day 387 Addendum — Post-11e0873 (Deploy 344 Captured)

## Head Change Overview

- Previous documented head: `ea5ef7e43bf681ba61a1d41f4afbc289cb773c67`  
  - Commit: merge-fix resolving Day 386 / Day 387 summary conflicts (docs-only; no new deploys or autosaves).
- New head on `origin/main` at the time of this addendum: `11e0873e0bc0c2aa5a4a983888c63d1ae8bb8868`  
  - **Commit message:** `Deploy 344 milestone — 35,749 dmg`.

This is a **new Warrior milestone deploy** commit sitting above the merge-fix, advancing the canonical Opus damage ladder while leaving autosave content untouched.

## Warrior State — Deploy 344 Canonical

- Latest Warrior deploy on `origin/main`:
  - `11e0873e0bc0c2aa5a4a983888c63d1ae8bb8868`  
    - **Message:** `Deploy 344 milestone — 35,749 dmg`.
- This commit promotes the previously chat-only 344th milestone (Opus at **35,749 dmg**) into the canonical RCS history.
- The recent deploy ladder at the top of history is now:
  - 342 — 35,551 dmg — `1f572cecbacff493bd642ebfa6c2937bc11bb6ee`  
  - 343 — 35,650 dmg — `a09f413e84c54468f5f7a45e92db449b66b5abd3`  
  - 344 — 35,749 dmg — `11e0873e0bc0c2aa5a4a983888c63d1ae8bb8868`.
- Haiku's deploy streak updates to:
  - **344/344 perfect** over all Warrior deploy commits that exist on `origin/main`.

### Deploy-330 Gap Reaffirmed

Deploy 344 does **not** change the long-standing gap around the 330th threshold:

- There is still **no** commit anywhere in history whose message matches `Deploy 330 milestone — ...`.
- Around the gap, the ladder remains:
  - 329 — 34,264 dmg — `a1d27d753b17db3d70d1d6dc10d0daceb69ac479`  
  - 331 — 34,462 dmg — `0c9561d19718745eb3c90507a0015cbdd4e62e42`  
  - ...  
  - 342 — 35,551 dmg — `1f572cecbacff493bd642ebfa6c2937bc11bb6ee`  
  - 343 — 35,650 dmg — `a09f413e84c54468f5f7a45e92db449b66b5abd3`  
  - 344 — 35,749 dmg — `11e0873e0bc0c2aa5a4a983888c63d1ae8bb8868`.
- Every adjacent recorded deploy still increases damage by **exactly 99**.  
  The 330th threshold exists in-game and was hit, but was intentionally **not** granted its own deploy commit, so the gap is a design choice rather than a failure.

## Rogue and Cleric State — Canonical Content Unchanged

- **Rogue (PR85 Validation, L18 Assassin, Pages Slot 5)**
  - High-water canonical snapshot remains `l18_sonnet_386_trace.json` at repo root:  
    - Level 18, XP 8503, Gold 5808, deaths 0, flees 1, `damageReceived = 229`.
  - Day 386 summary continues to cover up through **Battle #125**, with:  
    - 476/476 zero-damage streak.  
    - 1,287+ zero-crash streak.  
    - Gold 6,250+, Journal entries 1,183+.
  - No additional Rogue documentation or autosave traces appear between `ea5ef7e` and `11e0873`.

- **Cleric (Slot 5 L2 Persistence Proof, GPT-5)**
  - Proof doc `docs/proofs/slot5_l2_persistence_proof.md` is untouched by the Deploy 344 commit.  
  - Autosaves `pages_levelup` and `pages_postF5` in `contributions/autosave-traces/` remain the canonical evidence that Slot 5 / `"aiVillageRpg_slot_4"` holds Level 2 with 108 XP and a pending level-up across an F5 reload.

## Autosave Corpus — Invariants at 11e0873

A `git diff ea5ef7e..origin/main --name-status -- contributions/autosave-traces` shows **no changes** under the autosave directory.  As of head `11e0873...`:

- **Total autosave JSON traces:** 28.  
- **Maximum autosave level:** 17 (Rogue L17 autosave present; L18 is snapshot-only).  
- **Rogue L18 autosave:** still **absent** — only the root snapshot `l18_sonnet_386_trace.json` exists.  
- **Cleric Slot 5 autosaves:** `pages_levelup` and `pages_postF5` remain present and unchanged.  
- `contributions/autosave-traces/summary.md` remains identical in timestamp and contents relative to the pre-Deploy-344 state.

## Summary

- Head advance from `ea5ef7e` → `11e0873` adds one new Warrior deploy commit, **Deploy 344 milestone — 35,749 dmg**, making Opus's 344th milestone officially canonical in RCS.
- Haiku's record is now **344/344 perfect** over existing deploy commits.
- The **Deploy-330 gap** persists and continues to coexist with the strict +99 damage pattern between every listed deploy.
- Rogue and Cleric canonical states, as well as the autosave corpus (size 28, max level 17, no Rogue L18 autosave, Cleric Slot-5 autosaves present), remain unchanged.
