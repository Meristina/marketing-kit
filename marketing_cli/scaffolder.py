"""scaffolder — `marketing init`: copy the command pack into a target project and write the
chosen harness's command files (via integrations).

Resolves the payload from the **repo root** when running from a source checkout (dev). A bundled
mode (shipping the pack inside the wheel) is the optional next step; for now `marketing init`
requires a source checkout / editable install.
"""

import shutil
from pathlib import Path

from . import integrations

N_COMMANDS = 11  # .marketing/commands/*.md


def sources() -> dict:
    """Locate the payload source. Keys: marketing, commands, agents, skills, mode."""
    here = Path(__file__).resolve()
    root = here.parents[1]
    if (root / ".marketing").is_dir() and (root / "agents").is_dir():
        return {"marketing": root / ".marketing", "commands": root / ".marketing" / "commands",
                "agents": root / "agents", "skills": root / "skills", "mode": "source"}
    p = here.parent / "payload"
    if (p / "marketing").is_dir():
        return {"marketing": p / "marketing", "commands": p / "marketing" / "commands",
                "agents": p / "agents", "skills": p / "skills", "mode": "bundled"}
    raise RuntimeError("Marketing-Kit payload not found — run from a source checkout / editable install.")


def init(target: str, agent: str = "claude") -> dict:
    """Scaffold .marketing/ + missions/ into `target` and install the harness command pack."""
    src = sources()
    target = Path(target).resolve()
    target.mkdir(parents=True, exist_ok=True)

    # 1) the .marketing/ payload (the command pack)
    shutil.copytree(src["marketing"], target / ".marketing", dirs_exist_ok=True)

    # 2) missions/ output dir
    (target / "missions").mkdir(exist_ok=True)

    # 3) harness integration (commands + engine for claude)
    summary = integrations.install(agent, src, target)
    summary["target"] = str(target)
    summary["payload_mode"] = src["mode"]
    return summary


def check(target: str = ".") -> list:
    """Lightweight prerequisite/health check. Returns (label, ok, detail) tuples."""
    checks = []
    try:
        src = sources()
        checks.append((f"payload found ({src['mode']})", True, str(src["marketing"].parent)))
        checks.append(("constitution present", (src["marketing"] / "memory" / "constitution.md").is_file(), ""))
        n = len(list(src["commands"].glob("*.md")))
        checks.append((f"{N_COMMANDS} commands present", n == N_COMMANDS, f"found {n}"))
        n_agents = len(list(src["agents"].glob("*.md")))
        checks.append(("agents mirror present (38)", n_agents == 38, f"found {n_agents}"))
    except RuntimeError as e:
        checks.append(("payload found", False, str(e)))
    try:
        import agents  # noqa: F401  (the Agents SDK)
        sdk = True
    except ImportError:
        sdk = False
    checks.append(("Agents SDK installed (needed for `marketing run`)", sdk, "pip install openai-agents"))
    return checks
