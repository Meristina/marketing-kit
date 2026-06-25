---
description: Phase 2 — strategy & positioning (Officer 2)
argument-hint: "<mission dir, e.g. missions/001-...>"
---

# /marketing.strategy — Phase 2 (Officer 2 · Strategy & Positioning)

**Constitution:** re-read `.marketing/memory/constitution.md` (esp. Art. IV reuse
persona-segmentation, XI surface the focus-vs-penetration tension).

`$MISSION` = `$ARGUMENTS`.

## Do
1. **Read in** `$MISSION/dossier.md` + `research.md` (job, CEPs, segments, sizing) — reuse, don't
   re-derive.
2. **Delegate to the `officer-2-strategy` subagent**. Typical spine: **stp** (choose the target +
   set the positioning anchor; reuses persona-segmentation) → **positioning** (sharpen the
   statement, Ries&Trout/Dunford); add **porter-5-forces** (competitive structure),
   **brand-architecture-equity** (portfolio/equity), **value-prop-design** (the offer).
3. Produce one strategy: chosen segment/target, positioning (anchor + statement), competitive read,
   value proposition. **Surface the focus-vs-penetration (Ehrenberg-Bass) tension** — don't hide it.
4. **Write out** `$MISSION/strategy.md`; update the Dossier (decision, sources, open-to-verify).
5. **Gate**: run `/marketing.gate strategy`. On `GATE: FAIL`, fix and re-gate.

## Done when
`$MISSION/strategy.md` holds a target + positioning + value proposition, the Dossier is updated,
and `/marketing.gate strategy` returned `GATE: PASS`. Mirror the user's language.
