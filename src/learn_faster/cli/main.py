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


def get_templates_dir() -> Path:
    """Get the templates directory from the installed package."""
    return Path(__file__).parent.parent / "templates"


def create_or_update_settings(claude_dir: Path) -> None:
    """Create or update .claude/settings.local.json."""
    settings_file = claude_dir / "settings.local.json"

    # Default settings for Learn FASTER
    default_settings = {
        "outputStyle": "learn-faster",
        "permissions": {
            "allow": [
                "Bash(python3 .learning/scripts/*)",
                "Bash(ls *)",
                "Read(.learning/**)",
                "Write(.learning/**)",
                "Write(**/*.md)",
                "Read(**/*.md)"
            ]
        }
    }

    if settings_file.exists():
        # Load existing settings
        with open(settings_file, "r") as f:
            settings = json.load(f)

        # Merge with defaults
        if "outputStyle" not in settings:
            settings["outputStyle"] = "learn-faster"

        if "permissions" not in settings:
            settings["permissions"] = default_settings["permissions"]
        else:
            # Merge permissions allow list
            if "allow" not in settings["permissions"]:
                settings["permissions"]["allow"] = []

            for perm in default_settings["permissions"]["allow"]:
                if perm not in settings["permissions"]["allow"]:
                    settings["permissions"]["allow"].append(perm)

        print(f"✓ Updated {settings_file}")
    else:
        # Create new settings file
        settings = default_settings
        print(f"✓ Created {settings_file}")

    # Write settings
    with open(settings_file, "w") as f:
        json.dump(settings, f, indent=2)


def init_project() -> None:
    """Initialize Learn FASTER in the current project."""
    import platform

    cwd = Path.cwd()
    templates_dir = get_templates_dir()

    print("🚀 Initializing Learn FASTER in current project...\n")

    # Ask about macOS Reminders (only on macOS)
    macos_reminders = False
    if platform.system() == "Darwin":
        response = input("📅 Enable macOS Reminders for review notifications? (y/n): ").strip().lower()
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
            print(f"✓ Copied agent: {file.name}")

    # Copy output styles
    styles_dest = claude_dir / "output-styles"
    styles_dest.mkdir(exist_ok=True)
    styles_src = templates_dir / "output_styles"
    if styles_src.exists():
        for file in styles_src.glob("*.md"):
            shutil.copy2(file, styles_dest / file.name)
            print(f"✓ Copied output style: {file.name}")

    # Copy commands
    commands_dest = claude_dir / "commands"
    commands_dest.mkdir(exist_ok=True)
    commands_src = templates_dir / "commands"
    if commands_src.exists():
        for file in commands_src.glob("*.md"):
            shutil.copy2(file, commands_dest / file.name)
            print(f"✓ Copied command: {file.name}")

    # Create/update settings.local.json
    create_or_update_settings(claude_dir)

    # Create .learning directory structure
    learning_dir = cwd / ".learning"
    learning_dir.mkdir(exist_ok=True)

    # Create config.json with macOS reminders preference
    config = {
        "macos_reminders_enabled": macos_reminders
    }
    config_path = learning_dir / "config.json"
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)
    print(f"✓ Created config.json (macOS Reminders: {'enabled' if macos_reminders else 'disabled'})")

    # Copy scripts
    scripts_dest = learning_dir / "scripts"
    scripts_dest.mkdir(exist_ok=True)
    scripts_src = templates_dir / "scripts"
    if scripts_src.exists():
        for file in scripts_src.glob("*.py"):
            shutil.copy2(file, scripts_dest / file.name)
            print(f"✓ Copied script: {file.name}")

    # Copy references
    references_dest = learning_dir / "references"
    references_dest.mkdir(exist_ok=True)
    references_src = templates_dir / "references"
    if references_src.exists():
        for file in references_src.glob("*.md"):
            shutil.copy2(file, references_dest / file.name)
            print(f"✓ Copied reference: {file.name}")

    # Copy CLAUDE.md to project root
    claude_md_src = templates_dir / "CLAUDE.md"
    claude_md_dest = cwd / "CLAUDE.md"
    if claude_md_src.exists() and not claude_md_dest.exists():
        shutil.copy2(claude_md_src, claude_md_dest)
        print(f"✓ Copied CLAUDE.md to project root")
    elif claude_md_dest.exists():
        print(f"⚠  CLAUDE.md already exists, skipping")

    print("\n✅ Learn FASTER initialization complete!\n")
    print("📁 Created structure:")
    print("   .claude/")
    print("   ├── agents/practice-creator.md")
    print("   ├── output-styles/learn-faster.md")
    print("   ├── commands/")
    print("   │   ├── learn.md")
    print("   │   ├── review.md")
    print("   │   └── progress.md")
    print("   └── settings.local.json")
    print()
    print("   .learning/")
    print("   ├── scripts/")
    print("   │   ├── init_learning.py")
    print("   │   ├── log_progress.py")
    print("   │   ├── review_scheduler.py")
    print("   │   └── generate_syllabus.py")
    print("   └── references/")
    print("       └── faster_framework.md")
    print()
    print("   CLAUDE.md")
    print()
    print("🎯 Next steps:")
    print("   1. Restart Claude Code to load new commands and style")
    print("   2. The 'learn-faster' output style is auto-activated")
    print("   3. Run: /learn \"Your Topic Name\"")
    print()
    print("Happy learning! 🚀📚")


def main() -> None:
    """Main CLI entry point."""
    if len(sys.argv) < 2:
        print("Learn FASTER - Accelerate learning with FASTER framework\n")
        print("Usage:")
        print("  uvx learn-faster init    Initialize in current project")
        print()
        print("For more info: https://github.com/cheukyin175/learn-faster-kit")
        sys.exit(0)

    command = sys.argv[1]

    if command == "init":
        init_project()
    elif command == "version":
        from learn_faster import __version__
        print(f"learn-faster version {__version__}")
    else:
        print(f"Unknown command: {command}")
        print("Available commands: init, version")
        sys.exit(1)


if __name__ == "__main__":
    main()
