"""CLI tests — offline (no SDK, no network). Exercises `marketing init` scaffolding for all six
harnesses (including codex) and the transcoding specifics. The actual `marketing run` engine path
needs the SDK and is covered structurally by test_mission_harness.py."""

import pytest

from marketing_cli import scaffolder, integrations, cli


def test_supported_harnesses_include_codex():
    assert integrations.SUPPORTED == ("claude", "codex", "cursor", "copilot", "gemini", "opencode")
    assert "codex" in integrations.SUPPORTED
    # "openai" is NOT a harness — the OpenAI-ecosystem target is codex.
    assert "openai" not in integrations.SUPPORTED


def test_cli_main_init(tmp_path, capsys):
    """Exercise the full CLI layer (argparse + _cmd_init print path), not just scaffolder."""
    rc = cli.main(["init", str(tmp_path), "--agent", "claude"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "Initialized Marketing-Kit" in out and "payload source" in out
    assert (tmp_path / ".claude" / "commands").is_dir()


def test_cli_main_check(tmp_path):
    assert cli.main(["check", str(tmp_path)]) in (0, 1)  # returns status, shouldn't raise


def test_cli_rejects_openai_as_harness(tmp_path):
    # argparse choices must reject "openai" (it's not a harness)
    with pytest.raises(SystemExit):
        cli.main(["init", str(tmp_path), "--agent", "openai"])


def test_init_claude(tmp_path):
    summary = scaffolder.init(str(tmp_path), agent="claude")
    assert (tmp_path / ".marketing" / "commands").is_dir()
    assert (tmp_path / "missions").is_dir()
    cmds = list((tmp_path / ".claude" / "commands").glob("marketing.*.md"))
    assert len(cmds) == scaffolder.N_COMMANDS, [c.name for c in cmds]
    assert summary["agent"] == "claude"
    # claude also gets the engine mirror: 38 agents (commander + inspector + 6 officers + 30 soldiers), 30 skills
    assert summary["agents"] == 38 and summary["skills"] == 30


def test_init_codex(tmp_path):
    summary = scaffolder.init(str(tmp_path), agent="codex")
    prompts = list((tmp_path / ".codex" / "prompts").glob("marketing-*.md"))
    assert len(prompts) == scaffolder.N_COMMANDS, [p.name for p in prompts]
    # codex is near-passthrough: frontmatter preserved
    sample = (tmp_path / ".codex" / "prompts" / "marketing-strategy.md").read_text()
    assert sample.startswith("---") and "description:" in sample
    assert summary["agent"] == "codex" and "note" in summary


def test_init_all_harnesses(tmp_path):
    expected = {
        "codex":    (".codex/prompts", "marketing-strategy.md", scaffolder.N_COMMANDS),
        "cursor":   (".cursor/commands", "marketing-strategy.md", scaffolder.N_COMMANDS),
        "copilot":  (".github/prompts", "marketing-strategy.prompt.md", scaffolder.N_COMMANDS),
        "gemini":   (".gemini/commands/marketing", "strategy.toml", scaffolder.N_COMMANDS),
        "opencode": (".opencode/commands", "marketing-strategy.md", scaffolder.N_COMMANDS),
    }
    for agent, (subdir, sample, count) in expected.items():
        proj = tmp_path / agent
        s = scaffolder.init(str(proj), agent=agent)
        files = list((proj / subdir).glob("*"))
        assert len(files) == count, (agent, [f.name for f in files])
        assert (proj / subdir / sample).is_file(), (agent, sample)
        assert s["agent"] == agent


def test_transcoding_specifics(tmp_path):
    # cursor: no YAML frontmatter in the body
    scaffolder.init(str(tmp_path / "cur"), agent="cursor")
    cur = (tmp_path / "cur" / ".cursor" / "commands" / "marketing-strategy.md").read_text()
    assert not cur.startswith("---"), "cursor commands must not carry frontmatter"
    # copilot: agent-mode frontmatter
    scaffolder.init(str(tmp_path / "cop"), agent="copilot")
    cop = (tmp_path / "cop" / ".github" / "prompts" / "marketing-strategy.prompt.md").read_text()
    assert cop.startswith("---") and "mode: agent" in cop
    # gemini: TOML with {{args}} (not $ARGUMENTS)
    scaffolder.init(str(tmp_path / "gem"), agent="gemini")
    gem = (tmp_path / "gem" / ".gemini" / "commands" / "marketing" / "mission.toml").read_text()
    assert gem.startswith("description = ") and "prompt = " in gem
    assert "{{args}}" in gem and "$ARGUMENTS" not in gem


def test_init_scaffolds_constitution(tmp_path):
    # the constitution is the binding cross-phase law; init must carry it into the project
    scaffolder.init(str(tmp_path), agent="claude")
    constitution = tmp_path / ".marketing" / "memory" / "constitution.md"
    assert constitution.is_file()
    text = constitution.read_text(encoding="utf-8")
    # Article VIII is the marketing inversion: no mandatory HITL gate — instead the optional,
    # non-blocking Direction Check. Assert the stable structural markers, not the heading wording.
    assert "Article VIII" in text and "Direction Check" in text


def test_every_command_references_the_constitution(tmp_path):
    # each command can be invoked alone, so each must re-anchor the constitution
    scaffolder.init(str(tmp_path), agent="claude")
    cmds = list((tmp_path / ".claude" / "commands").glob("marketing.*.md"))
    assert len(cmds) == scaffolder.N_COMMANDS
    missing = [c.name for c in cmds if "constitution.md" not in c.read_text(encoding="utf-8")]
    assert not missing, f"commands not anchoring the constitution: {missing}"


def test_unsupported_agent_raises(tmp_path):
    with pytest.raises(ValueError):
        scaffolder.init(str(tmp_path), agent="bogus")
