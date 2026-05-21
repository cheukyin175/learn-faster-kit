"""Tests for resume command construction in learn_faster.cli.launcher."""

from __future__ import annotations

import pytest

from learn_faster.cli.agents import get_agent_profile
from learn_faster.cli.launcher import (
    ResumeTarget,
    build_resume_command,
)


CLAUDE = get_agent_profile("claude-code")
CODEX = get_agent_profile("codex")
PROMPT = "FASTER coaching system prompt"


@pytest.mark.parametrize(
    "target, expected_tail",
    [
        (ResumeTarget(mode="last"), ["--continue"]),
        (ResumeTarget(mode="id", session_id="abc-123"), ["--resume", "abc-123"]),
        (ResumeTarget(mode="pick"), ["--resume"]),
        (ResumeTarget(mode="last", fork=True), ["--continue", "--fork-session"]),
        (
            ResumeTarget(mode="id", session_id="abc-123", fork=True),
            ["--resume", "abc-123", "--fork-session"],
        ),
        (ResumeTarget(mode="pick", fork=True), ["--resume", "--fork-session"]),
    ],
)
def test_claude_resume_command_shape(target: ResumeTarget, expected_tail: list[str]) -> None:
    cmd = build_resume_command(CLAUDE, PROMPT, target)
    assert cmd[:3] == ["claude", "--system-prompt", PROMPT]
    assert cmd[3:] == expected_tail


def test_claude_resume_never_includes_review() -> None:
    for target in [
        ResumeTarget(mode="last"),
        ResumeTarget(mode="id", session_id="x"),
        ResumeTarget(mode="pick"),
        ResumeTarget(mode="last", fork=True),
    ]:
        cmd = build_resume_command(CLAUDE, PROMPT, target)
        assert "/review" not in cmd


@pytest.mark.parametrize(
    "target, expected",
    [
        (ResumeTarget(mode="last"), ["codex", "resume", "--last"]),
        (ResumeTarget(mode="id", session_id="abc-123"), ["codex", "resume", "abc-123"]),
        (ResumeTarget(mode="pick"), ["codex", "resume"]),
        (ResumeTarget(mode="last", fork=True), ["codex", "fork", "--last"]),
        (
            ResumeTarget(mode="id", session_id="abc-123", fork=True),
            ["codex", "fork", "abc-123"],
        ),
        (ResumeTarget(mode="pick", fork=True), ["codex", "fork"]),
    ],
)
def test_codex_resume_command_shape(target: ResumeTarget, expected: list[str]) -> None:
    cmd = build_resume_command(CODEX, PROMPT, target)
    assert cmd == expected


def test_codex_resume_does_not_inject_prompt() -> None:
    for target in [
        ResumeTarget(mode="last"),
        ResumeTarget(mode="id", session_id="x"),
        ResumeTarget(mode="pick"),
        ResumeTarget(mode="last", fork=True),
    ]:
        cmd = build_resume_command(CODEX, PROMPT, target)
        assert PROMPT not in cmd
        assert "--system-prompt" not in cmd
