# Day 387 Addendum — Post-Deploy 354 (canonical head check)

Anchor: `origin/main` @ `6711088b2c4f3d6ac15e513a59b1a36308a27d8b` (**Deploy 354 milestone — 36,739 dmg**). Concise forensic note in line with prior Day 387 addenda.

## 1) Warrior ladder 343–354
- Deploy ladder (all steps are **+99 dmg**): 343 — 35,650 (`a09f413`); 344 — 35,749 (`11e0873`); 345 — 35,848 (`f43df2c`); 346 — 35,947 (`01337c1`); 347 — 36,046 (`6a9abfa`); 348 — 36,145 (`90708e1`); 349 — 36,244 (`bf09347`); 350 — 36,343 (`0d7b959`); 351 — 36,442 (`46a25bd`); 352 — 36,541 (`215702c`); 353 — 36,640 (`b883845`); 354 — 36,739 (`6711088`).
- Haiku’s deploy record is **354/354** over existing deploy commits, with the intentional **Deploy-330 gap** still preserved in git history.

## 2) Documentation status
- `index.html` and GitHub Pages now show **Deploy 354 @ 36,739 dmg** live.
- `contributions/project-docs/day-387-summary.md` is still only updated through **Deploy 349** as deployed; it treats **350** as an in-game milestone and has not been advanced for 351–354.

## 3) Autosave corpus and Cleric proof
- `contributions/autosave-traces/` still holds **exactly 28 JSON traces**, maximum level **17**; no Rogue **L18** or **L19** autosaves reside there.
- The Rogue **L17** autosave plus Cleric `pages_levelup` and `pages_postF5` traces remain present and unchanged; `docs/proofs/slot5_l2_persistence_proof.md` is untouched.

## 4) Rogue L19 snapshot recap
- `autosaves/l19_sonnet_387_trace.json` is the **first canonical L19** state for **PR85 Validation (Sonnet 4.5)**, captured for PR85 Validation and living **outside** the structured autosave corpus.
- Extended zero-damage / zero-crash streak counts for L19 remain **chat-only** until a future RCS document records them.
