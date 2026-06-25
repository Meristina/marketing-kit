"""Web-search selector tests — offline (no SDK, no network).

web_tools() is the single source of truth for the web capability every unit receives. The `agents`
SDK is stubbed in tests/conftest.py. These tests assert WHICH backend is selected by env — they
never execute a backend (no network). The "unavailable" tests check the graceful no-key path, which
returns before any API call.
"""

from marketing_kit import web  # the `agents` SDK is stubbed in tests/conftest.py

_ENV = ("MK_WEBSEARCH", "MK_SEARCH", "GEMINI_API_KEY", "GOOGLE_API_KEY", "TAVILY_API_KEY",
        "OPENAI_BASE_URL")


def _clear(monkeypatch):
    for v in _ENV:
        monkeypatch.delenv(v, raising=False)


# ---- disable ----------------------------------------------------------------

def test_disabled_returns_no_tools(monkeypatch):
    _clear(monkeypatch)
    monkeypatch.setenv("MK_WEBSEARCH", "0")
    assert web.web_tools() == []


# ---- explicit MK_SEARCH backend selection -----------------------------------

def test_mk_search_ddg(monkeypatch):
    _clear(monkeypatch)
    monkeypatch.setenv("MK_SEARCH", "ddg")
    assert web.web_tools() == [web.duckduckgo_web_search]


def test_mk_search_tavily(monkeypatch):
    _clear(monkeypatch)
    monkeypatch.setenv("MK_SEARCH", "tavily")
    assert web.web_tools() == [web.tavily_web_search]


def test_mk_search_gemini(monkeypatch):
    _clear(monkeypatch)
    monkeypatch.setenv("MK_SEARCH", "gemini")
    assert web.web_tools() == [web.gemini_web_search]


def test_mk_search_openai(monkeypatch):
    _clear(monkeypatch)
    monkeypatch.setenv("MK_SEARCH", "openai")
    tools = web.web_tools()
    assert len(tools) == 1 and type(tools[0]).__name__ == "WebSearchTool"


# ---- auto-detection (no MK_SEARCH) ------------------------------------------

def test_auto_prefers_tavily_key(monkeypatch):
    _clear(monkeypatch)
    monkeypatch.setenv("TAVILY_API_KEY", "x")
    monkeypatch.setenv("GEMINI_API_KEY", "y")  # tavily wins the auto order
    assert web.web_tools() == [web.tavily_web_search]


def test_auto_gemini_key(monkeypatch):
    _clear(monkeypatch)
    monkeypatch.setenv("GEMINI_API_KEY", "y")
    assert web.web_tools() == [web.gemini_web_search]


def test_auto_default_openai_hosted(monkeypatch):
    _clear(monkeypatch)
    tools = web.web_tools()
    assert len(tools) == 1 and type(tools[0]).__name__ == "WebSearchTool"


def test_ddg_not_auto_on_openai(monkeypatch):
    # on OpenAI (no custom base URL), DDG is never auto-selected -> hosted WebSearchTool
    _clear(monkeypatch)
    assert web.web_tools() != [web.duckduckgo_web_search]


def test_custom_base_url_auto_falls_back_to_ddg(monkeypatch):
    # OpenAI's hosted search can't run on a compat endpoint -> auto uses DDG instead
    _clear(monkeypatch)
    monkeypatch.setenv("OPENAI_BASE_URL", "https://generativelanguage.googleapis.com/v1beta/openai/")
    assert web.web_tools() == [web.duckduckgo_web_search]


# ---- graceful no-key path (no network: returns before any API call) ---------

def test_gemini_search_unavailable_without_key(monkeypatch):
    _clear(monkeypatch)
    out = web.gemini_web_search("what is the TAM of X")
    assert isinstance(out, str) and "unavailable" in out.lower()


def test_tavily_search_unavailable_without_key(monkeypatch):
    _clear(monkeypatch)
    out = web.tavily_web_search("what is the TAM of X")
    assert isinstance(out, str) and "unavailable" in out.lower()
