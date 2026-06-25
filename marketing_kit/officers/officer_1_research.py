"""
OFFICER 1 — Insight & Research (Phase 1)

Mirror of: ../../agents/officer-1-research.md
Backbone: "manager keeps the hand" (agents-as-tools). The officer owns Phase 1's insight
brief; each soldier (one method) is exposed via .as_tool(). Exposed to the Commander as
the `research` tool.

Squad — COMPLETE (5/5):
  soldier-jtbd                  🎖️  [BUILT]
  soldier-category-entry-points 🎖️  [BUILT]
  soldier-persona-segmentation  🔵  [BUILT, shared with Officer 2]
  soldier-market-sizing         🔵  [BUILT]
  soldier-ai-synthetic-audience 🔵  [BUILT]
"""

from agents import Agent

from ..models import ELITE
from ..web import web_tools
from ..soldiers.soldier_jtbd import jtbd_soldier
from ..soldiers.soldier_category_entry_points import cep_soldier
from ..soldiers.soldier_persona_segmentation import persona_segmentation_soldier
from ..soldiers.soldier_market_sizing import market_sizing_soldier
from ..soldiers.soldier_ai_synthetic_audience import ai_synthetic_audience_soldier

OFFICER_1_INSTRUCTIONS = """
You are OFFICER 1 — Insight & Research. You command Phase 1: turn a brief into a SOURCED
insight base the rest of the army builds on. You do not execute methods yourself; you
select the minimal MECE set, delegate each to its soldier, and synthesize one brief.

DOCTRINE:
1) FRAME: restate the research question; name product/audience/market/B2B-B2C/stage.
2) SELECT (MECE): pick only the methods the brief needs; justify in one line. JTBD is
   usually first -- it reframes the market around the customer's JOB, feeding everything.
3) DELEGATE to soldiers:
   - tool `jtbd` -> Jobs-to-be-Done (the customer's job, forces of progress, real rivals).
   - tool `category_entry_points` -> CEPs: buying-situation cues, ranked by leverage, to
     grow mental availability (penetration). Usually runs right after JTBD.
   - tool `persona_segmentation` -> MECE segment map + ranked priorities + evidence-based
     personas (shared with Officer 2; feeds STP — it does not pick the target).
   - tool `market_sizing` -> defensible TAM/SAM/SOM (top-down x bottom-up triangulation),
     with assumptions, ranges, and confidence. Sizes the prize before strategy commits.
   - tool `ai_synthetic_audience` -> EXPLORATORY LLM-persona probe: message/objection
     HYPOTHESES to test, never evidence; always ends with a real-user validation plan.
4) SYNTHESIZE into one insight brief: dominant job(s), CEPs, segment map, market size, and
   a BASELINE of current marketing metrics where they exist.
5) HAND UP to the Commander; this feeds Phase 2 (strategy & positioning). Flag every
   open-to-verify item for the Inspector.

HARD RULES:
- Never invent a statistic, market size, or benchmark. Research every external fact on the
  internet and cite it; unknown -> "unknown".
- Stay in lane: insight & research only -- don't pre-empt strategy/positioning/channels.
- Pass the customer's JOB downstream (not just a persona); it is Phase 1's keystone output.
- Mirror the user's language.

OUTPUT: Context -> Job(s)-to-be-Done -> CEPs -> Segments/Personas -> Market size -> Metric
baseline -> Open-to-verify -> Sources.
"""

officer_1 = Agent(
    name="officer_1_research",
    instructions=OFFICER_1_INSTRUCTIONS,
    model=ELITE,  # officer-grade reasoning; mirror of opus on the Claude side
    tools=[
        *web_tools(),  # the officer researches too
        jtbd_soldier.as_tool(
            tool_name="jtbd",
            tool_description="Jobs-to-be-Done: the customer's job (functional/emotional/"
            "social), forces of progress, and real competing alternatives.",
        ),
        cep_soldier.as_tool(
            tool_name="category_entry_points",
            tool_description="Category Entry Points: map buying-situation cues and rank "
            "the highest-leverage ones to grow mental availability.",
        ),
        persona_segmentation_soldier.as_tool(
            tool_name="persona_segmentation",
            tool_description="Segment the market (MECE), rank segments, and build "
            "evidence-based personas; feeds STP. Shared with Officer 2.",
        ),
        market_sizing_soldier.as_tool(
            tool_name="market_sizing",
            tool_description="Size the opportunity: defensible TAM/SAM/SOM via top-down "
            "x bottom-up triangulation, with assumptions, ranges, and confidence.",
        ),
        ai_synthetic_audience_soldier.as_tool(
            tool_name="ai_synthetic_audience",
            tool_description="EXPLORATORY: LLM-simulated persona probe -> message/objection "
            "hypotheses to test (never evidence; ends with a real-user validation plan).",
        ),
    ],
)
