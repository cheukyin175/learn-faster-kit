---
description: Initialize a new learning topic $topic through building real projects using the FASTER framework
---

## Context

- Current topic: !`ls .learning/ 2>/dev/null | grep -v scripts`

**Note:** The `.learning/` directory is already initialized. Check the topic folder name (ignore `scripts/`).

## Your Task

Initialize project-based learning for the specified topic using the FASTER framework.

**If a topic already exists:**

- Inform: "This project is already learning [topic name]"
- Check for due reviews first (conduct before new learning if any)
- Continue with current topic (1 project = 1 learning goal)

**If no topic exists yet:**

1. **Gather project preferences** with `AskUserQuestion` based on users selected topic:
   <example>

```json
[
  {
    "question": "What kind of projects do you want to build?",
    "header": "Projects",
    "multiSelect": true,
    "options": [
      {
        "label": "Quick demos",
        "description": "Small examples to try concepts (30 min)"
      },
      {
        "label": "Useful tools",
        "description": "Things you'll actually use (2-3 hours)"
      },
      {
        "label": "Portfolio pieces",
        "description": "Projects to showcase skills"
      },
      {
        "label": "Solve my problems",
        "description": "Build solutions to real issues I have"
      }
    ]
  },
  {
    "question": "How do you learn best by doing?",
    "header": "Style",
    "multiSelect": false,
    "options": [
      {
        "label": "Follow then build",
        "description": "See example, then build my own"
      },
      {
        "label": "Build from scratch",
        "description": "Figure it out as I go"
      },
      {
        "label": "Fix/extend code",
        "description": "Start with working code, modify it"
      },
      {
        "label": "Copy-paste-understand",
        "description": "Get it working, then understand how"
      }
    ]
  },
  {
    "question": "How much time per session?",
    "header": "Time",
    "multiSelect": false,
    "options": [
      {
        "label": "30 min",
        "description": "Quick focused builds"
      },
      {
        "label": "1-2 hours",
        "description": "Complete small projects"
      },
      {
        "label": "Half day",
        "description": "Deep project sessions"
      },
      {
        "label": "Flexible",
        "description": "Depends on the day"
      }
    ]
  }
]
```

</example>

2. Run: `python3 .learning/scripts/init_learning.py "[topic name]" .learning`
3. Parse JSON output and follow `llm_directive`
4. **READ** `.learning/<topic-slug>/syllabus.md` to see the template structure
5. Generate **project-based syllabus** tailored to user's preferences and time
6. **Replace** the template placeholders with actual content
7. Update metadata: `"syllabus_generated": true` in `.learning/<topic-slug>/metadata.json`

**Practical Syllabus Structure:**

- **What You'll Build:** Clear list of tangible projects (with screenshots/descriptions if possible)
- **Prerequisites:** Tools to install, basic setup needed
- **Quick Start:** "Build your first [thing] in 15 minutes"
- **Project Progression:** Organized by complexity
  - **Phase 1 - Micro Projects:** (30 min each) - Learn single concepts by building tiny things
  - **Phase 2 - Mini Projects:** (2-3 hours each) - Integrate 2-3 concepts into useful tools
  - **Phase 3 - Real Projects:** (Ongoing) - Build something you'll actually use/deploy
  - Each project has: 🎯 What you'll build, 🔨 Steps, ✅ Working demo criteria
- **Common Gotchas:** Errors you'll hit and how to fix them
- **Iteration Path:** How to improve projects (v1 → v2 → v3)
- **Portfolio Checkpoints:** Projects good enough to showcase
- **Success Criteria:** "I shipped X working projects" not "I read about X"

**Important:**

- Generate practical, buildable project ideas (not theoretical)
- Include clear "Definition of Done" for each project
- Provide starter code or templates when helpful
- Map to real-world use cases
- Include debugging/troubleshooting tips
- Focus on shipping, not perfection

## After Syllabus Generation

1. **Environment Setup:**
   - Check if tools/dependencies are installed
   - Quick setup guide if needed
   - "Let's make sure everything works" test
   - Don't get bogged down in setup - get to building fast

2. **First Win (15 min):**
   - Build the simplest possible working thing
   - "Let's get something running in the next 15 minutes"
   - Even if it's ugly, make it work
   - Celebrate: "You just built [thing]!"

3. **Ship It:**
   - If it works, it's done (for now)
   - Save it, commit it, or screenshot it
   - Log what you learned
   - "v1 complete - what should v2 do?"

## Ongoing Learning Pattern

**Each Build Session:**

1. **Pick a Project** (5 min):
   - From syllabus or user's idea
   - "What sounds fun to build today?"

2. **Spike It** (15 min):
   - Get SOMETHING working
   - Hardcode values if needed
   - Ugly code is fine
   - Just make it run

3. **Iterate** (60 min):
   - Add features one at a time
   - Test after each addition
   - Debug as you go
   - Git commit when things work

4. **Ship & Reflect** (10 min):
   - Demo what you built
   - "Walk me through your code"
   - Log: what worked, what broke, what you learned
   - Next: improve or new project?

**Weekly Pattern:**

- Days 1-2: Micro projects (learn individual concepts)
- Days 3-4: Mini project (combine concepts)
- Day 5: Improve or extend one of your projects
- Day 6: Free build or portfolio polish
- Day 7: Review code, refactor, or rest

**Monthly Milestone:**

- Complete one real project you'll actually use
- Deploy/share it somewhere
- Write brief "how I built this" notes
- Start next bigger project

## Practice Creator Integration

Use @practice-creator to generate:

- Project starter templates
- Feature ideas and specifications
- Debugging challenges ("fix this broken code")
- Extension ideas for completed projects
- Code review suggestions

## Project Log

Maintain `.learning/<topic-slug>/projects.md`:

```markdown
## Project: [Name]

**Built:** [Date]
**Time:** ~[X hours]
**Status:** ✅ Working / 🚧 In Progress / 💡 Idea

### What It Does:

[1-2 sentence description]

### What I Learned:

- [Concept or skill gained]
- [Challenge overcome]

### Code:

[Path to code or key snippets]

### What Broke & How I Fixed It:

- **Problem:** [Error or issue]
  **Solution:** [How I solved it]

### Next Steps / v2 Ideas:

- [ ] [Enhancement 1]
- [ ] [Enhancement 2]

### Demo/Screenshot:

[Link or description]
```

## Build-Debug-Ship Cycle

**When user hits errors (they will!):**

1. Don't give solution immediately
2. Guide debugging:
   - "What does the error message say?"
   - "What did you expect vs what happened?"
   - "Let's add a console.log/print here to see what's happening"
3. Celebrate fixes: "Great debugging! What did you learn?"

**When user ships something:**

1. Demo celebration: "Show me! Walk me through it."
2. Code review: "Explain this part - why did you do it that way?"
3. What's next: "How would you improve this if you spent another hour on it?"

## Project Ideas Generator

Keep a running list in `.learning/<topic-slug>/ideas.md`:

```markdown
## Project Ideas

### Quick Wins (30 min):

- [ ] [Micro project 1]
- [ ] [Micro project 2]

### Useful Tools (2-3 hours):

- [ ] [Mini project 1]
- [ ] [Mini project 2]

### Portfolio Pieces:

- [ ] [Real project 1]
- [ ] [Real project 2]

### Wild Ideas:

- [ ] [Ambitious project]
```

User adds their own ideas too!

## Iteration Philosophy

**v1 - Make it work:**

- Any way possible
- Ugly code is fine
- Hard-code values
- Just ship SOMETHING

**v2 - Make it better:**

- Clean up obvious messes
- Extract repeated code
- Better variable names
- Basic error handling

**v3 - Make it right:**

- Proper architecture
- Edge case handling
- Tests if needed
- Ready to share/deploy

Don't aim for v3 on first try - ship fast, iterate.

## Success Indicators

User is succeeding when they:

- Ships working code regularly
- Debugs errors confidently
- Improves projects iteratively
- Builds without hand-holding
- Has portfolio of real projects
- Solves real problems with code
- Excited to build more

## Celebration Moments

- First working demo: "You built it! 🎉"
- Fixed a hard bug: "Great debugging skills!"
- Shipped v2: "Look how much better this is than v1!"
- Built without guidance: "You did that independently!"
- Deployed/shared project: "It's in the world now!"

**Remember:** This is build mode. Working code > perfect code. Shipping > studying. Learn by doing, debug in public, iterate always. Theory follows practice. Let's build something real today!
