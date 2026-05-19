"""Project initialization for the Learn FASTER CLI."""

import json
import shutil
from pathlib import Path

import inquirer

from learn_faster.cli.agents import AGENT_PROFILES, DEFAULT_AGENT, get_agent_profile
from learn_faster.cli.paths import get_agent_templates_dir, get_shared_templates_dir
from learn_faster.cli.ui import (
    BANNER,
    Colors,
    print_header,
    print_success,
    print_warning,
)


MODE_NAMES = {
    "exam": "Exam-Oriented",
    "theory": "Theory-Focused",
    "practical": "Practical",
    "balanced": "Balanced",
    "programming": "Programming",
}


def create_or_update_settings(agent_dir: Path) -> None:
    """Create or update Claude Code settings.local.json."""
    settings_file = agent_dir / "settings.local.json"

    default_settings = {
        "permissions": {
            "allow": [
                "Bash(python3 .learning/scripts/:*)",
                "Bash(ls:*)",
                "Read(.learning/**)",
                "Write(.learning/**)",
                "Write(**/*.md)",
                "Read(**/*.md)",
            ],
            "deny": [
                "Bash(rm:*)",
                "Bash(curl:*)",
                "Read(.env)",
                "Read(.env.*)",
                "Write(.env)",
                "Write(.env.*)",
            ],
        },
        "companyAnnouncements": [
            '🚀 Learn FASTER is active! Use /learn "Topic" to start learning',
        ],
    }

    if settings_file.exists():
        with open(settings_file, "r") as f:
            settings = json.load(f)

        if "permissions" not in settings:
            settings["permissions"] = default_settings["permissions"]
        else:
            if "allow" not in settings["permissions"]:
                settings["permissions"]["allow"] = []

            for perm in default_settings["permissions"]["allow"]:
                if perm not in settings["permissions"]["allow"]:
                    settings["permissions"]["allow"].append(perm)

            if "deny" not in settings["permissions"]:
                settings["permissions"]["deny"] = []

            for perm in default_settings["permissions"]["deny"]:
                if perm not in settings["permissions"]["deny"]:
                    settings["permissions"]["deny"].append(perm)

        if "companyAnnouncements" not in settings:
            settings["companyAnnouncements"] = default_settings["companyAnnouncements"]

        print_success(f"Updated {settings_file}")
    else:
        settings = default_settings
        print_success(f"Created {settings_file}")

    with open(settings_file, "w") as f:
        json.dump(settings, f, indent=2)


def check_initialization() -> bool:
    """Check if project has been initialized."""
    config_path = Path.cwd() / ".learning" / "config.json"
    if not config_path.exists():
        return False

    try:
        with open(config_path, "r") as f:
            config = json.load(f)
        return config.get("initialized", False)
    except Exception:
        return False


def copy_markdown_templates(src: Path, dest: Path, label: str) -> None:
    """Copy Markdown templates from a directory when it exists."""
    if not src.exists():
        return

    dest.mkdir(exist_ok=True)
    for file in src.glob("*.md"):
        shutil.copy2(file, dest / file.name)
        print_success(f"Copied {label}: {file.name}")


def choose_agent(agent_name: str | None) -> str:
    """Choose an agent interactively unless one was provided."""
    if agent_name:
        return agent_name

    agent_question = [
        inquirer.List(
            "agent",
            message="Choose your agent",
            choices=[
                (profile.display_name, name)
                for name, profile in sorted(
                    AGENT_PROFILES.items(),
                    key=lambda item: 0 if item[0] == DEFAULT_AGENT else 1,
                )
            ],
            default=DEFAULT_AGENT,
        ),
    ]
    agent_answer = inquirer.prompt(agent_question)
    return agent_answer["agent"] if agent_answer else DEFAULT_AGENT


def init_project(agent_name: str | None = None) -> None:
    """Initialize Learn FASTER in the current project."""
    agent = get_agent_profile(choose_agent(agent_name))
    cwd = Path.cwd()
    agent_templates_dir = get_agent_templates_dir(agent.name)
    shared_templates_dir = get_shared_templates_dir()

    print(BANNER)
    print_header(f"\nInitializing Learn FASTER for {agent.display_name}...\n")

    learning_mode_question = [
        inquirer.List(
            "mode",
            message="Choose your learning mode",
            choices=[
                (
                    "Balanced         均衡 - Mix of theory, practice, and application / 理论与实践的平衡",
                    "balanced",
                ),
                (
                    "Exam-Oriented    应试 - Printable exam papers, practice tests, and certification prep / 刷题与备考",
                    "exam",
                ),
                (
                    "Theory-Focused   - Deep conceptual understanding and mental models",
                    "theory",
                ),
                (
                    "Practical        - Build projects immediately, learn by doing",
                    "practical",
                ),
                (
                    "Programming      - Learn programming through building projects",
                    "programming",
                ),
            ],
            default="balanced",
        ),
    ]

    mode_answer = inquirer.prompt(learning_mode_question)
    learning_mode = mode_answer["mode"] if mode_answer else "balanced"
    print_success(f"Selected: {MODE_NAMES[learning_mode]} mode\n")

    agent_dir = cwd / agent.config_dir
    agent_dir.mkdir(exist_ok=True)

    mode_templates_dir = agent_templates_dir / "modes" / learning_mode
    copy_markdown_templates(
        mode_templates_dir / "agents", agent_dir / "agents", "agent"
    )
    copy_markdown_templates(
        mode_templates_dir / "commands", agent_dir / "commands", "command"
    )

    if agent.supports_settings:
        create_or_update_settings(agent_dir)

    learning_dir = cwd / ".learning"
    learning_dir.mkdir(exist_ok=True)

    config = {
        "initialized": True,
        "agent": agent.name,
        "learning_mode": learning_mode,
    }
    config_path = learning_dir / "config.json"
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)
    print_success(
        f"Created config.json (Agent: {agent.display_name}, Mode: {MODE_NAMES[learning_mode]})"
    )

    scripts_dest = learning_dir / "scripts"
    scripts_dest.mkdir(exist_ok=True)
    scripts_src = shared_templates_dir / "scripts"
    if scripts_src.exists():
        for file in scripts_src.glob("*.py"):
            shutil.copy2(file, scripts_dest / file.name)
            print_success(f"Copied script: {file.name}")

    references_dest = learning_dir / "references"
    references_dest.mkdir(exist_ok=True)
    references_src = shared_templates_dir / "references"
    if references_src.exists():
        for file in references_src.glob("*.md"):
            shutil.copy2(file, references_dest / file.name)
            print_success(f"Copied reference: {file.name}")

    instructions_src = agent_templates_dir / "instructions.md"
    instructions_dest = cwd / agent.instruction_file
    if instructions_src.exists() and not instructions_dest.exists():
        shutil.copy2(instructions_src, instructions_dest)
        print_success(
            f"Copied instructions to {agent.instruction_file} in project root"
        )
    elif instructions_dest.exists():
        print_warning(f"{agent.instruction_file} already exists, skipping")

    print(f"\n{Colors.GREEN}{Colors.BOLD}Initialization complete!{Colors.RESET}\n")

    print_header(f"Available workflows in {agent.display_name}:")
    if agent.name == "claude-code":
        print(
            f"  {Colors.CYAN}/learn [topic]{Colors.RESET}    - Initialize or continue learning"
        )
        print(
            f"  {Colors.CYAN}/review{Colors.RESET}           - Spaced repetition review session"
        )
        print(
            f"  {Colors.CYAN}/progress{Colors.RESET}         - Show detailed progress report"
        )
    else:
        print(
            f"  {Colors.CYAN}Learn <topic>{Colors.RESET}      - Initialize or continue learning"
        )
        print(
            f"  {Colors.CYAN}Review{Colors.RESET}             - Run due spaced-repetition reviews"
        )
        print(
            f"  {Colors.CYAN}Progress{Colors.RESET}           - Summarize learning progress"
        )
    print()
