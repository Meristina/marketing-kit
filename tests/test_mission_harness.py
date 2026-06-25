"""End-to-end harness test for the mission loop — no SDK, no network, no API key.

We inject a fake `agents` module into sys.modules BEFORE importing marketing_kit.mission
(the package and its officers/soldiers all do `from agents import ...` at import time and
call `.as_tool()` while building the graph). Then we drive `run_mission` by scripting
`Runner.run_sync` outputs and injecting the `direction_check_fn`, covering the marketing
control-flow branches: PROCEED->PASS, STEER->loop, and VETO->iteration cap.

NB: unlike Solve-Kit there is NO mandatory HITL gate here — the Direction Check is optional
and non-blocking (default auto_proceed), so there is no NO-GO branch.

The `agents` SDK is stubbed in tests/conftest.py (shared, installed before any test imports).
"""

from marketing_kit import mission


class _Result:
    def __init__(self, final_output):
        self.final_output = final_output


class ScriptedRunner:
    """Returns scripted final_outputs in order; records the calls made."""

    def __init__(self, outputs):
        self.outputs = list(outputs)
        self.calls = []

    def run_sync(self, agent, inp):
        self.calls.append(getattr(agent, "name", None))
        return _Result(self.outputs.pop(0))


def _checker(sequence):
    """direction_check_fn returning (choice, note) from a scripted sequence."""
    seq = iter(sequence)

    def fn(_strategy_package):
        return (next(seq), "test")

    return fn


# ---- pure helpers ------------------------------------------------------------

def test_parse_verdict_priority():
    assert mission.parse_verdict("all good, PASS but also VETO on X") == "VETO"
    assert mission.parse_verdict("verdict: PASS WITH FIXES") == "PASS_WITH_FIXES"
    assert mission.parse_verdict("PASS-WITH-FIXES") == "PASS_WITH_FIXES"
    assert mission.parse_verdict("PASS") == "PASS"
    assert mission.parse_verdict("") == "UNCLEAR"


def test_required_fixes_extracted_by_prefix():
    txt = "intro\n- Required: cite the TAM figure\n- Fix: add opt-out\n- nice polish\n- BLOCKING: confirm scope"
    fixes = mission.extract_required_fixes(txt)
    assert len(fixes) == 3


def test_new_dossier_seeds_loop_contract():
    # the keys + defaults the control loop and serializer depend on
    d = mission.new_dossier("g")
    for key in ("goal", "context", "baseline", "direction_check", "verdicts", "iteration", "open_to_verify"):
        assert key in d
    assert d["goal"] == "g" and d["iteration"] == 0 and d["direction_check"] is None


def test_auto_proceed_is_non_blocking():
    choice, _ = mission.auto_proceed("strategy package")
    assert choice == "PROCEED"


# ---- the marketing control-flow branches ------------------------------------

def test_proceed_then_pass(monkeypatch):
    # iteration 1: strategise -> PROCEED -> build -> FINAL PASS
    runner = ScriptedRunner(["STRATEGY PACKAGE", "BUILD PLAN", "VERDICT: PASS"])
    monkeypatch.setattr(mission, "Runner", runner)
    d = mission.run_mission("goal", direction_check_fn=_checker(["PROCEED"]))
    assert "delivered" in d and "residual_risk" not in d
    assert d["direction_check"]["choice"] == "PROCEED"
    assert d["iteration"] == 1
    assert d["verdicts"][-1]["verdict"] == "PASS"


def test_default_is_auto_proceed(monkeypatch):
    # no direction_check_fn passed -> auto_proceed -> straight to build -> PASS
    runner = ScriptedRunner(["STRATEGY PACKAGE", "BUILD PLAN", "VERDICT: PASS"])
    monkeypatch.setattr(mission, "Runner", runner)
    d = mission.run_mission("goal")
    assert d["direction_check"]["choice"] == "PROCEED"
    assert "delivered" in d


def test_steer_then_proceed(monkeypatch):
    # iter1: strategise -> STEER (loop, no build). iter2: strategise -> PROCEED -> build -> PASS
    runner = ScriptedRunner(["STRAT1", "STRAT2", "BUILD", "VERDICT: PASS"])
    monkeypatch.setattr(mission, "Runner", runner)
    d = mission.run_mission("goal", direction_check_fn=_checker(["STEER", "PROCEED"]))
    assert d["iteration"] == 2
    assert "delivered" in d
    assert d["direction_check"]["choice"] == "PROCEED"
    # a STEER must NOT have run an inspection in iter1 (no build that round)
    assert len(d["verdicts"]) == 1


def test_veto_hits_iteration_cap(monkeypatch):
    # every iteration: strategise -> PROCEED -> build -> VETO ; MAX_ITERS -> residual_risk
    outputs = []
    for _ in range(mission.MAX_ITERS):
        outputs += ["STRAT", "BUILD", "VERDICT: VETO"]
    runner = ScriptedRunner(outputs)
    monkeypatch.setattr(mission, "Runner", runner)
    d = mission.run_mission("goal", direction_check_fn=_checker(["PROCEED"] * mission.MAX_ITERS))
    assert d["iteration"] == mission.MAX_ITERS
    assert "residual_risk" in d
    assert d["verdicts"][-1]["verdict"] == "VETO"
