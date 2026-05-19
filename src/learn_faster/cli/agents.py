"""Agent profile definitions for generated Learn FASTER assets."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AgentProfile:
    name: str
    display_name: str
    config_dir: str
    executable: str
    instruction_file: str
    launch_style: str
    install_url: str
    supports_settings: bool = False
    plan_mode_cmd: str = ""


AGENT_PROFILES = {
    "claude-code": AgentProfile(
        name="claude-code",
        display_name="Claude Code",
        config_dir=".claude",
        executable="claude",
        instruction_file="CLAUDE.md",
        launch_style="system-prompt",
        install_url="https://claude.ai/download",
        supports_settings=True,
        plan_mode_cmd="--permission-mode plan",
    ),
    "codex": AgentProfile(
        name="codex",
        display_name="Codex",
        config_dir=".codex",
        executable="codex",
        instruction_file="AGENTS.md",
        launch_style="prompt",
        install_url="https://developers.openai.com/codex",
        plan_mode_cmd="--enable collaboration_modes",
    ),
}

DEFAULT_AGENT = "claude-code"


def get_agent_profile(agent_name: str | None = None) -> AgentProfile:
    """Return an agent profile by name, falling back to the default agent."""
    normalized_name = agent_name or DEFAULT_AGENT
    try:
        return AGENT_PROFILES[normalized_name]
    except KeyError as exc:
        supported_agents = ", ".join(sorted(AGENT_PROFILES))
        raise ValueError(
            f"Unsupported agent '{normalized_name}'. Supported agents: {supported_agents}"
        ) from exc
