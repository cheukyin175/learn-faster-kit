#!/usr/bin/env python3
"""
Generate a structured learning syllabus for a topic.
This is a helper that Claude will use to create comprehensive learning paths.
"""

import json
from pathlib import Path
from datetime import datetime


def update_syllabus(topic_slug: str, syllabus_content: str, base_dir: str = ".learning"):
    """
    Update the syllabus file with generated content.

    Args:
        topic_slug: Slug of the topic
        syllabus_content: Markdown content for the syllabus
        base_dir: Base directory for learning data
    """
    topic_dir = Path(base_dir) / topic_slug
    syllabus_path = topic_dir / "syllabus.md"

    if not topic_dir.exists():
        print(f"❌ Topic '{topic_slug}' not found.")
        return False

    with open(syllabus_path, "w") as f:
        f.write(syllabus_content)

    # Update metadata
    metadata_path = topic_dir / "metadata.json"
    with open(metadata_path, "r") as f:
        metadata = json.load(f)

    metadata["syllabus_generated"] = True
    metadata["syllabus_updated_at"] = datetime.now().isoformat()

    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=2)

    print(f"✅ Syllabus updated for '{topic_slug}'")
    print(f"📄 {syllabus_path}")

    return True


def get_topic_info(topic_slug: str, base_dir: str = ".learning"):
    """
    Get information about a learning topic.

    Args:
        topic_slug: Slug of the topic
        base_dir: Base directory for learning data

    Returns:
        Dictionary with topic information
    """
    topic_dir = Path(base_dir) / topic_slug

    if not topic_dir.exists():
        return None

    metadata_path = topic_dir / "metadata.json"
    with open(metadata_path, "r") as f:
        metadata = json.load(f)

    return {
        "topic": metadata["topic"],
        "status": metadata["status"],
        "sessions": metadata["total_sessions"],
        "syllabus_exists": metadata.get("syllabus_generated", False),
        "directory": str(topic_dir)
    }


def list_topics(base_dir: str = ".learning"):
    """
    List all learning topics.

    Args:
        base_dir: Base directory for learning data

    Returns:
        List of topic information dictionaries
    """
    learning_dir = Path(base_dir)

    if not learning_dir.exists():
        return []

    topics = []
    for topic_dir in learning_dir.iterdir():
        if topic_dir.is_dir() and (topic_dir / "metadata.json").exists():
            info = get_topic_info(topic_dir.name, base_dir)
            if info:
                topics.append(info)

    return topics


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage:")
        print("  List topics:  python3 generate_syllabus.py list")
        print("  Topic info:   python3 generate_syllabus.py info <topic_slug>")
        sys.exit(1)

    command = sys.argv[1]

    if command == "list":
        topics = list_topics()
        if not topics:
            output = {
                "status": "no_topics",
                "topics": [],
                "llm_directive": "No learning topics found. Ask user what they'd like to learn and initialize a new topic.",
                "suggested_response": "No learning topics found yet. What would you like to learn?"
            }
            print(json.dumps(output, indent=2))
        else:
            output = {
                "status": "success",
                "topic_count": len(topics),
                "topics": topics,
                "llm_directive": "Show user the list of topics. Ask which one they'd like to work on or if they want to start a new one.",
                "suggested_response": f"You have {len(topics)} learning topic(s):\n\n" + "\n".join([
                    f"{'✅' if t['status'] == 'completed' else '📖'} {t['topic']} - {t['sessions']} sessions"
                    for t in topics
                ]) + "\n\nWhich topic would you like to work on?"
            }
            print(json.dumps(output, indent=2))

    elif command == "info" and len(sys.argv) >= 3:
        info = get_topic_info(sys.argv[2])
        if info:
            output = {
                "status": "success",
                "topic_info": info,
                "llm_directive": "Display topic information to user. Check if reviews are due for this topic.",
                "suggested_response": f"Topic: {info['topic']}\nSessions: {info['sessions']}\nStatus: {info['status']}"
            }
            print(json.dumps(output, indent=2))
        else:
            output = {
                "status": "error",
                "error": f"Topic '{sys.argv[2]}' not found",
                "llm_directive": "Inform user topic not found. Suggest listing all topics or creating new one."
            }
            print(json.dumps(output, indent=2))
