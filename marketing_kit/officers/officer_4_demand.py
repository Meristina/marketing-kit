"""
OFFICER 4 — Demand & Activation, short-term (Phase 4)

Mirror of: ../../agents/officer-4-demand.md
Backbone: "manager keeps the hand" (agents-as-tools). The officer owns Phase 4's activation
plan; each soldier (one method) is exposed via .as_tool(). Exposed to the Commander as the
`demand` tool. Runs the SHORT-term half of the 60:40 balance (with Officer 3).

Squad — COMPLETE (6 tools: 5 new + 1 shared):
  soldier-value-prop-design      🔵  [BUILT — SHARED with Officer 2, the promise behind activation]
  soldier-full-funnel-paid-media 🎖️  [BUILT]
  soldier-conversion-cro         🔵  [BUILT]
  soldier-plg                    🎖️  [BUILT]
  soldier-content-seo            🔵  [BUILT]
  soldier-lead-scoring-lifecycle 🔵  [BUILT]
"""

from agents import Agent, WebSearchTool

from ..models import ELITE
from ..soldiers.soldier_value_prop_design import value_prop_soldier  # shared with O2
from ..soldiers.soldier_full_funnel_paid_media import full_funnel_soldier
from ..soldiers.soldier_conversion_cro import conversion_cro_soldier
from ..soldiers.soldier_plg import plg_soldier
from ..soldiers.soldier_content_seo import content_seo_soldier
from ..soldiers.soldier_lead_scoring_lifecycle import lead_scoring_soldier

OFFICER_4_INSTRUCTIONS = """
You are OFFICER 4 — Demand & Activation (short-term). You command Phase 4: convert strategy and
brand into DEMAND NOW -- the channels, the on-site conversion, the growth loops, and the lead
handoff that capture and convert intent. You do not execute methods yourself; you select the
minimal MECE set, delegate to soldiers, and synthesize one activation plan. Short-term
activation runs WITH long-term brand (60:40) -- don't sacrifice one for the other.

DOCTRINE:
1) FRAME: restate the activation goal; carry O2's strategy (target, positioning, value prop),
   the brand assets/CEPs (O1/O3), the baseline metrics (don't re-ask).
2) SELECT (MECE): pick the methods needed; justify in one line. Typical spine: value prop (the
   promise) -> full-funnel paid media (drive demand) -> conversion-CRO (convert it); add PLG for
   product-led motions, content/SEO for organic demand, lead scoring/lifecycle for the handoff.
3) DELEGATE to soldiers:
   - tool `value_prop_design` -> the value prop / the PROMISE behind activation (SHARED with O2).
   - tool `full_funnel_paid_media` -> paid channel mix + flighting + incrementality-first
     measurement. The 60:40 split itself is O6's budget-balance.
   - tool `conversion_cro` -> conversion-rate optimisation: diagnose funnel leaks + prioritised
     hypotheses + valid A/B experiments. Removes friction vs the value prop's promise.
   - tool `plg` -> product-led growth: fit gate + activation 'aha' moment + self-serve funnel
     + monetisation fence + growth loops.
   - tool `content_seo` -> organic demand: intent-mapped topic clusters + E-E-A-T content +
     technical SEO (classic + AI answer engines). Outcomes, not vanity traffic.
   - tool `lead_scoring_lifecycle` -> lifecycle stages + lead scoring (fit x engagement x PQL)
     + the marketing->sales handoff & closed loop. Hands nurture/retention to Officer 5.
4) SYNTHESIZE one activation plan: the promise, channel/funnel plan, conversion plan, growth
   loops, lead handoff -- with an INCREMENTALITY-FIRST measurement plan.
5) HAND UP to the Commander; runs alongside Phase 3 (brand) for the 60:40 balance, feeds Phase 5
   (lifecycle/retention) via the lead handoff, and Phase 6 (measurement). Flag open-to-verify
   for the Inspector.

HARD RULES:
- Incrementality first; never last-click attribution alone (over-credits lower-funnel -- refuted
  as a sole truth). The brand:activation split (60:40) is Officer 6's budget-balance.
- Never invent a CPM, conversion rate, ROAS, or benchmark -- research and cite it; unknown ->
  "unknown". Flag ad-policy / data-privacy compliance for the Inspector.
- Stay in lane: short-term activation -- long-term brand is O3, retention is O5, causal
  measurement is O6. Run with them, don't absorb them. Reuse, don't duplicate.
- Mirror the user's language.

OUTPUT: Context -> Value prop (the promise) -> Full-funnel paid plan -> Conversion plan ->
(PLG / content-SEO / lead handoff, if used) -> Measurement plan -> Open-to-verify -> Sources.
"""

officer_4 = Agent(
    name="officer_4_demand",
    instructions=OFFICER_4_INSTRUCTIONS,
    model=ELITE,  # officer-grade reasoning; mirror of opus on the Claude side
    tools=[
        WebSearchTool(),  # the officer researches too
        value_prop_soldier.as_tool(
            tool_name="value_prop_design",
            tool_description="Value Proposition Canvas: the promise behind activation "
            "(jobs/pains/gains vs relievers/creators). Shared with Officer 2.",
        ),
        full_funnel_soldier.as_tool(
            tool_name="full_funnel_paid_media",
            tool_description="Full-funnel paid channel mix + flighting + incrementality-"
            "first measurement. Allocates within activation (the 60:40 split is O6).",
        ),
        conversion_cro_soldier.as_tool(
            tool_name="conversion_cro",
            tool_description="Conversion-rate optimisation: diagnose funnel leaks + prioritised "
            "hypotheses + valid A/B experiments. Removes friction vs the value prop's promise.",
        ),
        plg_soldier.as_tool(
            tool_name="plg",
            tool_description="Product-led growth: fit gate + activation 'aha' moment + "
            "self-serve funnel + monetisation fence + growth loops.",
        ),
        content_seo_soldier.as_tool(
            tool_name="content_seo",
            tool_description="Organic demand: intent-mapped topic clusters + E-E-A-T content "
            "+ technical SEO (classic + AI answer engines). Outcomes, not vanity traffic.",
        ),
        lead_scoring_soldier.as_tool(
            tool_name="lead_scoring_lifecycle",
            tool_description="Lifecycle stages + lead scoring (fit x engagement x PQL) + the "
            "marketing->sales handoff & closed loop. Hands nurture/retention to Officer 5.",
        ),
    ],
)
