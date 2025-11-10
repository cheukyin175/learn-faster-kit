#!/usr/bin/env python3
"""
Log daily learning progress for a topic.
"""

import json
from datetime import datetime
from pathlib import Path


def log_progress(topic_slug: str, content: str, concepts_learned: list = None, base_dir: str = ".learning"):
    """
    Add a progress entry to the learning log.

    Args:
        topic_slug: Slug of the topic (e.g., 'react-hooks')
        content: Description of what was learned
        concepts_learned: List of concepts/skills learned in this session
        base_dir: Base directory for learning data
    """
    topic_dir = Path(base_dir) / topic_slug

    if not topic_dir.exists():
        print(f"❌ Topic '{topic_slug}' not found. Initialize it first.")
        return False

    # Update metadata
    metadata_path = topic_dir / "metadata.json"
    with open(metadata_path, "r") as f:
        metadata = json.load(f)

    metadata["total_sessions"] += 1
    metadata["last_session"] = datetime.now().isoformat()

    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=2)

    # Add to progress log
    progress_path = topic_dir / "progress.md"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    with open(progress_path, "a") as f:
        f.write(f"\n### Session {metadata['total_sessions']} - {timestamp}\n\n")
        f.write(f"{content}\n\n")

        if concepts_learned:
            f.write("**Concepts learned:**\n")
            for concept in concepts_learned:
                f.write(f"- {concept}\n")
            f.write("\n")

    # Output structured JSON for LLM parsing
    directive = ""
    if concepts_learned:
        directive = f"1. Add these concepts to review schedule: {concepts_learned}. Use 'python3 .learning/scripts/review_scheduler.py add {topic_slug} <concept>' for each.\n2. After adding concepts, run 'python3 .learning/scripts/concept_quiz.py generate {topic_slug}' to generate a quick quiz on least-reviewed concepts."
    else:
        directive = f"No new concepts to add. Run 'python3 .learning/scripts/concept_quiz.py generate {topic_slug}' to quiz on existing concepts."

    output = {
        "status": "success",
        "session_number": metadata['total_sessions'],
        "concepts_logged": concepts_learned if concepts_learned else [],
        "total_sessions": metadata['total_sessions'],
        "next_action": "add_to_review_schedule_and_quiz" if concepts_learned else "quiz_only",
        "llm_directive": directive,
        "suggested_response": f"Session {metadata['total_sessions']} logged!" + (f" Added {len(concepts_learned)} concept(s) to track." if concepts_learned else "")
    }

    print(json.dumps(output, indent=2))
    return True


def get_recent_progress(topic_slug: str, sessions: int = 3, base_dir: str = ".learning"):
    """
    Retrieve recent progress entries for review.

    Args:
        topic_slug: Slug of the topic
        sessions: Number of recent sessions to retrieve
        base_dir: Base directory for learning data

    Returns:
        String containing recent progress entries
    """
    topic_dir = Path(base_dir) / topic_slug
    progress_path = topic_dir / "progress.md"

    if not progress_path.exists():
        return None

    with open(progress_path, "r") as f:
        content = f.read()

    # Extract session entries (simple approach - could be enhanced)
    lines = content.split("\n")
    session_lines = []
    in_session = False
    session_count = 0

    for line in reversed(lines):
        if line.startswith("### Session"):
            session_count += 1
            if session_count > sessions:
                break
            in_session = True

        if in_session:
            session_lines.insert(0, line)

    return "\n".join(session_lines)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage: python3 log_progress.py <topic_slug> <content> [concepts...]")
        print("\nExample: python3 log_progress.py react-hooks 'Learned useState and useEffect' 'useState' 'useEffect'")
        sys.exit(1)

    topic = sys.argv[1]
    content = sys.argv[2]
    concepts = sys.argv[3:] if len(sys.argv) > 3 else None

    log_progress(topic, content, concepts)
