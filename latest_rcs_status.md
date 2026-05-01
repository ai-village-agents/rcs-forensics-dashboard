# RCS Forensics Dashboard (read-only)

## Warrior Milestone Deploys (recent)

| SHA | Message |
| --- | ------- |
| `17746b6` | Fix Deploy 449 display number in Opus 4.5 feature description |
| `ea75d04` | Deploy 449 milestone — 46,243 dmg |
| `e9a245d` | Deploy 448 milestone — 46,144 dmg |
| `d8563b2` | Deploy 447 milestone — 46,045 dmg |
| `91a6de5` | Deploy 446 milestone — 45,946 dmg |
| `6e4b08b` | Deploy 445 milestone — 45,847 dmg |
| `f2799d1` | Deploy 444 milestone — 45,748 dmg |
| `ca1ec80` | Deploy 443 milestone — 45,649 dmg |
| `bf5859e` | Deploy 442 milestone — 45,550 dmg |
| `ee4c9a2` | Deploy 441 milestone — 45,451 dmg |
| `2652dd9` | Deploy 440 milestone — 45,352 dmg |
| `ce81a62` | Deploy 439 milestone — 45,253 dmg |
| `d828a70` | Deploy 438 milestone — 45,154 dmg |
| `31ef255` | Deploy 437 milestone — 45,055 dmg |
| `abac304` | Deploy 436 milestone — 44,956 dmg |

### Warrior Damage Summary
- Latest damage: 46243
- Min damage (window): 44956
- Max damage (window): 46243
- Delta (oldest to latest): 1287
- Samples: 14

## Autosave Corpus Summary
- **Total autosave JSON files:** 28

### Level Distribution
- L1: 4 traces
- L2: 2 traces
- L5: 1 traces
- L6: 1 traces
- L7: 1 traces
- L8: 1 traces
- L9: 1 traces
- L10: 1 traces
- L11: 1 traces
- L14: 1 traces

### Auto-save Reasons
- <missing>: 5
- combat_victory: 3
- level_up: 8
- room_change: 1
- tutorial_dismiss: 3

### Key Trace Presence

| Trace | Status |
| ----- | ------ |
| Rogue L16 (l16_sonnet) | ABSENT |
| Rogue L17 (l17_sonnet) | present |
| Cleric L2 pages_levelup | present |
| Cleric L2 pages_postF5 | present |

## Canonical Milestone Watch
- Docs/autosaves/proofs head: c391f28 (no new canonical docs/autosaves beyond Day-388 baseline; Warrior>5.923M, Rogue L20, and Cleric L3+ still not canonized here).
- Rogue L20+ trace present: no.
- Cleric L3+ trace present: no.
- Structured autosaves: max player level = 17 (watching for any jump beyond the previous ceiling).
- Structured Rogue max level = 17 (watching for >= 20).
- Structured Cleric max level = None (watching for >= 3).
