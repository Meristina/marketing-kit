"""
MISSION RUNNER — deterministic control loop + Mission Dossier + optional Direction Check (OpenAI port)

The army's spine. Where commander.py *defines* the commander agent, this runner *drives the
mission*: it holds the Mission Dossier (living state), runs the army, offers an OPTIONAL Direction
Check after strategy/positioning, runs the Inspector, parses the verdict, and controls re-entry and
the iteration cap. The commander agent is the brain within a pass; this harness owns the loop --
see agents/commander-marketing.md ("Mission Dossier & control loop", "DIRECTION CHECK").

MARKETING VARIANT (differs from Solve-Kit on purpose): this army produces *deliverables* — it does
NOT spend budget or launch live — so there is NO mandatory human go/no-go gate. Instead, a LIGHT,
OPTIONAL Direction Check is offered after Phase 2 (validate positioning + strategy before the heavy
build). It is non-blocking by default (auto-proceed); pass an interactive checker to enable a steer.

Two stages per iteration:
  STRATEGISE (Phases 0-2: frame -> insight & research -> strategy & positioning)
  --- optional Direction Check: present positioning + strategy, offer to confirm/steer (non-blocking) ---
  BUILD      (Phases 3-6: brand-building -> demand -> lifecycle -> measurement)
Then the FINAL Inspector verdict gates delivery.

Run:  python -m marketing_kit.mission "Describe the marketing goal here"
(Requires `pip install openai-agents` and OPENAI_API_KEY.)
"""

import json
import sys

from agents import Runner

from .commander import commander
from .inspector import inspector

MAX_ITERS = 3  # iteration cap -- deliver-with-residual-risk rather than thrash forever


def new_dossier(goal: str) -> dict:
    """The single living-state artifact carried across the whole mission."""
    return {
        "goal": goal,
        "context": None,           # product/audience/market/B2B-B2C/stage detected in framing
        "baseline": None,          # current marketing metrics where they exist (set in Phase 1)
        "assumptions": [],
        "decisions": [],           # decisions per phase
        "sources": [],
        "open_to_verify": [],
        "direction_check": None,   # the optional steer recorded after Phase 2 (if used)
        "verdicts": [],            # Inspector verdicts + required fixes, per iteration
        "iteration": 0,
    }


def _dossier_block(dossier: dict) -> str:
    return json.dumps(dossier, ensure_ascii=False, indent=2)


def strategise_brief(dossier: dict, required_fixes: list) -> str:
    """Stage 1 -- run Phases 0-2 and STOP at the optional Direction Check with a strategy package."""
    parts = [
        "MISSION DOSSIER (read in; do not re-ask what is already here):",
        _dossier_block(dossier),
        "\nRun PHASES 0-2 ONLY: frame, insight & research (Officer 1), strategy & positioning "
        "(Officer 2) -- with the quick Inspector GATE after Phase 2. STOP at the Direction Check; "
        "do NOT start the brand/demand build (Phase 3+).",
        "\nReturn a STRATEGY PACKAGE in the user's language: the detected context, the customer's "
        "job(s)/CEPs, the chosen segment/target, the positioning (anchor + statement) and value "
        "proposition, and the top assumptions. Make sources and open-to-verify items explicit.",
    ]
    if required_fixes:
        parts.append(
            "\nRE-ENTRY -- resolve these before re-presenting (carry the dossier):\n- "
            + "\n- ".join(required_fixes)
        )
    return "\n".join(parts)


def build_brief(dossier: dict, strategy_package: str) -> str:
    """Stage 2 -- build on top of the (optionally steered) strategy: Phases 3-6."""
    return "\n".join([
        "MISSION DOSSIER:",
        _dossier_block(dossier),
        "\nThe strategy below is confirmed (with any steer recorded in the dossier). Run PHASES "
        "3-6: brand-building (Officer 3) and demand & activation (Officer 4) TOGETHER for the "
        "60:40 balance, then lifecycle & retention (Officer 5), then measurement (Officer 6).",
        "\nCONFIRMED STRATEGY:\n" + strategy_package,
        "\nReturn the full deliverable in the user's language: the strategy recap, the brand-"
        "building plan, the activation plan, the lifecycle/retention program, and the measurement "
        "plan (triangulated), with sources and open-to-verify items explicit.",
    ])


def parse_verdict(text: str) -> str:
    """Map the Inspector's free text to a machine verdict. Order matters (VETO first)."""
    upper = (text or "").upper()
    if "VETO" in upper:
        return "VETO"
    if "PASS WITH FIXES" in upper or "PASS-WITH-FIXES" in upper:
        return "PASS_WITH_FIXES"
    if "PASS" in upper:
        return "PASS"
    return "UNCLEAR"


def extract_required_fixes(text: str) -> list:
    """Best-effort pull of the required-fix bullet lines from the Inspector output."""
    fixes = []
    for line in (text or "").splitlines():
        s = line.strip().lstrip("-*•").strip()
        if s and any(s.upper().startswith(p) for p in ("FIX", "REQUIRED", "BLOCK")):
            fixes.append(s)
    return fixes


# ----- Direction Check functions (injectable; OPTIONAL and NON-BLOCKING by default) ----------

def auto_proceed(strategy_package: str) -> tuple:
    """Default: no human gate. This army produces deliverables, so it proceeds without approval."""
    return ("PROCEED", "auto-proceed (no mandatory direction check)")


def console_direction_check(strategy_package: str) -> tuple:
    """Optional interactive light check: show the strategy, offer to confirm or steer.

    Recommended for high-stakes / non-obvious positioning; still NON-BLOCKING -- the default is to
    proceed. Returns ("PROCEED", note) or ("STEER", note); a STEER re-enters the strategy stage.
    """
    print("\n=== DIRECTION CHECK (optional) — confirm or steer the strategy before the build ===")
    print(strategy_package)
    raw = input("\nProceed to the build, or steer the strategy? [PROCEED / STEER] (default PROCEED): ").strip().lower()
    note = input("Steer/note (optional): ").strip()
    if raw in ("steer", "s", "revise", "r"):
        return ("STEER", note)
    return ("PROCEED", note)  # default: proceed (non-blocking)


# ----- The mission loop -----------------------------------------------------------

def run_mission(goal: str, direction_check_fn=auto_proceed) -> dict:
    """Drive the full loop with an OPTIONAL direction check before the build. Returns the dossier."""
    dossier = new_dossier(goal)
    required_fixes: list = []
    deliverable = ""

    while dossier["iteration"] < MAX_ITERS:
        dossier["iteration"] += 1
        print(f"\n=== ITERATION {dossier['iteration']}/{MAX_ITERS} ===")

        # STAGE 1 -- STRATEGISE (Phases 0-2). The commander stops at the Direction Check.
        strategy = Runner.run_sync(commander, strategise_brief(dossier, required_fixes))
        strategy_package = strategy.final_output

        # Direction Check -- OPTIONAL and non-blocking (unlike Solve-Kit's mandatory HITL gate).
        choice, note = direction_check_fn(strategy_package)
        dossier["direction_check"] = {"iteration": dossier["iteration"], "choice": choice, "note": note}
        print(f"Direction check: {choice}" + (f" — {note}" if note else ""))

        if choice == "STEER":
            required_fixes = ["Direction steer before the build: " + (note or "steer the strategy")]
            continue  # loop back to the strategy stage with the human's steer

        # STAGE 2 -- BUILD (Phases 3-6).
        execution = Runner.run_sync(commander, build_brief(dossier, strategy_package))
        deliverable = strategy_package + "\n\n---\n\n" + execution.final_output

        # FINAL Inspector verdict of record (the harness owns it).
        inspection = Runner.run_sync(
            inspector,
            "MODE: FINAL. Inspect this deliverable (sources / compliance / quality) and end with a "
            "clear verdict line -- PASS, PASS WITH FIXES, or VETO -- plus the required fixes as "
            "bullet lines:\n\n" + deliverable,
        )
        verdict = parse_verdict(inspection.final_output)
        required_fixes = extract_required_fixes(inspection.final_output)
        dossier["verdicts"].append({
            "iteration": dossier["iteration"],
            "verdict": verdict,
            "required_fixes": required_fixes,
        })
        print(f"Inspector verdict: {verdict}  ({len(required_fixes)} required fix(es))")

        if verdict == "PASS":
            dossier["delivered"] = deliverable
            return dossier
        # else loop with the fixes carried in the dossier.

    # Iteration cap reached: deliver best result WITH residual risk stated.
    dossier["delivered"] = deliverable
    dossier["residual_risk"] = (
        "Iteration cap reached without a clean PASS. Delivered the best result; "
        f"unresolved required fixes: {required_fixes}; open_to_verify: {dossier['open_to_verify']}."
    )
    return dossier


def main() -> None:
    """Console-script entry point (`marketing-kit-mission "<goal>"`)."""
    goal = sys.argv[1] if len(sys.argv) > 1 else "We have a marketing goal: ... (describe it)"
    final = run_mission(goal)  # non-blocking auto-proceed by default; inject a checker to steer
    print("\n=== DELIVERED ===")
    print(final.get("delivered", "(nothing)"))
    if final.get("residual_risk"):
        print("\n=== RESIDUAL RISK ===")
        print(final["residual_risk"])


if __name__ == "__main__":
    main()
