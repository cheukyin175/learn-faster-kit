# Learn FASTER

> Accelerate learning with the FASTER framework - spaced repetition, progress tracking, and hands-on practice using AI agent

**[Claude Code](https://claude.com/claude-code) Only** - This tool currently integrates with Claude Code's commands, agents, and output styles system.

## What is FASTER?

-   **F**orget: Beginner's mindset
-   **A**ct: Learn by doing
-   **S**tate: Optimize focus
-   **T**each: Explain to retain
-   **E**nter: Consistent sessions
-   **R**eview: Spaced repetition

## Features

-   Auto-generated syllabi tailored to your level and goals
-   Spaced repetition review system
-   Progress tracking and reports
-   Practice exercise generation
-   Teaching-based retention prompts

## Installation

**Prerequisites:** [uv](https://docs.astral.sh/uv/) package manager

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Option 1: Persistent Installation (Recommended)

Install once and use across all projects:

```bash
uv tool install learn-faster --from git+https://github.com/cheukyin175/learn-faster-kit.git
```

Then in any project directory:

```bash
learn-faster init
```

### Option 2: One-Time Use

Run directly without installation:

```bash
uvx --from git+https://github.com/cheukyin175/learn-faster-kit.git learn-faster init
```

### What Gets Installed

```
your-project/
├── .claude/
│   ├── agents/practice-creator.md
│   ├── output-styles/learn-faster.md
│   ├── commands/
│   │   ├── learn.md
│   │   ├── review.md
│   │   └── progress.md
│   └── settings.local.json
├── .learning/
│   ├── scripts/
│   │   ├── init_learning.py
│   │   ├── log_progress.py
│   │   ├── review_scheduler.py
│   │   └── generate_syllabus.py
│   └── references/faster_framework.md
└── CLAUDE.md
```

## Quick Start

1. **Install in your project**

    ```bash
    cd your-project
    learn-faster init
    ```

2. **Start Claude Code** to load new commands and output style

3. **Start learning**
    ```bash
    /learn "React Hooks"
    ```

## Commands

-   `/learn [topic]` - Initialize or continue learning a topic
-   `/review` - Conduct spaced repetition review session
-   `/progress` - Show detailed progress report

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/cheukyin175/learn-faster-kit.git
cd learn-faster-kit

# Install uv if needed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync
```

## Requirements

-   Python 3.12+
-   [Claude Code](https://claude.com/claude-code)
-   [uv](https://docs.astral.sh/uv/) package manager

## License

MIT License - See LICENSE file for details

---

**Master any topic faster** with spaced repetition, active practice, and teaching-based reinforcement.
