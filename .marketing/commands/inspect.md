---
description: Final quality gate (Inspector FINAL mode) — sources, compliance, quality; veto
argument-hint: "<mission dir, e.g. missions/001-...>"
---

# /marketing.inspect — final gate (Inspector, FINAL mode, veto power)

**Constitution:** re-read `.marketing/memory/constitution.md` — **Art. IX** (Inspector veto, FINAL
mode) + Art. I (sourcing) + Art. II (compliance).

`$MISSION` = `$ARGUMENTS`.

## Do
1. **Read** all mission artifacts (`dossier.md`, `research.md`, `strategy.md`, `brand.md`,
   `demand.md`, `lifecycle.md`, `measure.md` — whichever were produced).
2. **Delegate to the `inspector` subagent** in **FINAL mode** — the full three-check pass:
   - **Sources** — every metric/market-size/benchmark cites a real internet source; spot-check the
     riskiest by searching. Uncited/hallucinated → automatic **VETO**. Enforce the research
     doctrine (ESOV hedged; 95-5 ≠ budget split; attribution ≠ causal; loyalty ≠ growth engine; the
     CDP model is dated; refuted McKinsey forecast figures not cited).
   - **Compliance** — data & advertising law for the detected market (GDPR / CAN-SPAM / ePrivacy /
     **loi 09-08 / CNDP** / ad-claim substantiation / #ad disclosure / regulated sectors); flag
     where qualified human/legal review is needed. A material risk presented as safe → **VETO**.
   - **Quality** — devil's-advocate on the weakest points, then **converge**.
3. **Verdict**: `PASS` / `PASS WITH FIXES` / `VETO` + the prioritized required fixes (each concrete
   and checkable), with evidence for each finding.
4. **Log**: append the verdict + findings to `$MISSION/inspections.md` and the Dossier.

## On PASS-WITH-FIXES / VETO
Fix the **affected** phase only (re-run its command, carry the Dossier) and **re-inspect**. Loop,
capped at `MAX_ITERS=3`; if still failing, deliver the best result **with residual risk stated**.
Mirror the user's language.
