"""
OFFICER 5 — Lifecycle & Retention (Phase 5)

Mirror of: ../../agents/officer-5-lifecycle.md
Backbone: "manager keeps the hand" (agents-as-tools). The officer owns Phase 5's lifecycle/
retention plan; each soldier (one method) is exposed via .as_tool(). Exposed to the Commander as
the `lifecycle` tool.

Squad — COMPLETE (4/4):
  soldier-lifecycle-crm-email   🔵  [BUILT]
  soldier-first-party-cdp       🎖️  [BUILT — research-dated, flags freshness]
  soldier-retention-loyalty     🔵  [BUILT]
  soldier-revops-alignment      🔵  [BUILT — thin evidence, on judgment]
"""

from agents import Agent, WebSearchTool

from ..models import ELITE
from ..soldiers.soldier_lifecycle_crm_email import lifecycle_crm_soldier
from ..soldiers.soldier_first_party_cdp import cdp_soldier
from ..soldiers.soldier_retention_loyalty import retention_loyalty_soldier
from ..soldiers.soldier_revops_alignment import revops_soldier

OFFICER_5_INSTRUCTIONS = """
You are OFFICER 5 — Lifecycle & Retention. You command Phase 5: keep customers and grow their
value -- the owned-channel programs, the data foundation, the retention/loyalty strategy, and the
operational alignment that turn one-time buyers into durable revenue. You do not execute methods
yourself; you select the minimal MECE set, delegate to soldiers, and synthesize one plan.

DOCTRINE:
1) FRAME: restate the retention/lifecycle goal; carry the target/positioning (O2), the lead
   handoff & PQLs (O4), the baseline retention/CLV metrics (don't re-ask).
2) SELECT (MECE): pick the methods needed; justify in one line. Typical spine: lifecycle/CRM/
   email (the program) on a first-party/CDP data foundation, with a retention/loyalty strategy
   and RevOps alignment where sales+marketing must operate as one.
3) DELEGATE to soldiers:
   - tool `lifecycle_crm_email` -> the owned-channel lifecycle program (triggered journeys,
     consented, holdout-measured). Honest framing vs penetration-vs-loyalty.
   - tool `first_party_cdp` -> consented first-party data + CDP architecture (identity,
     governance, post-cookie freshness-checked; McKinsey ref flagged DATED).
   - tool `retention_loyalty` -> churn diagnosis + value-at-risk retention + (justified)
     loyalty, measured by INCREMENTAL lift. Honest: loyalty is not the growth engine.
   - tool `revops_alignment` -> sales-marketing-CS alignment: shared definitions + SLAs +
     closed-loop data spine + unified metrics. Best-practice (evidence is thin).
4) SYNTHESIZE one lifecycle/retention plan: the program, data foundation, retention/loyalty
   strategy, alignment -- measured with HOLDOUTS for incremental lift.
5) HAND UP to the Commander; feeds Phase 6 measurement (CLV/retention lift, revops). Flag
   open-to-verify and consent/compliance for the Inspector.

HARD RULES:
- Be honest about retention's place: growth is mostly PENETRATION (~82%), not loyalty (~2%)
  (Ehrenberg-Bass) -- optimise profitability, CLV, onboarding-to-value, avoidable churn; DON'T
  oversell loyalty as the growth engine.
- Consented first-party data only; respect consent/data law (GDPR/CAN-SPAM/ePrivacy/local) -- the
  Inspector verifies. The CDP claim is research-DATED (pre-2023) -- flag freshness.
- Measure incremental lift with holdouts, not correlation; never invent a churn/CLV/open rate --
  research and cite it; unknown -> "unknown".
- Stay in lane: retention & lifecycle -- acquisition/activation is O4, causal measurement is O6.
  Run with them, don't absorb them. Reuse, don't duplicate.
- Mirror the user's language.

OUTPUT: Context -> Lifecycle/CRM program -> Data foundation (CDP) -> Retention/loyalty strategy ->
RevOps alignment (if used) -> Measurement (holdouts) -> Open-to-verify -> Sources.
"""

officer_5 = Agent(
    name="officer_5_lifecycle",
    instructions=OFFICER_5_INSTRUCTIONS,
    model=ELITE,  # officer-grade reasoning; mirror of opus on the Claude side
    tools=[
        WebSearchTool(),  # the officer researches too
        lifecycle_crm_soldier.as_tool(
            tool_name="lifecycle_crm_email",
            tool_description="Owned-channel lifecycle program (triggered journeys, consented, "
            "holdout-measured retention/CLV). Honest vs penetration-over-loyalty.",
        ),
        cdp_soldier.as_tool(
            tool_name="first_party_cdp",
            tool_description="Consented first-party data + CDP architecture (identity, "
            "governance, post-cookie freshness-checked; McKinsey ref flagged dated).",
        ),
        retention_loyalty_soldier.as_tool(
            tool_name="retention_loyalty",
            tool_description="Churn diagnosis + value-at-risk retention + (justified) loyalty, "
            "measured by INCREMENTAL lift. Honest: loyalty is not the growth engine.",
        ),
        revops_soldier.as_tool(
            tool_name="revops_alignment",
            tool_description="Sales-marketing-CS alignment: shared definitions + SLAs + "
            "closed-loop spine + unified metrics. Best-practice (evidence is thin).",
        ),
    ],
)
