"""Shared test setup: stub the openai-agents SDK so the whole suite runs OFFLINE — no SDK, no
network, no API key. pytest imports this before any test module, so the stub is in place when the
package (and its officers/soldiers/web) do `from agents import ...` at import time.

Tests that drive the loop script `Runner.run_sync` by monkeypatching `mission.Runner`.
"""

import sys
import types

_fake = types.ModuleType("agents")


class Agent:
    def __init__(self, *a, **k):
        self.name = k.get("name")
        self.model = k.get("model")
        self.tools = k.get("tools", [])

    def as_tool(self, *a, **k):
        return {"tool_name": k.get("tool_name")}


class WebSearchTool:
    def __init__(self, *a, **k):
        pass


class Runner:
    @staticmethod
    def run_sync(agent, inp):  # replaced per-test via a scripted runner
        raise RuntimeError("Runner.run_sync not scripted")


def function_tool(f=None, **k):
    """@function_tool and @function_tool(...) both return the function unchanged."""
    if f is None:
        return lambda g: g
    return f


_fake.Agent = Agent
_fake.WebSearchTool = WebSearchTool
_fake.Runner = Runner
_fake.function_tool = function_tool
# Force the stub regardless of whether a real `agents` SDK is installed — the suite is offline.
sys.modules["agents"] = _fake
