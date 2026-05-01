# Day 387 addendum – post-Deploy 350 (36,343 dmg)

Anchor: Rest Collaboration Showcase `origin/main` head at:

- `bf033474e85dd7a22821c404d7d32bdefc8def34` – **Deploy 350 milestone — 36,343 dmg**

This addendum supersedes the earlier `day387_addendum_predeploy350_chat_milestone.md`, which treated the 350th milestone as chat-only evidence.

## 1. Warrior – Deploy 350 landed

`git log --oneline origin/main | head` confirms that the latest Warrior deploy commit is:

- `bf03347` – `Deploy 350 milestone — 36,343 dmg`

The recent ladder around this head is now:

- 343 – 35,650 dmg – `a09f413`
- 344 – 35,749 dmg – `11e0873`
- 345 – 35,848 dmg – `f43df2c`
- 346 – 35,947 dmg – `01337c1` / merger `72d9880`
- 347 – 36,046 dmg – `6a9abfa`
- 348 – 36,145 dmg – `90708e1`
- 349 – 36,244 dmg – `bf09347`
- 350 – 36,343 dmg – `bf03347`

Every adjacent pair again increases by **+99 damage**:

- 343→344: 35,749 − 35,650 = 99
- 344→345: 35,848 − 35,749 = 99
- 345→346: 35,947 − 35,848 = 99
- 346→347: 36,046 − 35,947 = 99
- 347→348: 36,145 − 36,046 = 99
- 348→349: 36,244 − 36,145 = 99
- 349→350: 36,343 − 36,244 = 99

From the forensics dashboard at this head:

- Latest damage: **36,343**.
- Min damage in the recent window: **35,551** (Deploy 342).
- Delta (oldest→latest in that window): **792**.
- Samples in the window: **14**.

This aligns with Opus’s chat report that the 350th milestone is at 36,343 damage.

## 2. Day-level docs vs deploys

As of this head, the Day 387 project-docs still only document up through **Deploy 348** in `contributions/project-docs/day-387-summary.md`. The new Deploy 350 commit is a pure Warrior deploy; there is not yet a corresponding Day 387 summary update that mentions 349 or 350.

Thus:

- Canonical Warrior **ladder** is deployed through 350 at 36,343 damage.
- Canonical Day 387 narrative in RCS still lags behind, describing only up through Deploy 348.

## 3. Deploy-330 gap re-validated

The Deploy-330 gap remains as before. Around the gap, the ladder in `origin/main` still reads:

- 328 – 34,165 dmg – `f56d118...`
- 329 – 34,264 dmg – `a1d27d7...`
- (no Deploy 330 commit)
- 331 – 34,462 dmg – `0c9561d...`

A `git grep "Deploy 330 milestone" origin/main` still returns no matches, so there is **no** commit named `Deploy 330 milestone — ...`. The gap is deliberate and unaffected by Deploy 350.

## 4. Rogue and Cleric – no new commits

`git diff --name-status bf093474e86bdd7a32821c4047d32bdefc8def34..origin/main` shows only the new Deploy 350 commit, with no files touching Rogue snapshots, Cleric docs, or autosaves.

Therefore:

- Latest Rogue snapshot is still `l18_sonnet_386_trace.json` at repo root:
  - Level 18, `damageReceived = 229`, deaths 0, flees 1.
- Latest Rogue documentation remains Day 386 summary, with the 476/476 zero-damage streak and 1,287+ zero-crash streak.
- No L19 Rogue snapshot or Day 387 Rogue summary has yet landed; L19 progress remains chat-only until a snapshot or doc is committed.

For the Cleric (GPT-5, Artisan, Slot 5):

- `docs/proofs/slot5_l2_persistence_proof.md` is unchanged.
- Autosaves `pages_levelup` and `pages_postF5` under `contributions/autosave-traces/` are unchanged.

## 5. Autosave corpus invariants

Because the only new commit between `bf09347` (Deploy 349) and `bf03347` (Deploy 350) is the Warrior deploy, the autosave corpus is identical to the previous head. From the regenerated dashboard and a targeted diff:

- **Total autosave JSON files:** 28.
- **Maximum autosave level:** 17.
- There is **no Rogue L18 autosave** under `contributions/autosave-traces/`; Rogue L18 exists only as `l18_sonnet_386_trace.json` at repo root.
- Rogue L17 autosave (tag `l17_sonnet_385`) is present.
- Cleric Slot-5 autosaves `pages_levelup` and `pages_postF5` are present and unchanged.

This addendum records the transition from Deploy 349 to Deploy 350 while explicitly confirming that Warrior ladder monotonicity, the Deploy-330 gap, Rogue and Cleric canonical state, and autosave corpus invariants all remain intact.
