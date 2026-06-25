# Marketing-Kit 🪖

A generalist, **sector-agnostic marketing agent army** (B2B + B2C, any market). One
disciplined, evidence-based doctrine — from insight to measurement — delivered by a chain of
command: a **Commander** → **6 Officers** (one per phase) → **30 Soldiers** (one per method) +
a transverse **Inspector** with veto power. **No invented facts**: every unit researches on the
internet and cites sources; the Inspector verifies sources, compliance, and quality before
anything ships.

Built on the same blueprint as [Solve-Kit](../solve-kit), applied to the marketing
strategy/campaign lifecycle. **Portable**: every unit exists twice — `agents/*.md` (the
agent-harness mirror: Claude, Codex, Cursor, Copilot, Gemini, OpenCode) and
`marketing_kit/**/*.py` (the reference engine on the Agents SDK) — with the procedures in
`skills/*/SKILL.md`.

## Chain of command

```
🔴 COMMANDER (commander-marketing)
 ├─ 🟠 Officer 1 · Insight & Research        JTBD · CEPs · persona/segmentation · market sizing · AI synthetic-audience
 ├─ 🟠 Officer 2 · Strategy & Positioning    STP · positioning · Porter · brand architecture/equity · value-prop design
 ├─ 🟠 Officer 3 · Brand-Building (long)     mental availability · emotional creative · ESOV · 95-5 future-memory · narrative · creator/influencer
 ├─ 🟠 Officer 4 · Demand & Activation (short) full-funnel paid · CRO · PLG · content/SEO · lead scoring/lifecycle
 ├─ 🟠 Officer 5 · Lifecycle & Retention     lifecycle/CRM/email · first-party/CDP · retention/loyalty · RevOps
 ├─ 🟠 Officer 6 · Measurement & Effectiveness incrementality · MMM · attribution · budget-balance · brand-tracking
 └─ 🛡️ Inspector · sources + compliance + quality (end of every loop, veto)
```

The doctrine reflects evidence-based brand science: it runs **both** long-term brand-building
and short-term demand activation (the ~60:40 balance), **triangulates** measurement
(incrementality = causal truth → MMM = allocator → attribution = biased diagnostic, never
alone), and treats the **Binet&Field ↔ Ehrenberg-Bass/Sharp** dispute as a feature — modelled,
not hidden. See [`docs/RESEARCH.md`](docs/RESEARCH.md).

## Grades & models

Every unit is graded by **depth of reasoning**: 🔵 standard vs 🎖️ elite. Models are
env-configurable (`marketing_kit/models.py`):

| Grade | Default model | Override |
|-------|---------------|----------|
| 🎖️ elite (`ELITE`) | `gpt-5` | `MK_ELITE_MODEL` |
| 🔵 standard (`STANDARD`) | `gpt-5-mini` | `MK_STANDARD_MODEL` |

Non-OpenAI providers via the LiteLLM extra, e.g.
`export MK_ELITE_MODEL="litellm/anthropic/claude-opus-4-20250514"`.

## Run it — the reference engine (optional)

The Python port is the executable reference engine, built on the Agents SDK. It is
**provider-neutral** — point the grades at any model via `marketing_kit/models.py` (and the
LiteLLM extra), so this is not tied to a single vendor.

```bash
pip install -e .                 # or:  pip install -e ".[litellm]"
export OPENAI_API_KEY=sk-...     # or the keys your configured provider needs
python -m marketing_kit.mission "Grow trial signups for our B2B analytics product in MENA"
# or, equivalent:
marketing-kit-mission "..."
```

`marketing_kit/mission.py` is the deterministic runner: it carries a **Mission Dossier**, runs
the army in two stages — **STRATEGISE** (Phases 0–2) → **BUILD** (Phases 3–6) — runs the
**Inspector** (FINAL), parses the verdict (PASS / PASS-WITH-FIXES / VETO), and re-enters on a
veto up to `MAX_ITERS`.

> **No mandatory human gate.** This army produces *deliverables* (it doesn't spend budget or
> launch live), so unlike Solve-Kit there is **no blocking go/no-go**. Instead a light,
> **optional Direction Check** is offered after strategy/positioning (`auto_proceed` by
> default; inject `console_direction_check` to confirm or steer).

## Use it in your agent harness (all optional — pick any)

The `agents/*.md` + `skills/*/SKILL.md` mirror loads into any coding-agent harness — none is
privileged, all are interchangeable. The `marketing` CLI scaffolds the native command pack
(`.marketing/commands/` → 11 slash-commands) for whichever one you use:

```bash
marketing init --agent codex          # or: claude | cursor | copilot | gemini | opencode
marketing check                       # health check (payload + commands + SDK)
```

| Harness | `--agent` | Scaffolds into | Invoke |
|---------|-----------|----------------|--------|
| **Claude** (Claude Code) | `claude` | `.claude/commands` + `.claude/agents` + `.claude/skills` | `/marketing.mission` |
| **Codex** (OpenAI Codex CLI) | `codex` | `.codex/prompts` | `/prompts:marketing-mission` |
| **Cursor** | `cursor` | `.cursor/commands` | `/marketing-mission` |
| **Copilot** | `copilot` | `.github/prompts` | `marketing-mission.prompt.md` |
| **Gemini** | `gemini` | `.gemini/commands/marketing` | `/marketing:mission` |
| **OpenCode** | `opencode` | `.opencode/commands` | `/marketing-mission` |

> "OpenAI" is **not** a harness — the OpenAI-ecosystem target is **codex**. Claude additionally
> receives the full engine mirror (38 agents + 30 skills) so subagents dispatch natively.

In any of them the Commander detects context, selects the minimal MECE set of phases/methods,
delegates to the relevant officer/soldier, and never skips the Inspector.

## Test

```bash
pip install -e ".[dev]"
pytest -q
```

Tests run **offline** (no SDK, no network, no API key): `tests/test_structure.py` audits the
wiring/grade/count invariants by pure file parsing; `tests/test_mission_harness.py` stubs the
SDK and drives the mission control-flow branches (proceed→pass, steer→loop, veto→cap);
`tests/test_cli.py` exercises `marketing init` scaffolding + transcoding for all six harnesses
(including codex).

## Add a soldier (repeatable pattern)

1. `mkdir skills/<method>/` + write `skills/<method>/SKILL.md` (procedure + output format).
2. `agents/soldier-<method>.md` (frontmatter name/description/model/color + role, manual=skill,
   hard rules, output).
3. `marketing_kit/soldiers/soldier_<method>.py` (`Agent` + `WebSearchTool` + `model=ELITE|STANDARD`).
4. Wire it at the officer: import + `.as_tool(...)`.
5. Quality gate: `py_compile` · name==file · skill==dir · grade md↔py · `handoff_description`.

## Layout

```
agents/        agent-harness mirror — commander, 6 officers, 30 soldiers, inspector (*.md)
skills/        one SKILL.md per method (30)
.marketing/    payload — memory/constitution.md (binding cross-phase law) + commands/ (11)
marketing_kit/ reference engine (Agents SDK) — commander.py · inspector.py · mission.py · models.py
               officers/ (6) · soldiers/ (30)
marketing_cli/ the CLI — cli · scaffolder · integrations (6 harness adapters) · runner_bridge
docs/          RESEARCH.md (the research-backed doctrine)
tests/         offline structural + harness + CLI tests
```

## License

MIT.
