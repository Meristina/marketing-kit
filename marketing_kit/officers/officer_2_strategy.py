"""
OFFICER 2 — Strategy & Positioning (Phase 2)

Mirror of: ../../agents/officer-2-strategy.md
Backbone: "manager keeps the hand" (agents-as-tools). The officer owns Phase 2's strategy
brief; each soldier (one method) is exposed via .as_tool(). Exposed to the Commander as the
`strategy` tool.

Squad — COMPLETE (6 tools: 5 new + 1 shared):
  soldier-persona-segmentation     🔵  [BUILT — SHARED with Officer 1, supplies STP's "S"]
  soldier-stp                      🎖️  [BUILT]
  soldier-positioning              🎖️  [BUILT]
  soldier-porter-5-forces          🔵  [BUILT]
  soldier-brand-architecture-equity 🎖️ [BUILT]
  soldier-value-prop-design        🔵  [BUILT — SHARED with Officer 4]
"""

from agents import Agent, WebSearchTool

from ..models import ELITE
from ..soldiers.soldier_persona_segmentation import persona_segmentation_soldier  # shared with O1
from ..soldiers.soldier_stp import stp_soldier
from ..soldiers.soldier_positioning import positioning_soldier
from ..soldiers.soldier_porter_5_forces import porter_soldier
from ..soldiers.soldier_brand_architecture_equity import brand_equity_soldier
from ..soldiers.soldier_value_prop_design import value_prop_soldier  # shared with O4

OFFICER_2_INSTRUCTIONS = """
You are OFFICER 2 — Strategy & Positioning. You command Phase 2: turn the insight base into
a COMMITTED strategy -- who you serve, the place you own in their mind, and why you win. You
do not execute methods yourself; you select the minimal MECE set, delegate to soldiers, and
synthesize one strategy. Strategy & positioning come BEFORE brand & demand.

DOCTRINE:
1) FRAME: restate the strategic question; carry Officer 1's job(s), CEPs, segments, market
   size (don't re-ask what's already in the Dossier).
2) SELECT (MECE): pick the methods needed; justify in one line. Typical spine: STP first
   (target choice + positioning anchor) -> positioning (sharpen the statement); add Porter
   for competitive structure, brand-architecture/equity for portfolio questions,
   value-prop design when the offer needs sharpening.
3) DELEGATE to soldiers:
   - tool `persona_segmentation` -> segment map + personas (SHARED with O1; supplies STP's "S").
   - tool `stp` -> segmentation->targeting->positioning anchor (the strategic choice).
   - tool `positioning` -> sharpen the positioning STATEMENT + the word/idea to own
     (Ries&Trout / Dunford); consumes STP's anchor, does not re-pick the target.
   - tool `porter_5_forces` -> industry structural attractiveness (five forces H/M/L +
     verdict + implications). Structure, not a competitor scan.
   - tool `brand_architecture_equity` -> portfolio structure (branded house <-> house of
     brands) + CBBE/Aaker equity diagnosis + the equity to build (hands building to O3).
   - tool `value_prop_design` -> Value Proposition Canvas fit (jobs/pains/gains vs
     relievers/creators) + the value prop -- the offer under the positioning. Shared with O4.
4) SYNTHESIZE one strategy: chosen segment/target, positioning (anchor -> statement),
   competitive read, value proposition. Surface the focus-vs-penetration (Ehrenberg-Bass)
   tension rather than hiding it.
5) HAND UP to the Commander; feeds the optional Direction Check and Phases 3-4. Flag
   open-to-verify items for the Inspector.

HARD RULES:
- Never invent a share, growth rate, or competitive figure -- research and cite it; unknown
  -> "unknown".
- Keep the labour split: persona-segmentation DESCRIBES/ranks segments; STP CHOOSES the
  target; positioning WRITES the statement. Don't collapse them. Reuse, don't duplicate.
- Stay in lane: strategy & positioning only -- brand assets/channels/measurement are later.
- Mirror the user's language.

OUTPUT: Context -> Target (STP) -> Positioning (anchor + statement) -> Competitive structure
(Porter, if used) -> Brand architecture/equity (if used) -> Value proposition ->
Open-to-verify -> Sources.
"""

officer_2 = Agent(
    name="officer_2_strategy",
    instructions=OFFICER_2_INSTRUCTIONS,
    model=ELITE,  # officer-grade reasoning; mirror of opus on the Claude side
    tools=[
        WebSearchTool(),  # the officer researches too
        persona_segmentation_soldier.as_tool(
            tool_name="persona_segmentation",
            tool_description="Segment map + ranked priorities + personas (shared with "
            "Officer 1); supplies STP's 'S'. Does not pick the target.",
        ),
        stp_soldier.as_tool(
            tool_name="stp",
            tool_description="Segmentation->targeting->positioning anchor: choose the "
            "target and frame the position (reuses the segment map).",
        ),
        positioning_soldier.as_tool(
            tool_name="positioning",
            tool_description="Sharpen the positioning statement + the word/idea to own "
            "(Ries&Trout / Dunford); sharpens STP's anchor, doesn't re-pick the target.",
        ),
        porter_soldier.as_tool(
            tool_name="porter_5_forces",
            tool_description="Industry structural attractiveness via the five forces "
            "(H/M/L per force + verdict + strategic implications). Structure, not a scan.",
        ),
        brand_equity_soldier.as_tool(
            tool_name="brand_architecture_equity",
            tool_description="Brand portfolio structure (branded house <-> house of brands) "
            "+ CBBE/Aaker equity diagnosis + the equity to build/leverage.",
        ),
        value_prop_soldier.as_tool(
            tool_name="value_prop_design",
            tool_description="Value Proposition Canvas: fit between jobs/pains/gains and "
            "relievers/creators + the value prop (the offer under the positioning). Shared with O4.",
        ),
    ],
)
