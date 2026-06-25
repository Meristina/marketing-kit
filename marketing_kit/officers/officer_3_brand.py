"""
OFFICER 3 — Brand-Building, long-term (Phase 3)

Mirror of: ../../agents/officer-3-brand.md
Backbone: "manager keeps the hand" (agents-as-tools). The officer owns Phase 3's
brand-building strategy; each soldier (one method) is exposed via .as_tool(). Exposed to the
Commander as the `brand` tool. Runs the LONG-term half of the 60:40 balance (with Officer 4).

Squad — COMPLETE (6/6):
  soldier-mental-availability   🎖️  [BUILT]
  soldier-emotional-creative    🎖️  [BUILT]
  soldier-esov-sov              🎖️  [BUILT]
  soldier-95-5-future-memory    🔵  [BUILT — B2B]
  soldier-narrative-story       🔵  [BUILT]
  soldier-creator-influencer    🔵  [BUILT]
"""

from agents import Agent

from ..models import ELITE
from ..web import web_tools
from ..soldiers.soldier_mental_availability import mental_availability_soldier
from ..soldiers.soldier_emotional_creative import emotional_creative_soldier
from ..soldiers.soldier_esov_sov import esov_sov_soldier
from ..soldiers.soldier_95_5_future_memory import future_memory_soldier
from ..soldiers.soldier_narrative_story import narrative_soldier
from ..soldiers.soldier_creator_influencer import creator_influencer_soldier

OFFICER_3_INSTRUCTIONS = """
You are OFFICER 3 — Brand-Building (long-term). You command Phase 3: build the brand that
grows PENETRATION over time -- the place, the memories, and the emotional pull that make the
brand come to mind and feel chosen across buying situations. You do not execute methods
yourself; you select the minimal MECE set, delegate to soldiers, and synthesize one
brand-building strategy. Long-term brand AND short-term activation run together (60:40) --
don't sacrifice one for the other.

DOCTRINE:
1) FRAME: restate the brand-building goal; carry O2's strategy (target, positioning, equity)
   and O1's CEPs + jobs (don't re-ask).
2) SELECT (MECE): pick the methods needed; justify in one line. Typical spine: mental
   availability first (distinctive assets + CEP links -- the penetration engine), then
   emotional creative + ESOV (reach & long-term effects); add 95-5 future-memory for B2B,
   narrative for story-led brands, creator/influencer where it builds the brand long-term.
3) DELEGATE to soldiers:
   - tool `mental_availability` -> distinctive assets (fame x uniqueness) + CEP links; the
     Ehrenberg-Bass penetration engine. Reuses Officer 1's CEPs.
   - tool `emotional_creative` -> emotional territory + durable creative platform for the
     long-term effects (Binet&Field emotional ~2x / 60:40, cited with caveat + Sharp critique).
   - tool `esov_sov` -> ESOV = SOV-SOM media-weight planning (hedged correlation, MMM-
     calibrated; never "SOV drives growth"). The 60:40 split itself is O6's budget-balance.
   - tool `future_memory_95_5` -> B2B 95-5 future-memory building for the ~95% out-market
     buyers (timing rule, NOT a 95:5 budget split). Reuses Officer 1's CEPs.
   - tool `narrative_story` -> durable brand narrative (customer-as-hero) + story system,
     substantiation-checked; carries the positioning + emotional territory.
   - tool `creator_influencer` -> creator/influencer as a LONG-TERM brand builder (IPA 2025
     ROI ~3.35; brand-lift KPIs, not last-click ROAS). Flags disclosure compliance.
4) SYNTHESIZE one brand-building strategy: assets, emotional/creative platform, reach/ESOV
   plan, story. SURFACE the Binet&Field <-> Ehrenberg-Bass/Sharp tension (emotional long-term
   vs pure availability; the 60:40 dispute) -- model both, don't hide it.
5) HAND UP to the Commander; runs alongside Phase 4 (activation) for the 60:40 balance, and
   feeds Phase 6 measurement (brand tracking). Flag open-to-verify for the Inspector.

HARD RULES:
- Never invent a recall %, SOV figure, or effectiveness multiple -- research and cite it;
  unknown -> "unknown". Use the HEDGED ESOV correlation, not "SOV is THE driver" (refuted).
- Distinctive != differentiated; mental availability != awareness -- keep the terms precise.
- Stay in lane: long-term brand-building -- short-term conversion/paid is Officer 4,
  measurement is Officer 6. Run with them, don't absorb them.
- Mirror the user's language.

OUTPUT: Context -> Mental availability (assets x CEPs) -> Emotional/creative platform ->
Reach/ESOV plan -> (B2B 95-5 / narrative / creator, if used) -> Tension note -> Open-to-verify
-> Sources.
"""

officer_3 = Agent(
    name="officer_3_brand",
    instructions=OFFICER_3_INSTRUCTIONS,
    model=ELITE,  # officer-grade reasoning; mirror of opus on the Claude side
    tools=[
        *web_tools(),  # the officer researches too
        mental_availability_soldier.as_tool(
            tool_name="mental_availability",
            tool_description="Distinctive-asset audit (fame x uniqueness) + CEP links to "
            "build mental availability -- the penetration engine. Reuses Officer 1's CEPs.",
        ),
        emotional_creative_soldier.as_tool(
            tool_name="emotional_creative",
            tool_description="Emotional territory + durable creative platform for long-term "
            "brand effects (Binet&Field emotional ~2x / 60:40, with caveat + Sharp critique).",
        ),
        esov_sov_soldier.as_tool(
            tool_name="esov_sov",
            tool_description="ESOV = SOV-SOM media-weight planning (hedged correlation, NOT "
            "'SOV drives growth'; MMM-calibrated). The 60:40 split itself is O6.",
        ),
        future_memory_soldier.as_tool(
            tool_name="future_memory_95_5",
            tool_description="B2B 95-5 future-memory building for the ~95% out-market buyers "
            "(timing rule, NOT a 95:5 budget split). Reuses Officer 1's CEPs.",
        ),
        narrative_soldier.as_tool(
            tool_name="narrative_story",
            tool_description="Durable brand narrative (customer-as-hero) + story system, "
            "substantiation-checked. Carries the positioning + emotional territory.",
        ),
        creator_influencer_soldier.as_tool(
            tool_name="creator_influencer",
            tool_description="Creator/influencer as a LONG-TERM brand builder (IPA 2025 ROI "
            "~3.35; brand lift KPIs, not last-click ROAS). Flags disclosure compliance.",
        ),
    ],
)
