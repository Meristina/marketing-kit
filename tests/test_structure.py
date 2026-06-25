"""Structural invariants — pure file parsing, no imports, no SDK, no network.

Doubles as the durable consistency audit: wiring completeness, grade parity
(py model= <-> md frontmatter model:), shared-arsenal sanity, counts.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / "agents"
PKG = ROOT / "marketing_kit"
OFFICERS = PKG / "officers"
SOLDIERS = PKG / "soldiers"
SKILLS = ROOT / "skills"

GRADE = {"ELITE": "opus", "STANDARD": "sonnet"}  # py grade token -> md model

N_SOLDIERS = 30
N_OFFICERS = 6


def _py_model(path: Path) -> str:
    # Models are resolved via ELITE/STANDARD tokens (marketing_kit/models.py, env-configurable);
    # the grade token is what must mirror the md frontmatter.
    m = re.search(r"model=(ELITE|STANDARD)\b", path.read_text(encoding="utf-8"))
    return m.group(1) if m else ""


def _md_model(path: Path) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("model:"):
            return line.split(":", 1)[1].strip()
    return ""


def _soldier_pys():
    return sorted(p for p in SOLDIERS.glob("soldier_*.py") if p.stem != "__init__")


def _officer_pys():
    return sorted(OFFICERS.glob("officer_*.py"))


# ---- counts -----------------------------------------------------------------

def test_counts():
    assert len(list(AGENTS.glob("soldier-*.md"))) == N_SOLDIERS
    assert len(_soldier_pys()) == N_SOLDIERS
    assert len(list(AGENTS.glob("officer-*.md"))) == N_OFFICERS
    assert len(_officer_pys()) == N_OFFICERS
    # one SKILL.md per soldier method (no extra meta-skill on the marketing side)
    assert len(list(SKILLS.glob("*/SKILL.md"))) == N_SOLDIERS


# ---- wiring: every soldier is invoked by >=1 officer ------------------------

def test_every_soldier_wired():
    officer_text = "\n".join(p.read_text(encoding="utf-8") for p in _officer_pys())
    for sp in _soldier_pys():
        assert sp.stem in officer_text, f"{sp.stem} is never imported/used by an officer"


# ---- wiring: commander invokes all 6 officers + the inspector ---------------

def test_commander_wires_full_chain():
    txt = (PKG / "commander.py").read_text(encoding="utf-8")
    for n in range(1, N_OFFICERS + 1):
        assert f"officer_{n}.as_tool" in txt, f"officer_{n} not wired into commander"
    assert "inspector.as_tool" in txt, "inspector not wired into commander"


# ---- grade parity: py model= <-> md frontmatter model: ----------------------

def _md_for(py: Path) -> Path:
    if py.name == "commander.py":
        return AGENTS / "commander-marketing.md"
    if py.name == "inspector.py":
        return AGENTS / "inspector.md"
    return AGENTS / (py.stem.replace("_", "-") + ".md")


def test_grade_parity():
    units = [PKG / "commander.py", PKG / "inspector.py", *_officer_pys(), *_soldier_pys()]
    assert len(units) == 2 + N_OFFICERS + N_SOLDIERS  # commander + inspector + officers + soldiers
    for py in units:
        md = _md_for(py)
        assert md.exists(), f"no md mirror for {py.name} (looked for {md.name})"
        py_m, md_m = _py_model(py), _md_model(md)
        assert py_m in GRADE, f"{py.name} has unexpected model {py_m!r}"
        assert GRADE[py_m] == md_m, f"grade mismatch {py.name}: py={py_m} md={md_m}"


# ---- name == file: py Agent name mirrors the file stem ----------------------

def test_name_matches_file():
    for sp in _soldier_pys():
        m = re.search(r'name="([^"]+)"', sp.read_text(encoding="utf-8"))
        assert m and m.group(1) == sp.stem, f"{sp.name}: agent name != file stem"


# ---- shared-arsenal sanity: known shared soldiers used by >=2 officers -------

def test_shared_arsenal():
    texts = {p.name: p.read_text(encoding="utf-8") for p in _officer_pys()}
    for shared in ("soldier_persona_segmentation", "soldier_value_prop_design"):
        used_by = [n for n, t in texts.items() if shared in t]
        assert len(used_by) >= 2, f"{shared} should be shared by >=2 officers, got {used_by}"


# ---- no flat (non-relative) intra-package imports leaked ---------------------

def test_no_flat_imports():
    flat = re.compile(r'^from (commander|inspector|officers|soldiers|models)\b', re.M)
    for py in PKG.rglob("*.py"):
        assert not flat.search(py.read_text(encoding="utf-8")), f"flat import in {py}"
