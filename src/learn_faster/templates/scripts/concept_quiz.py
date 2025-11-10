#!/usr/bin/env python3
"""
Generate quick conceptual multiple-choice quizzes based on least-reviewed concepts.
Called after progress logging to reinforce learning.
"""

import json
from pathlib import Path
from datetime import datetime


def get_least_asked_concepts(topic_slug: str, limit: int = 3, base_dir: str = ".learning"):
    """
    Get the least-asked concepts that need reinforcement.

    Args:
        topic_slug: Slug of the topic
        limit: Number of concepts to return (default 3)
        base_dir: Base directory for learning data

    Returns:
        List of concept dictionaries with review data
    """
    topic_dir = Path(base_dir) / topic_slug
    concepts_dir = topic_dir / "concepts"

    if not concepts_dir.exists():
        return []

    concepts = []
    for concept_file in concepts_dir.glob("*.json"):
        with open(concept_file, "r") as f:
            data = json.load(f)
            concepts.append({
                "concept": data["concept"],
                "slug": data["concept_slug"],
                "review_count": data.get("review_count", 0),
                "last_reviewed": data.get("last_reviewed"),
                "learned_date": data.get("learned_date")
            })

    # Sort by review_count (ascending) then by learned_date (oldest first)
    concepts.sort(key=lambda x: (x["review_count"], x["learned_date"]))

    return concepts[:limit]


def generate_quiz_directive(topic_slug: str, base_dir: str = ".learning"):
    """
    Generate LLM directive for creating MC questions about least-asked concepts.

    Args:
        topic_slug: Slug of the topic
        base_dir: Base directory for learning data

    Returns:
        JSON output with quiz directive for LLM
    """
    concepts = get_least_asked_concepts(topic_slug, limit=3, base_dir=base_dir)

    if not concepts:
        output = {
            "status": "no_concepts",
            "quiz_needed": False,
            "llm_directive": "No concepts available for quiz. Continue with learning."
        }
        print(json.dumps(output, indent=2))
        return

    # Build directive for LLM
    concept_names = [c["concept"] for c in concepts]

    directive = f"""
After logging progress, create a quick conceptual quiz using AskUserQuestion.

Pick ONE concept from these least-reviewed concepts: {', '.join(concept_names)}

Create a multiple-choice question that tests understanding (not memorization):
- Question should test conceptual understanding
- 4 plausible options (one correct, three reasonable distractors)
- After user answers, explain why the correct answer is right and why others are wrong
- Keep it quick (30 seconds to answer)

Example format for AskUserQuestion:
{{
  "question": "What is the main purpose of [concept]?",
  "header": "Quick Quiz",
  "multiSelect": false,
  "options": [
    {{"label": "Option A", "description": "Brief explanation"}},
    {{"label": "Option B", "description": "Brief explanation"}},
    {{"label": "Option C", "description": "Brief explanation"}},
    {{"label": "Option D", "description": "Brief explanation"}}
  ]
}}

After quiz, update the concept's quiz_count in .learning/{topic_slug}/concepts/[concept-slug].json
"""

    output = {
        "status": "quiz_ready",
        "quiz_needed": True,
        "least_reviewed_concepts": concepts,
        "llm_directive": directive.strip(),
        "suggested_prompt": f"Quick quiz time! Let's test your understanding of one of these: {', '.join(concept_names)}"
    }

    print(json.dumps(output, indent=2))


def record_quiz_attempt(topic_slug: str, concept: str, correct: bool, base_dir: str = ".learning"):
    """
    Record a quiz attempt for a concept.

    Args:
        topic_slug: Slug of the topic
        concept: Name of the concept
        correct: Whether the answer was correct
        base_dir: Base directory for learning data
    """
    topic_dir = Path(base_dir) / topic_slug
    concepts_dir = topic_dir / "concepts"

    # Find the concept file
    concept_slug = concept.lower().replace(" ", "-").replace("/", "-")
    concept_file = concepts_dir / f"{concept_slug}.json"

    if not concept_file.exists():
        print(f"❌ Concept '{concept}' not found")
        return False

    with open(concept_file, "r") as f:
        data = json.load(f)

    # Update quiz history
    if "quiz_history" not in data:
        data["quiz_history"] = []

    data["quiz_history"].append({
        "timestamp": datetime.now().isoformat(),
        "correct": correct
    })

    if "quiz_count" not in data:
        data["quiz_count"] = 0
    data["quiz_count"] += 1

    if "quiz_correct_count" not in data:
        data["quiz_correct_count"] = 0
    if correct:
        data["quiz_correct_count"] += 1

    with open(concept_file, "w") as f:
        json.dump(data, f, indent=2)

    accuracy = (data["quiz_correct_count"] / data["quiz_count"] * 100) if data["quiz_count"] > 0 else 0

    output = {
        "status": "success",
        "concept": concept,
        "correct": correct,
        "quiz_count": data["quiz_count"],
        "accuracy": round(accuracy, 1),
        "llm_directive": f"Quiz attempt recorded. {'Great job!' if correct else 'Keep practicing this concept.'}"
    }

    print(json.dumps(output, indent=2))
    return True


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage:")
        print("  Generate quiz:  python3 concept_quiz.py generate <topic_slug>")
        print("  Record attempt: python3 concept_quiz.py record <topic_slug> <concept> <correct>")
        sys.exit(1)

    command = sys.argv[1]

    if command == "generate" and len(sys.argv) >= 3:
        generate_quiz_directive(sys.argv[2])
    elif command == "record" and len(sys.argv) >= 5:
        concept = sys.argv[3]
        correct = sys.argv[4].lower() in ['true', '1', 'yes']
        record_quiz_attempt(sys.argv[2], concept, correct)
    else:
        print("❌ Invalid command or missing arguments")
