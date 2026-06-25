"""Web-search capability — provider-agnostic, powered by Gemini's Google-Search grounding.

The army's "no invented facts" doctrine (Constitution Art. I) needs LIVE web access. OpenAI's
hosted `WebSearchTool` only works when the brain runs on OpenAI's own platform — it breaks on
Gemini / Anthropic / OpenRouter. This module is the single source of truth for the web capability
every unit receives, selected by environment:

  MK_WEBSEARCH=0                          -> []                  (no web search; units say "unknown")
  GEMINI_API_KEY / GOOGLE_API_KEY set    -> [gemini_web_search] (works with ANY brain model)
  else                                   -> [WebSearchTool()]   (OpenAI hosted; OpenAI brain only)

So one Google AI Studio (Gemini) key gives every soldier real web search regardless of which model
(OpenAI, Anthropic, OpenRouter, or Gemini itself) is doing the reasoning. The grade/brain model is
chosen separately in models.py (ELITE / STANDARD).
"""

import os

from agents import WebSearchTool, function_tool


def _gemini_key():
    return os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")


def _websearch_disabled() -> bool:
    return os.getenv("MK_WEBSEARCH", "1").strip().lower() in ("0", "false", "no", "off")


@function_tool
def gemini_web_search(query: str) -> str:
    """Search the live web (Google Search, via Gemini grounding) and return a concise, SOURCED
    answer. Use for any real fact — market sizes, benchmarks, dates, competitor claims. Returns the
    grounded answer followed by source URLs; if nothing is found or the tool is unavailable, say so
    so the caller can mark the fact 'unknown' (never invent it)."""
    try:
        from google import genai
        from google.genai import types
    except ImportError:
        return ('web_search unavailable: install the Gemini extra '
                '(pip install "marketing-kit[gemini]") or set MK_WEBSEARCH=0.')
    key = _gemini_key()
    if not key:
        return "web_search unavailable: set GEMINI_API_KEY (Google AI Studio) or MK_WEBSEARCH=0."
    model = os.getenv("MK_SEARCH_MODEL", "gemini-2.5-flash")
    try:
        client = genai.Client(api_key=key)
        resp = client.models.generate_content(
            model=model,
            contents=query,
            config=types.GenerateContentConfig(
                tools=[types.Tool(google_search=types.GoogleSearch())]
            ),
        )
        answer = (getattr(resp, "text", None) or "").strip()
        sources = []
        for cand in (getattr(resp, "candidates", None) or []):
            gm = getattr(cand, "grounding_metadata", None)
            for chunk in (getattr(gm, "grounding_chunks", None) or []):
                web = getattr(chunk, "web", None)
                uri = getattr(web, "uri", None) if web else None
                if uri:
                    title = getattr(web, "title", "") or uri
                    line = f"- {title}: {uri}"
                    if line not in sources:
                        sources.append(line)
        if sources:
            answer += "\n\nSources:\n" + "\n".join(sources)
        return answer or "No grounded result found."
    except Exception as e:  # network / quota / model errors -> caller marks 'unknown'
        return f"web_search error: {type(e).__name__}: {str(e)[:200]}"


def web_tools() -> list:
    """The web-search capability every unit receives, selected by env. Single source of truth.

    - MK_WEBSEARCH=0           -> no web search
    - GEMINI_API_KEY present   -> Gemini Google-Search grounding (any brain model)
    - otherwise                -> OpenAI hosted WebSearchTool (OpenAI brain only)
    """
    if _websearch_disabled():
        return []
    if _gemini_key():
        return [gemini_web_search]
    return [WebSearchTool()]
