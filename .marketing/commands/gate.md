---
description: Quick quality gate (Inspector GATE mode) between phases — definition-of-done + sourcing
argument-hint: "<phase: strategy | demand>  [mission dir]"
---

# /marketing.gate — quick gate (Inspector, GATE mode)

**Constitution:** re-read `.marketing/memory/constitution.md` — **Art. IX** (Inspector veto) +
Art. I (sourcing).

`$ARGUMENTS` = the phase just finished (`strategy` after Phase 2, `demand` after Phase 4), plus the
mission dir if not the current one.

## Do
1. **Delegate to the `inspector` subagent** in **GATE mode** — a fast checkpoint on THAT phase's
   output so a weak phase can't poison the downstream. Check only:
   - (1) is the phase's **definition of done** met?
   - (2) any **unsourced fact / fabricated number / invented citation**?
2. Return **`GATE: PASS`** or **`GATE: FAIL`** + the 1–3 must-fix items. No full compliance sweep,
   no deep devil's-advocate here.

## On GATE: FAIL
The relevant officer fixes the phase output and re-runs this gate before moving on. Mirror the
user's language.
