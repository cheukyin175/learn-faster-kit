"""Agent launch logic for the Learn FASTER CLI."""

import json
import subprocess
import sys
from pathlib import Path

from learn_faster.cli.agents import DEFAULT_AGENT, AgentProfile, get_agent_profile
from learn_faster.cli.paths import get_agent_templates_dir
from learn_faster.cli.ui import print_dim, print_error, print_info


def get_project_config() -> dict:
    """Read Learn FASTER config for the current project."""
    config_path = Path.cwd() / ".learning" / "config.json"
    if not config_path.exists():
        return {}

    try:
        with open(config_path, "r") as f:
            return json.load(f)
    except Exception:
        return {}


def read_system_prompt(agent: AgentProfile, learning_mode: str) -> str:
    """Read a mode system prompt and remove Markdown frontmatter."""
    system_prompt_path = (
        get_agent_templates_dir(agent.name)
        / "modes"
        / learning_mode
        / "system_prompts"
        / "learn-faster.md"
    )

    if not system_prompt_path.exists():
        print_error(
            f"Error: System prompt for '{learning_mode}' mode not found for {agent.display_name}"
        )
        print_dim(f"Expected at: {system_prompt_path}")
        sys.exit(1)

    with open(system_prompt_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    in_frontmatter = False
    content_lines = []
    for line in lines:
        if line.strip() == "---":
            in_frontmatter = not in_frontmatter
            continue
        if not in_frontmatter:
            content_lines.append(line)

    return "".join(content_lines).strip()


def launch_coach(auto_review: bool = False, initialize: bool = False) -> None:
    """Launch the configured agent with the learn-faster system prompt."""
    config = get_project_config()
    try:
        agent = get_agent_profile(config.get("agent", DEFAULT_AGENT))
    except ValueError as exc:
        print_error(str(exc))
        sys.exit(1)

    learning_mode = config.get("learning_mode", "balanced")
    system_prompt = read_system_prompt(agent, learning_mode)

    print_info(f"Launching {agent.display_name} in learning coach mode...")
    print_dim("(Using FASTER framework system prompt)\n")

    if agent.launch_style == "system-prompt":
        cmd = [agent.executable, "--system-prompt", system_prompt]
        if initialize:
            cmd.append(agent.plan_mode_cmd)
        if auto_review:
            cmd.extend(["/review"])
    elif agent.launch_style == "prompt":
        startup_prompt = system_prompt
        if auto_review:
            startup_prompt = f"{system_prompt}\n\nStart by checking for due reviews."
        cmd = [agent.executable, startup_prompt]
    else:
        print_error(
            f"Unsupported launch style '{agent.launch_style}' for {agent.display_name}"
        )
        sys.exit(1)

    try:
        subprocess.run(cmd, check=False)
    except FileNotFoundError:
        print_error(f"Error: '{agent.executable}' command not found")
        print_dim(f"Make sure {agent.display_name} CLI is installed and in your PATH")
        print_dim(f"Install from: {agent.install_url}")
        sys.exit(1)
