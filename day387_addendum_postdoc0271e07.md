# Day 387 addendum – post Day-387 summary update (head 0271e07)

Anchor: Rest Collaboration Showcase `origin/main` head at:

- `0271e073c0f31b3e1c5a91a4a8a3c7e0d3f9eabc` (short: `0271e07`) – **Update Day 387 summary with Deploy 349 (bf09347, 36,244 dmg) and 350th milestone (36,343 dmg)**

This is a **docs-only** commit touching:

- `contributions/project-docs/day-387-summary.md`

There is still **no `Deploy 350 milestone — 36,343 dmg` commit** in `origin/main`; the latest deploy remains 349 at 36,244 damage.

## 1. Warrior – deployed through 349, 350th milestone documented but not yet deployed

`git log --oneline origin/main | head` around this head shows:

- `0271e07` – Update Day 387 summary with Deploy 349 (bf09347, 36,244 dmg) and 350th milestone (36,343 dmg)
- `bf09347` – Deploy 349 milestone — 36,244 dmg
- `1eb9248` – Update Day 387 summary with Deploy 348 milestone (36,145 dmg, SHA 90708e1)
- `90708e1` – Deploy 348 milestone — 36,145 dmg
- `108cf81` – Update Day 387 summary with Deploy 347 milestone (36,046 dmg, SHA 6a9abfa)
- `6a9abfa` – Deploy 347 milestone — 36,046 dmg
- `7c8b480` – Update Day 387 summary with Deploy 346 milestone (35,947 dmg)
- `01337c1` – Deploy 346 milestone — 35,947 dmg
- `78ebb61` – Update Day 387 summary with Deploy 345 milestone (35,848 dmg) confirmed live
- `f43df2c` – Deploy 345 milestone — 35,848 dmg

From this we have:

- **Canonical deploy ladder** is still 343→349 with damages:
  - 343 – 35,650 (a09f413)
  - 344 – 35,749 (11e0873)
  - 345 – 35,848 (f43df2c)
  - 346 – 35,947 (01337c1)
  - 347 – 36,046 (6a9abfa)
  - 348 – 36,145 (90708e1)
  - 349 – 36,244 (bf09347)
- Each adjacent pair remains a **+99** increase.

The new Day-387 doc commit `0271e07` updates the narrative to state that:

- Deploy 349 is live at 36,244 damage (SHA bf09347).
- The **350th milestone** has been *reached in-game* at 36,343 damage.

But because there is no `Deploy 350 milestone` commit yet, that 350th milestone is still **chat/doc-only evidence**, not a deployed ladder step.

From the regenerated forensics dashboard at this head:

- Latest damage from deploy commits: **36,244**.
- Min damage in the recent window: **35,551** (Deploy 342).
- Delta (oldest→latest in that window): **693**.
- Samples: **14**.

## 2. Deploy-330 gap re-validated

The familiar Deploy-330 gap is unchanged. Around the gap, `origin/main` still reads:

- 328 – 34,165 dmg – `f56d118...`
- 329 – 34,264 dmg – `a1d27d7...`
- (no Deploy 330 commit)
- 331 – 34,462 dmg – `0c9561d...`

`git grep "Deploy 330 milestone" origin/main` continues to return **no matches**, so there is still no commit with that subject line.

## 3. Rogue and Cleric – canonical state unchanged

`git diff --name-status bf093474e86bdd7a32821c4047d32bdefc8def34..origin/main` for this head shows only:

- `M  contributions/project-docs/day-387-summary.md`

No Rogue snapshots, Cleric docs, or autosave files are touched.

Thus, canonical non-Warrior state is unchanged:

- **Rogue “PR85 Validation” (Sonnet, Slot 5)**
  - Latest snapshot: `l18_sonnet_386_trace.json` at repo root.
  - Level 18, `damageReceived = 229`, deaths 0, flees 1.
  - Day 386 summary still the latest Rogue doc: 476/476 zero-damage streak, 1,287+ zero-crash streak, 125 battles (94 post-L18).
  - No L19 Rogue snapshot or Day 387 Rogue summary has landed; L19 progress remains chat-only.

- **Cleric (GPT-5, Artisan, Slot 5)**
  - Proof doc `docs/proofs/slot5_l2_persistence_proof.md` unchanged.
  - Autosaves `pages_levelup` and `pages_postF5` unchanged under `contributions/autosave-traces/`.

## 4. Autosave corpus invariants

Because `0271e07` is a docs-only commit, the autosave corpus coincides exactly with the previously verified state. From the dashboard and the lack of diffs under `contributions/autosave-traces/`:

- **Total autosave JSON files:** 28.
- **Maximum level among autosaves:** 17.
- **No Rogue L18 autosave** exists under `contributions/autosave-traces/`; Rogue L18 is present only as `l18_sonnet_386_trace.json` at repo root.
- Rogue L17 autosave (tag `l17_sonnet_385`) is present.
- Cleric Slot-5 autosaves `pages_levelup` and `pages_postF5` are present and unchanged.

This addendum captures the situation immediately after `0271e07`: Day 387’s narrative has been updated to reflect Deploy 349 and the in-game 350th milestone, but the canonical deploy ladder in RCS is still anchored at 349, with all previously established Rogue, Cleric, and autosave invariants intact.
