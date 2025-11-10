#!/usr/bin/env python3
"""
Learn FASTER CLI - One-time installer for Claude Code learning system.

Usage:
    uvx learn-faster init
"""

import sys
import shutil
import json
from pathlib import Path
from typing import Dict, Any


# ANSI color codes
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"

    # Colors
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    GRAY = "\033[90m"


BANNER = f"""{Colors.CYAN}
██╗     ███████╗ █████╗ ██████╗ ███╗   ██╗    ███████╗ █████╗ ███████╗████████╗███████╗██████╗
██║     ██╔════╝██╔══██╗██╔══██╗████╗  ██║    ██╔════╝██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔══██╗
██║     █████╗  ███████║██████╔╝██╔██╗ ██║    █████╗  ███████║███████╗   ██║   █████╗  ██████╔╝
██║     ██╔══╝  ██╔══██║██╔══██╗██║╚██╗██║    ██╔══╝  ██╔══██║╚════██║   ██║   ██╔══╝  ██╔══██╗
███████╗███████╗██║  ██║██║  ██║██║ ╚████║    ██║     ██║  ██║███████║   ██║   ███████╗██║  ██║
╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝    ╚═╝     ╚═╝  ╚═╝╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝
{Colors.RESET}"""


def print_success(msg: str) -> None:
    """Print success message in green."""
    print(f"{Colors.GREEN}✓{Colors.RESET} {msg}")


def print_info(msg: str) -> None:
    """Print info message in cyan."""
    print(f"{Colors.CYAN}{msg}{Colors.RESET}")


def print_warning(msg: str) -> None:
    """Print warning message in yellow."""
    print(f"{Colors.YELLOW}!{Colors.RESET} {msg}")


def print_header(msg: str) -> None:
    """Print header message in bold magenta."""
    print(f"{Colors.BOLD}{Colors.MAGENTA}{msg}{Colors.RESET}")


def print_dim(msg: str) -> None:
    """Print dimmed message."""
    print(f"{Colors.DIM}{msg}{Colors.RESET}")


def print_error(msg: str) -> None:
    """Print error message in red."""
    print(f"{Colors.RED}✗{Colors.RESET} {msg}")


def get_templates_dir() -> Path:
    """Get the templates directory from the installed package."""
    return Path(__file__).parent.parent / "templates"


def create_or_update_settings(claude_dir: Path) -> None:
    """Create or update .claude/settings.local.json."""
    settings_file = claude_dir / "settings.local.json"

    # Default settings for Learn FASTER
    default_settings = {
        "permissions": {
            "allow": [
                "Bash(python3 .learning/scripts/*)",
                "Bash(ls *)",
                "Read(.learning/**)",
                "Write(.learning/**)",
                "Write(**/*.md)",
                "Read(**/*.md)"
            ],
            "deny": [
                "Bash(rm -rf *)",
                "Bash(curl *)",
                "Read(.env)",
                "Read(.env.*)",
                "Write(.env)",
                "Write(.env.*)"
            ]
        },
        "companyAnnouncements": [
            "🚀 Learn FASTER is active! Use /learn \"Topic\" to start learning",
            "💡 Tip: Use /review to conduct spaced repetition reviews",
            "📊 Check your progress anytime with /progress"
        ]
    }

    if settings_file.exists():
        # Load existing settings
        with open(settings_file, "r") as f:
            settings = json.load(f)

        # Merge with defaults
        if "permissions" not in settings:
            settings["permissions"] = default_settings["permissions"]
        else:
            # Merge permissions allow list
            if "allow" not in settings["permissions"]:
                settings["permissions"]["allow"] = []

            for perm in default_settings["permissions"]["allow"]:
                if perm not in settings["permissions"]["allow"]:
                    settings["permissions"]["allow"].append(perm)

            # Merge permissions deny list
            if "deny" not in settings["permissions"]:
                settings["permissions"]["deny"] = []

            for perm in default_settings["permissions"]["deny"]:
                if perm not in settings["permissions"]["deny"]:
                    settings["permissions"]["deny"].append(perm)

        # Add company announcements if not present
        if "companyAnnouncements" not in settings:
            settings["companyAnnouncements"] = default_settings["companyAnnouncements"]

        print_success(f"Updated {settings_file}")
    else:
        # Create new settings file
        settings = default_settings
        print_success(f"Created {settings_file}")

    # Write settings
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
    except:
        return False


def init_project() -> None:
    """Initialize Learn FASTER in the current project."""
    import platform

    cwd = Path.cwd()
    templates_dir = get_templates_dir()

    print(BANNER)
    print_header("\nInitializing Learn FASTER in current project...\n")

    # Ask about macOS Reminders (only on macOS)
    macos_reminders = False
    if platform.system() == "Darwin":
        response = input(f"{Colors.CYAN}Enable macOS Reminders for review notifications? (y/n):{Colors.RESET} ").strip().lower()
        macos_reminders = response in ['y', 'yes']

    # Create .claude directory structure
    claude_dir = cwd / ".claude"
    claude_dir.mkdir(exist_ok=True)

    # Copy agents
    agents_dest = claude_dir / "agents"
    agents_dest.mkdir(exist_ok=True)
    agents_src = templates_dir / "agents"
    if agents_src.exists():
        for file in agents_src.glob("*.md"):
            shutil.copy2(file, agents_dest / file.name)
            print_success(f"Copied agent: {file.name}")

    # Copy commands
    commands_dest = claude_dir / "commands"
    commands_dest.mkdir(exist_ok=True)
    commands_src = templates_dir / "commands"
    if commands_src.exists():
        for file in commands_src.glob("*.md"):
            shutil.copy2(file, commands_dest / file.name)
            print_success(f"Copied command: {file.name}")

    # Create/update settings.local.json
    create_or_update_settings(claude_dir)

    # Create .learning directory structure
    learning_dir = cwd / ".learning"
    learning_dir.mkdir(exist_ok=True)

    # Create config.json with initialization flag
    config = {
        "initialized": True,
        "macos_reminders_enabled": macos_reminders
    }
    config_path = learning_dir / "config.json"
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)
    print_success(f"Created config.json (macOS Reminders: {'enabled' if macos_reminders else 'disabled'})")

    # Copy scripts
    scripts_dest = learning_dir / "scripts"
    scripts_dest.mkdir(exist_ok=True)
    scripts_src = templates_dir / "scripts"
    if scripts_src.exists():
        for file in scripts_src.glob("*.py"):
            shutil.copy2(file, scripts_dest / file.name)
            print_success(f"Copied script: {file.name}")

    # Copy references
    references_dest = learning_dir / "references"
    references_dest.mkdir(exist_ok=True)
    references_src = templates_dir / "references"
    if references_src.exists():
        for file in references_src.glob("*.md"):
            shutil.copy2(file, references_dest / file.name)
            print_success(f"Copied reference: {file.name}")

    # Copy instructions.md to project root as CLAUDE.md
    instructions_src = templates_dir / "instructions.md"
    claude_md_dest = cwd / "CLAUDE.md"
    if instructions_src.exists() and not claude_md_dest.exists():
        shutil.copy2(instructions_src, claude_md_dest)
        print_success("Copied instructions to CLAUDE.md in project root")
    elif claude_md_dest.exists():
        print_warning("CLAUDE.md already exists, skipping")

    print(f"\n{Colors.GREEN}{Colors.BOLD}Initialization complete!{Colors.RESET}\n")

    print_header("Available commands in Claude Code:")
    print(f"  {Colors.CYAN}/learn [topic]{Colors.RESET}    - Initialize or continue learning")
    print(f"  {Colors.CYAN}/review{Colors.RESET}           - Spaced repetition review session")
    print(f"  {Colors.CYAN}/progress{Colors.RESET}         - Show detailed progress report")
    print()


def launch_coach() -> None:
    """Launch Claude Code with learn-faster system prompt."""
    import subprocess

    # Get the path to the system prompt template
    templates_dir = Path(__file__).parent.parent / "templates"
    system_prompt_path = templates_dir / "system_prompts" / "learn-faster.md"

    if not system_prompt_path.exists():
        print_error("Error: learn-faster system prompt not found")
        print_dim(f"Expected at: {system_prompt_path}")
        sys.exit(1)

    # Read the system prompt content (skip frontmatter)
    with open(system_prompt_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Skip frontmatter (between --- lines)
    in_frontmatter = False
    content_lines = []
    for line in lines:
        if line.strip() == "---":
            if not in_frontmatter:
                in_frontmatter = True
                continue
            else:
                in_frontmatter = False
                continue
        if not in_frontmatter:
            content_lines.append(line)

    system_prompt = "".join(content_lines).strip()

    # Launch Claude Code with the system prompt
    print_info("Launching Claude Code in learning coach mode...")
    print_dim("(Using FASTER framework system prompt)\n")

    try:
        subprocess.run(
            ["claude", "--system-prompt", system_prompt],
            check=False
        )
    except FileNotFoundError:
        print_error("Error: 'claude' command not found")
        print_dim("Make sure Claude Code CLI is installed and in your PATH")
        print_dim("Install from: https://claude.ai/download")
        sys.exit(1)


def main() -> None:
    """Main CLI entry point."""
    # Check for explicit commands
    if len(sys.argv) >= 2:
        command = sys.argv[1]

        if command == "init":
            init_project()
            return
        elif command == "version":
            from learn_faster import __version__
            print(f"learn-faster version {__version__}")
            return
        elif command in ["help", "--help", "-h"]:
            print("Learn FASTER - Accelerate learning with FASTER framework\n")
            print("Usage:")
            print("  learn-faster           Auto-init and launch Claude Code in coach mode")
            print("  learn-faster init      Force re-initialization")
            print("  learn-faster version   Show version")
            print()
            print("For more info: https://github.com/cheukyin175/learn-faster-kit")
            return
        else:
            print_error(f"Unknown command: {command}")
            print_dim("Run 'learn-faster --help' for usage")
            sys.exit(1)

    # Default behavior: check init, then launch
    if not check_initialization():
        print_info("First-time setup detected. Initializing...")
        print()
        init_project()
        print()
        print_header("Launching Claude Code with FASTER framework...")
        print()
    else:
        print_info("Launching Claude Code in learning coach mode...")
        print()

    launch_coach()


if __name__ == "__main__":
    main()
