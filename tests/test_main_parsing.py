"""Tests for resume argument parsing in learn_faster.cli.main."""

from __future__ import annotations

import pytest

from learn_faster.cli.launcher import ResumeTarget
from learn_faster.cli.main import parse_resume_args


def test_parse_resume_no_args_means_last() -> None:
    assert parse_resume_args([]) == ResumeTarget(mode="last")


def test_parse_resume_with_id() -> None:
    assert parse_resume_args(["abc-123"]) == ResumeTarget(mode="id", session_id="abc-123")


def test_parse_resume_pick() -> None:
    assert parse_resume_args(["--pick"]) == ResumeTarget(mode="pick")


def test_parse_resume_fork_alone() -> None:
    assert parse_resume_args(["--fork"]) == ResumeTarget(mode="last", fork=True)


def test_parse_resume_id_with_fork() -> None:
    assert parse_resume_args(["abc-123", "--fork"]) == ResumeTarget(
        mode="id", session_id="abc-123", fork=True
    )


def test_parse_resume_pick_with_fork() -> None:
    assert parse_resume_args(["--pick", "--fork"]) == ResumeTarget(mode="pick", fork=True)


def test_parse_resume_pick_with_id_errors() -> None:
    with pytest.raises(SystemExit):
        parse_resume_args(["--pick", "abc-123"])


def test_parse_resume_multiple_ids_errors() -> None:
    with pytest.raises(SystemExit):
        parse_resume_args(["abc-123", "def-456"])


def test_parse_resume_unknown_flag_errors() -> None:
    with pytest.raises(SystemExit):
        parse_resume_args(["--bogus"])
