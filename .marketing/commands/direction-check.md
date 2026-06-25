---
description: Optional, non-blocking Direction Check — confirm or steer the strategy before the build
argument-hint: "<mission dir, e.g. missions/001-...>"
---

# /marketing.direction-check — optional steer (NON-blocking)

**Constitution:** re-read `.marketing/memory/constitution.md` — **Art. VIII**: this army produces
deliverables, so there is NO mandatory go/no-go; this check is optional and non-blocking.

`$MISSION` = `$ARGUMENTS`.

This army produces *deliverables* (it doesn't spend budget or launch live), so there is **no
mandatory go/no-go**. This is a light, optional check — **recommended** when high-stakes or the
positioning is non-obvious; **skip** for small/clear briefs.

## Do
1. **Read in** `$MISSION/strategy.md` (target + positioning + value prop).
2. Present the positioning + strategy in one screen and **offer** the user to **confirm** or
   **steer** — default is to proceed.
3. **Write out**: record the steer (if any) in `$MISSION/dossier.md` → `direction_check`.
   - **PROCEED** → continue to `/marketing.brand` + `/marketing.demand`.
   - **STEER** → re-run `/marketing.strategy` carrying the Dossier (don't restart from scratch).

## Done when
`direction_check` is recorded in the Dossier and the user has chosen to proceed or steer. Mirror
the user's language.
