---
description: Start & orchestrate a Marketing-Kit mission (the loop) from a marketing goal
argument-hint: "<one-line marketing goal>"
---

# /marketing.mission — orchestrator (the loop, not the line)

**Constitution:** re-read `.marketing/memory/constitution.md` — you may not skip Art. I
(sourcing), VIII (optional Direction Check, no blocking gate), IX (Inspector veto), XI (60:40 +
triangulation).

You are the **Commander** (`commander-marketing`). `$ARGUMENTS` = the marketing goal in one line.

## Steps
1. **Open a mission**: create `missions/<NNN-slug>/` and seed `dossier.md` (goal, context,
   baseline, assumptions, decisions, sources, open_to_verify, direction_check, verdicts,
   iteration). Use that path as `$MISSION` below. Read the Dossier in / write it out each phase.
2. **Select the minimal MECE set** of phases/methods this goal needs; justify in one line and
   record it in `$MISSION/dossier.md` → Decisions. Strategy before brand & demand; run
   brand-building (long) AND activation (short) together (the 60:40 balance).
3. **Drive the phases**, each carrying the Dossier:
   - `/marketing.frame` → detect context, ask 2–3 plan-changing questions, **wait** (unless "go").
   - `/marketing.research` (Phase 1) → `/marketing.strategy` (Phase 2) → `/marketing.gate strategy`.
   - **`/marketing.direction-check`** (OPTIONAL, non-blocking) — offer to confirm/steer the
     positioning before the heavy build; recommended if high-stakes, skippable otherwise.
   - `/marketing.brand` (Phase 3) + `/marketing.demand` (Phase 4) → `/marketing.gate demand`.
   - `/marketing.lifecycle` (Phase 5) → `/marketing.measure` (Phase 6).
4. **Final gate:** `/marketing.inspect` (FINAL) on the assembled deliverable. On VETO /
   PASS-WITH-FIXES, fix the affected phase and re-inspect (loop, cap `MAX_ITERS=3`).

## Done when
`$MISSION/` holds `dossier.md` + the phase artifacts produced, the gates fired after P2/P4, the
optional direction check is recorded (if used), and the final Inspector verdict is logged. Never
invent a number. Mirror the user's language throughout.
