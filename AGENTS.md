# AGENTS.md — working in Marketing-Kit

Instructions for coding agents (and humans) contributing to this repo. Read this first; it is the
cross-harness anchor (Claude Code, Codex, Cursor, Copilot, Gemini, OpenCode all read `AGENTS.md` or
its equivalent).

## What this is

A generalist, sector-agnostic **marketing agent army**: Commander → 6 Officers (one per phase) →
30 Soldiers (one per method) + a transverse Inspector with veto. Every unit is **portable** —
authored twice: `agents/*.md` (the harness mirror) and `marketing_kit/**/*.py` (the Agents-SDK
engine), with procedures in `skills/*/SKILL.md`. See `README.md` for the full picture.

## The binding rules — read before any change

- **`.marketing/memory/constitution.md`** — the 11-article cross-phase law. Non-negotiable:
  Art. I (no invented facts — source or tag `[assumption — verify]`), Art. IX (Inspector veto),
  Art. XI (60:40 balance + measurement triangulation + model both sides of the Binet&Field↔Sharp
  dispute). Art. VIII is the marketing inversion: **no mandatory HITL** — an optional, non-blocking
  Direction Check after Phase 2.
- **`docs/RESEARCH.md`** — the research-backed doctrine and the **refuted claims you must never
  cite** (e.g. "SOV is THE driver of growth"; a "B2B ~95:5 budget"; last-touch as causal; loyalty
  as the growth engine; the dated McKinsey CDP model; the refuted McKinsey forecast figures).

## Build & test

```bash
pip install -e ".[dev]"     # add ".[litellm]" for non-OpenAI providers
pytest                      # 26 offline tests — no SDK, no network, no API key needed
python -m py_compile $(find marketing_kit marketing_cli -name "*.py")
```

The engine (`marketing run` / `python -m marketing_kit.mission`) needs `openai-agents` +
a configured provider; the test suite does not (it stubs the SDK).

## Conventions (locked)

- **Files in English; runtime mirrors the user's language** (FR / AR / EN…).
- **Grades by depth of reasoning:** 🔵 standard (`STANDARD` ↔ md `model: sonnet`) vs 🎖️ elite
  (`ELITE` ↔ md `model: opus`). Models are env-configurable (`MK_ELITE_MODEL` / `MK_STANDARD_MODEL`).
- **Shared arsenal, no duplication:** one method = one soldier + one skill, reused across officers
  (e.g. `persona-segmentation` O1↔O2, `value-prop-design` O2↔O4).
- **Relative intra-package imports only** (`from ..models import ELITE`), never flat.
- Each soldier `.py` is an `Agent(name=, handoff_description=, instructions=, tools=[WebSearchTool()],
  model=ELITE|STANDARD)`; `name=` must equal the file stem.

## Repeatable pattern — add a soldier

1. `mkdir skills/<method>/` + write `skills/<method>/SKILL.md` (procedure + output format).
2. `agents/soldier-<method>.md` — frontmatter (name/description/model/color) + role, manual=skill,
   hard rules, output.
3. `marketing_kit/soldiers/soldier_<method>.py` — the `Agent` (mirror of the `.md`).
4. Wire it at the owning officer: `import` + `.as_tool(tool_name=..., tool_description=...)`.
5. Update `_ETAT_AVANCEMENT.md` (the local progress log, gitignored).

## Quality gate (run before presenting/committing)

- `py_compile` clean across `marketing_kit/` + `marketing_cli/`.
- **name == file** (py `name="soldier_x"` ↔ `soldier_x.py` ↔ `soldier-x.md`); **skill == dir**.
- **Grade parity:** py `model=ELITE|STANDARD` ↔ md `model: opus|sonnet`.
- Every soldier has a `handoff_description`; every soldier is wired into ≥1 officer; the commander
  wires all 6 officers + the inspector. (`tests/test_structure.py` enforces all of this.)
- `pytest` green.
- When you change tests, review them with the **`test-guard`** skill before committing (optional,
  local tooling — install with `npx skills add amElnagdy/guard-skills --skill test-guard`).

## Layout

```
agents/        harness mirror (commander, 6 officers, 30 soldiers, inspector)   *.md
skills/        one SKILL.md per method (30)
.marketing/    constitution + 11 slash-commands (the CLI's source of truth)
marketing_kit/ engine — commander · inspector · mission · models · officers/ · soldiers/
marketing_cli/ CLI — cli · scaffolder · integrations (6 harness adapters) · runner_bridge
docs/RESEARCH.md   the research-backed doctrine
tests/         offline structural + mission-harness + CLI tests
```
