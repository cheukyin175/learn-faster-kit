#!/usr/bin/env python3
"""
Learn FASTER CLI - One-time installer for agent-based learning systems.

Usage:
    uvx learn-faster init
"""

import sys

from learn_faster.cli.agents import AGENT_PROFILES
from learn_faster.cli.installer import check_initialization, init_project
from learn_faster.cli.launcher import launch_coach
from learn_faster.cli.ui import print_dim, print_error, print_header, print_info


def print_help() -> None:
    """Print CLI usage information."""
    print("Learn FASTER - Accelerate learning with FASTER framework\n")
    print("Usage:")
    print("  learn-faster           Auto-init and launch the configured agent in coach mode")
    print("  learn-faster init      Force re-initialization")
    print("  learn-faster init --agent claude-code")
    print("  learn-faster init --agent codex")
    print("  learn-faster version   Show version")
    print()
    print(f"Supported agents: {', '.join(sorted(AGENT_PROFILES))}")
    print("For more info: https://github.com/cheukyin175/learn-faster-kit")


def parse_agent_arg(args: list[str]) -> str | None:
    """Parse an optional --agent value from a command argument list."""
    if not args:
        return None

    if len(args) == 2 and args[0] == "--agent":
        return args[1]

    print_error("Invalid arguments")
    print_dim("Usage: learn-faster init [--agent claude-code|codex]")
    sys.exit(1)


def main() -> None:
    """Main CLI entry point."""
    if len(sys.argv) >= 2:
        command = sys.argv[1]

        if command == "init":
            try:
                init_project(agent_name=parse_agent_arg(sys.argv[2:]))
            except ValueError as exc:
                print_error(str(exc))
                sys.exit(1)
            return
        if command == "version":
            from learn_faster import __version__

            print(f"learn-faster version {__version__}")
            return
        if command in ["help", "--help", "-h"]:
            print_help()
            return

        print_error(f"Unknown command: {command}")
        print_dim("Run 'learn-faster --help' for usage")
        sys.exit(1)

    if not check_initialization():
        print_info("First-time setup detected. Initializing...")
        print()
        init_project()
        print()
        print_header("Launching configured agent with FASTER framework...")
        print()
        launch_coach(auto_review=False, initialize=True)
    else:
        print_info("Launching configured agent in learning coach mode...")
        print_dim("(Starting with /review to check for due reviews)\n")
        launch_coach(auto_review=True)


if __name__ == "__main__":
    main()
