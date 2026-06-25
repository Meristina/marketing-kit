"""Web-search selector tests — offline (no SDK, no network).

web_tools() is the single source of truth for the web capability every unit receives. We stub the
`agents` SDK (web.py imports WebSearchTool + function_tool from it) and assert the selection by env:
- MK_WEBSEARCH=0           -> no web search
- GEMINI_API_KEY present   -> Gemini Google-Search grounding (works with any brain model)
- otherwise                -> OpenAI hosted WebSearchTool (OpenAI brain only)
"""

from marketing_kit import web  # the `agents` SDK is stubbed in tests/conftest.py


def _clear(monkeypatch):
    for v in ("MK_WEBSEARCH", "GEMINI_API_KEY", "GOOGLE_API_KEY"):
        monkeypatch.delenv(v, raising=False)


def test_disabled_returns_no_tools(monkeypatch):
    _clear(monkeypatch)
    monkeypatch.setenv("MK_WEBSEARCH", "0")
    assert web.web_tools() == []


def test_gemini_key_selects_grounded_search(monkeypatch):
    # a Gemini key -> the provider-agnostic grounded search tool (works with ANY brain)
    _clear(monkeypatch)
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    tools = web.web_tools()
    assert tools == [web.gemini_web_search]


def test_google_api_key_also_selects_grounded_search(monkeypatch):
    _clear(monkeypatch)
    monkeypatch.setenv("GOOGLE_API_KEY", "test-key")
    assert web.web_tools() == [web.gemini_web_search]


def test_default_falls_back_to_openai_hosted(monkeypatch):
    # no Gemini key, not disabled -> the OpenAI hosted WebSearchTool
    _clear(monkeypatch)
    tools = web.web_tools()
    assert len(tools) == 1 and type(tools[0]).__name__ == "WebSearchTool"


def test_gemini_search_unavailable_without_genai(monkeypatch):
    # the function returns a graceful "unavailable" string (never raises) when the SDK/key is absent
    _clear(monkeypatch)
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    out = web.gemini_web_search("what is the TAM of X")
    assert isinstance(out, str) and "unavailable" in out.lower()
