"""
COMMANDER — Generalist Marketing Army (OpenAI Agents SDK port)

Mirror of: ../agents/commander-marketing.md
Backbone: "manager keeps the hand" (agents-as-tools). The commander owns the final
deliverable; officers are exposed via .as_tool(). The Inspector is a mandatory tool
at the end of every loop.

Entry points (mirroring Solve-Kit):
- mission.py  -> the looped, stateful runner (Mission Dossier + optional Direction Check +
  iteration). NB: no mandatory HITL — this army produces deliverables, it doesn't spend budget.
- this file's __main__ is a single-pass demo only.

Install `openai-agents`; web access via the hosted WebSearchTool so no unit invents facts.
"""

from agents import Agent, Runner, WebSearchTool

from .models import ELITE

# Officers and inspector are imported as they get built (one per turn).
from .officers.officer_1_research import officer_1
from .officers.officer_2_strategy import officer_2
from .officers.officer_3_brand import officer_3
from .officers.officer_4_demand import officer_4
from .officers.officer_5_lifecycle import officer_5
from .officers.officer_6_measure import officer_6
from .inspector import inspector

COMMANDER_INSTRUCTIONS = """
You are the COMMANDER of a generalist marketing army (B2B + B2C, any market). You do
not execute methods yourself. You command.

ALWAYS run this doctrine:
0) FRAME: restate the marketing goal in one line; name product/audience/market/
   B2B-B2C/stage + the business objective; ask 2-3 questions that change the plan,
   each with a recommended default; then WAIT (unless told "go").
1) INSIGHT & RESEARCH         -> tool `research`   (Officer 1)
2) STRATEGY & POSITIONING      -> tool `strategy`   (Officer 2)
   --- optional DIRECTION CHECK: present positioning+strategy, offer to confirm/steer
       before heavy build (no mandatory go/no-go; recommended if high-stakes) ---
3) BRAND-BUILDING (long)       -> tool `brand`      (Officer 3)
4) DEMAND & ACTIVATION (short) -> tool `demand`     (Officer 4)
5) LIFECYCLE & RETENTION       -> tool `lifecycle`  (Officer 5)
6) MEASUREMENT & EFFECTIVENESS -> tool `measure`    (Officer 6)

Pick the MINIMAL set of phases/methods the brief needs (MECE). Justify in one line.
Strategy & positioning before brand & demand; run brand-building (long) AND activation
(short) together (the 60:40 balance) — and surface the Binet&Field ↔ Sharp tension, don't
hide it. For measurement, TRIANGULATE (incrementality + MMM + attribution), never one alone.

END OF EVERY LOOP: call tool `inspect` (the Inspector). It verifies (a) sources — every
metric/market-size/benchmark cites a real internet source, nothing invented; (b)
compliance — data & advertising law for the detected market; (c) quality via a
devil's-advocate pass, then converges. Veto power: fix and re-inspect on material issues.

Deliver ONE coherent result, MIRROR THE USER'S LANGUAGE, cite sources, and state what
was verified / changed after critique / still risky. Never invent a number.
"""

commander = Agent(
    name="commander_marketing",
    instructions=COMMANDER_INSTRUCTIONS,
    model=ELITE,  # elite tier — mirror of opus on the Claude side
    tools=[
        WebSearchTool(),  # every unit can research; the commander too
        officer_1.as_tool(tool_name="research",  tool_description="Phase 1: insight & research (JTBD, CEPs, sizing)."),
        officer_2.as_tool(tool_name="strategy",  tool_description="Phase 2: strategy & positioning (STP, brand equity)."),
        officer_3.as_tool(tool_name="brand",     tool_description="Phase 3: brand-building (mental availability, ESOV)."),
        officer_4.as_tool(tool_name="demand",    tool_description="Phase 4: demand & activation (paid, CRO, PLG, SEO)."),
        officer_5.as_tool(tool_name="lifecycle", tool_description="Phase 5: lifecycle & retention (CRM, CDP, RevOps)."),
        officer_6.as_tool(tool_name="measure",   tool_description="Phase 6: measurement (incrementality, MMM, 60:40)."),
        inspector.as_tool(tool_name="inspect",   tool_description="Sources+compliance+quality gate (veto)."),
    ],
)

if __name__ == "__main__":
    result = Runner.run_sync(commander, "We have a marketing goal: ... (describe it)")
    print(result.final_output)
