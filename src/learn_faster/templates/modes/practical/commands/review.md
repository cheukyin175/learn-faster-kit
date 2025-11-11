---
description: Conduct spaced repetition review session for learned concepts
---

## Context

- Learning directory: !`ls -d .learning 2>/dev/null`
- Current topic: !`ls .learning/ 2>/dev/null`

**Note:** If `.learning/` doesn't exist, inform user to run `/learn [topic]`. Check topic folders (ignore `scripts/`).

## Your Task

Conduct spaced repetition reviews to combat forgetting and reinforce learning.

**If no `.learning/`:**

- Inform: "No learning in progress. Use `/learn [topic]` to start!"

**If reviews due:**

For each concept in review list:

1. Present: "Let's review: [Concept Name]"
2. Prompt teaching (rotate):
   - "Explain [concept] in your own words"
   - "How would you teach [concept] to a beginner?"
   - "What's the key idea behind [concept]?"
3. Listen to user's explanation
4. Evaluate:
   - Clear & accurate → Praise, mark reviewed
   - Partial → Ask clarifying questions, guide to fill gaps
   - Incorrect → Gently correct, provide hints
5. Mark reviewed: `python3 .learning/scripts/review_scheduler.py review <topic-slug> "[Concept]"`

**After all reviews:**

- Celebrate: "Great job! Reviewed N concepts! 🎉"
- Show next review date
- Use `AskUserQuestion` for next action:

```json
{
  "question": "What would you like to do next?",
  "header": "Next",
  "multiSelect": false,
  "options": [
    {
      "label": "Learn new",
      "description": "Continue with next syllabus item"
    },
    {
      "label": "Practice",
      "description": "Work on hands-on exercises"
    },
    {
      "label": "Take break",
      "description": "Come back later"
    }
  ]
}
```

**If no reviews due:**

- Inform: "No reviews due today! Next: [date]"
- Suggest continuing with new material

**Handling forgotten concepts:**

- Don't give answer immediately
- Provide hints: "It's related to [context]..."
- If still stuck: Review briefly, reschedule for tomorrow
- Reschedule: `python3 .learning/scripts/review_scheduler.py add <topic-slug> "[Concept]"`

**Key principle:** Active recall (user reconstructs from memory), not passive recognition
