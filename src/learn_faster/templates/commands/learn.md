---
description: Initialize a new learning topic $topic or continue learning an existing one using the FASTER framework
---

## Context

-   Learning directory: !`ls -d .learning 2>/dev/null`
-   Current topic: !`ls .learning/ 2>/dev/null`

**Note:** If `.learning/` doesn't exist, you'll initialize it. If it exists, check the topic folder name (ignore `scripts/`).

## Your Task

Initialize learning for the specified topic using the FASTER framework.

**If `.learning/` exists:**

-   Inform: "This project is already learning [topic name]"
-   Check for due reviews first (conduct before new learning if any)
-   Continue with current topic (1 project = 1 learning goal)

**If `.learning/` doesn't exist:**

1. **Gather learning preferences** with `AskUserQuestion`:

```json
[
    {
        "question": "What level do you want to achieve with [topic]?",
        "header": "Level",
        "multiSelect": false,
        "options": [
            {
                "label": "Beginner",
                "description": "Fundamentals and basic concepts"
            },
            {
                "label": "Intermediate",
                "description": "Practical skills and common patterns"
            },
            {
                "label": "Advanced",
                "description": "Deep expertise and edge cases"
            },
            {
                "label": "Expert",
                "description": "Mastery level, architecture, optimization"
            }
        ]
    },
    {
        "question": "What do you want to focus on?",
        "header": "Focus",
        "multiSelect": true,
        "options": [
            {
                "label": "Theory",
                "description": "Concepts, principles, how things work"
            },
            {
                "label": "Practice",
                "description": "Hands-on coding and building projects"
            },
            {
                "label": "Real-world",
                "description": "Production patterns and best practices"
            },
            {
                "label": "Interview prep",
                "description": "Common questions and problem-solving"
            }
        ]
    }
]
```

2. Run: `python3 .learning/scripts/init_learning.py "[topic name]" .learning`
3. Parse JSON output and follow `llm_directive`
4. **READ** `.learning/<topic-slug>/syllabus.md` to see the template structure
5. Generate comprehensive syllabus content **tailored to user's level and focus areas**
6. **Replace** the template placeholders with actual content
7. Update metadata: `"syllabus_generated": true` in `.learning/<topic-slug>/metadata.json`

**Follow the template structure:**

-   All sections from the template file (Overview, Prerequisites, Learning Objectives, etc.)
-   3-4 Phases with specific concepts + 🔨 hands-on projects
-   Checkboxes `- [ ]` for tracking progress

**After generation:**

-   Show first 2-3 learning items from Phase 1
-   Ask: "Ready to start with [first concept]?"
-   Suggest: "30min daily > 3hr weekly!"

**Important:**

-   Activate `/style learn-faster` for optimal coaching
-   Generate comprehensive syllabi (not minimal)
-   Include hands-on practice in every phase
