"""Model resolution — grade → model mapping (provider-agnostic, env-configurable).

Defaults keep OpenAI (non-breaking):
  MK_ELITE_MODEL     elite tier  (🎖️)  default: "gpt-5"
  MK_STANDARD_MODEL  standard    (🔵)  default: "gpt-5-mini"

Non-OpenAI providers via the LiteLLM extra (`pip install "openai-agents[litellm]"`):
  export MK_ELITE_MODEL="litellm/anthropic/claude-opus-4-20250514"
  export MK_STANDARD_MODEL="litellm/anthropic/claude-3-5-sonnet-20241022"

The grade of each unit is fixed in its definition; only the concrete model is configurable.
"""

import os

ELITE = os.getenv("MK_ELITE_MODEL", "gpt-5")
STANDARD = os.getenv("MK_STANDARD_MODEL", "gpt-5-mini")
