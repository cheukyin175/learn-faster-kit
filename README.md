# Learn FASTER

> Accelerate learning and improve retention through the FASTER framework with spaced repetition, progress tracking, and hands-on practice.

## Overview

**Learn FASTER** helps you master any topic using proven learning science principles. It manages your learning journey with syllabus generation, spaced repetition reviews, progress tracking, and practice exercise creation.

### FASTER Framework

- **F**orget: Clear your mind, embrace beginner's mindset
- **A**ct: Learn by doing, not just consuming
- **S**tate: Optimize focus and energy for learning
- **T**each: Explain concepts to reinforce understanding
- **E**nter: Schedule consistent learning sessions
- **R**eview: Combat forgetting with spaced repetition

## Features

✨ **Automatic Syllabus Generation** - Comprehensive learning paths created instantly for any topic
📅 **Spaced Repetition** - Reviews scheduled at optimal intervals (1d → 3d → 7d → 14d → 30d → 60d → 90d)
📊 **Progress Tracking** - Session logs, mastery checklists, and progress reports
🔨 **Practice Creator** - Agent generates hands-on exercises and projects
🧠 **Teaching Integration** - Prompts you to explain concepts for better retention
✅ **Self-Contained** - Everything installed in your project directory
🤖 **Proactive** - Automatically checks for due reviews and suggests next steps

## Installation

### Option 1: Persistent Installation (Recommended)

Install once and use across all projects:

```bash
uv tool install learn-faster --from git+https://github.com/yourusername/learn-faster.git
```

Then in any project directory:

```bash
learn-faster init
```

### Option 2: One-Time Use

Run directly without installation:

```bash
uvx --from git+https://github.com/yourusername/learn-faster.git learn-faster init
```

### What Gets Installed

After running `learn-faster init`, your project will have:

```
your-project/
├── .claude/
│   ├── agents/
│   │   └── practice-creator.md
│   ├── output-styles/
│   │   └── learn-faster.md
│   ├── commands/
│   │   ├── learn.md
│   │   ├── review.md
│   │   └── progress.md
│   └── settings.local.json         # Auto-activates learn-faster style
└── .learning/
    ├── scripts/                     # Python utilities
    │   ├── init_learning.py
    │   ├── log_progress.py
    │   ├── review_scheduler.py
    │   └── generate_syllabus.py
    └── references/
        └── faster_framework.md
```

## Quick Start

### 1. Install in your project

```bash
cd your-project
learn-faster init
```

### 2. Restart Claude Code

Restart Claude Code to load the new commands and output style.

### 3. Start learning!

```bash
/learn "React Hooks"
```

The system will:
1. Create a comprehensive syllabus
2. Set up progress tracking
3. Initialize spaced repetition schedule
4. Switch to learning coach mode

## Usage

### Commands

**`/learn [topic]`** - Initialize or continue learning a topic
```bash
/learn "Docker Containers"
/learn "System Design Patterns"
```

**`/review`** - Conduct spaced repetition review session
```bash
/review
```

**`/progress`** - Show detailed progress report
```bash
/progress
```

### Learning Session Flow

Every session follows this pattern:

1. **Review Check** - Automatically checks for concepts due for review
2. **State Check** - "Are you focused and ready?"
3. **Learn** - Work through syllabus items with hands-on practice
4. **Teach** - Explain concepts back to reinforce learning
5. **Log** - Progress automatically tracked
6. **Schedule** - Concepts added to review schedule

### Practice Exercises

Request exercises anytime:

```
"Create a practice exercise for useState"
"I need a mini-project to practice hooks"
"Generate a comprehensive project for this phase"
```

The **practice-creator** agent generates:
- **Micro-exercises** (5-10 min) for single concepts
- **Mini-projects** (30-60 min) integrating 2-3 concepts
- **Comprehensive projects** (2-4 hours) for full phases

## How It Works

### Output Style

The `learn-faster` output style (auto-activated) transforms Claude from a code writer into a learning coach who:
- Guides discovery instead of providing solutions
- Uses Socratic questioning
- Prompts you to teach concepts back
- Celebrates progress and maintains motivation

### Spaced Repetition

Reviews are scheduled using proven intervals:
- **Day 1**: Initial learning
- **Day 2**: First review (1 day later)
- **Day 5**: Second review (3 days later)
- **Day 12**: Third review (7 days later)
- **Day 26**: Fourth review (14 days later)
- **Day 56**: Fifth review (30 days later)
- **Day 116**: Sixth review (60 days later)
- **Day 206**: Seventh review (90 days later)

### Active Learning

Every learning activity is **active**:
- ❌ No passive reading or video watching
- ✅ Build projects immediately
- ✅ Write code and create examples
- ✅ Explain concepts in your own words
- ✅ Teach to solidify understanding

## Best Practices

### For Learners

1. **Be Consistent** - 30 min daily beats 3 hours weekly
2. **Trust the Reviews** - Don't skip spaced repetition
3. **Teach Often** - Explaining cements understanding
4. **Practice Immediately** - Apply concepts within 5 minutes
5. **Track Progress** - Celebrate wins and identify gaps

### Project Structure

- **1 project = 1 learning goal** - Each project directory focuses on mastering one specific topic
- **`.learning/`** exists = active learning in this project
- When starting a new topic, create a new project directory or complete the current one first

## Customization

### Modify Review Intervals

Edit `.learning/scripts/review_scheduler.py`:

```python
REVIEW_INTERVALS = [1, 3, 7, 14, 30, 60, 90]  # days
```

### Adjust Syllabus Templates

Edit generated syllabi directly in `.learning/<topic-slug>/syllabus.md`

### Customize Commands

Edit command files in `.claude/commands/` to adjust behavior

## Troubleshooting

### Scripts not executing

**Problem**: Permission errors with Python scripts
**Solution**: Ensure Python 3.7+ is installed and scripts are executable:

```bash
chmod +x .learning/scripts/*.py
```

### Reviews not showing

**Problem**: Reviews aren't being suggested
**Solution**: Check that concepts were added to review schedule after logging progress:

```bash
cat .learning/<topic-slug>/review_schedule.json
```

### Commands not available

**Problem**: Commands don't appear after init
**Solution**: Restart Claude Code to load new commands and output style

## Requirements

- **Python**: 3.7 or higher
- **Claude Code**: Latest version
- **uv**: For installation (install via `curl -LsSf https://astral.sh/uv/install.sh | sh`)

## Contributing

Found a bug or have a feature request? Please create an issue or submit a pull request!

### Development Setup

1. Clone the repository
2. Install dependencies: `uv sync`
3. Make changes to templates, commands, or scripts
4. Test with `learn-faster init` in a test directory
5. Submit PR with description

## License

MIT License - See LICENSE file for details

## Credits

Based on learning science research and the FASTER framework for accelerated learning and retention.

---

**Happy Learning! 🚀📚**

Master any topic faster with spaced repetition, active practice, and teaching-based reinforcement.
