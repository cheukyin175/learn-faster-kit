#!/usr/bin/env python3
"""
Initialize a new learning topic with structured syllabus and tracking files.
On first initialization, copies scripts and CLAUDE.md to .learning/ directory.
"""

import os
import json
import shutil
from datetime import datetime
from pathlib import Path


def init_learning_topic(topic_name: str, base_dir: str = ".learning"):
    """
    Initialize a new learning topic with directory structure and tracking files.

    Args:
        topic_name: Name of the topic to learn
        base_dir: Base directory for learning data (default: .learning)
    """
    # Create base directory if it doesn't exist
    learning_dir = Path(base_dir)
    learning_dir.mkdir(exist_ok=True)

    # Create topic-specific directory
    topic_slug = topic_name.lower().replace(" ", "-")
    topic_dir = learning_dir / topic_slug

    if topic_dir.exists():
        print(f"⚠️  Topic '{topic_name}' already exists at {topic_dir}")
        return str(topic_dir)

    topic_dir.mkdir(parents=True, exist_ok=True)

    # Create topic metadata
    metadata = {
        "topic": topic_name,
        "created_at": datetime.now().isoformat(),
        "status": "in_progress",
        "syllabus_generated": False,
        "total_sessions": 0,
        "last_reviewed": None
    }

    with open(topic_dir / "metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)

    # Create syllabus template
    with open(topic_dir / "syllabus.md", "w") as f:
        f.write(f"# {topic_name} - Learning Syllabus\n\n")
        f.write("## Overview\n\n")
        f.write("<!-- 2-3 sentences: what you'll learn and why it matters -->\n\n")
        f.write("## Prerequisites\n\n")
        f.write("- Prerequisite 1\n")
        f.write("- Prerequisite 2\n\n")
        f.write("## Learning Objectives\n\n")
        f.write("By the end, you will:\n")
        f.write("1. Objective 1\n")
        f.write("2. Objective 2\n\n")
        f.write("## Learning Path\n\n")
        f.write("### Phase 1: Foundations\n\n")
        f.write("- [ ] Concept 1.1 - Description\n")
        f.write("- [ ] Concept 1.2 - Description\n")
        f.write("- [ ] 🔨 Project: [Hands-on project name]\n\n")
        f.write("### Phase 2: Intermediate\n\n")
        f.write("- [ ] Concept 2.1 - Description\n")
        f.write("- [ ] 🔨 Project: [Intermediate project]\n\n")
        f.write("### Phase 3: Advanced\n\n")
        f.write("- [ ] Concept 3.1 - Description\n")
        f.write("- [ ] 🔨 Project: [Comprehensive project]\n\n")
        f.write("## Teaching Milestones\n\n")
        f.write("- After Phase 1: Explain [concept]\n")
        f.write("- After Phase 2: Teach [concept] to someone\n\n")
        f.write("## Resources\n\n")
        f.write("- [Link 1]\n")
        f.write("- [Link 2]\n\n")
        f.write("## Success Criteria\n\n")
        f.write("- [ ] Can explain core concepts without reference\n")
        f.write("- [ ] Completed all 🔨 projects\n")
        f.write("- [ ] Taught key concepts to someone else\n")

    # Create progress log
    with open(topic_dir / "progress.md", "w") as f:
        f.write(f"# {topic_name} - Learning Progress\n\n")
        f.write("## Daily Logs\n\n")
        f.write("<!-- Daily learning entries will be added here -->\n")

    # Create review schedule
    with open(topic_dir / "review_schedule.json", "w") as f:
        json.dump({"reviews": []}, f, indent=2)

    # Create mastery checklist
    with open(topic_dir / "mastery.md", "w") as f:
        f.write(f"# {topic_name} - Mastery Checklist\n\n")
        f.write("## Core Concepts\n\n")
        f.write("Track your understanding of key concepts:\n\n")
        f.write("- [ ] Concept 1 - Not started\n")
        f.write("- [ ] Concept 2 - Not started\n")

    # Output structured JSON for LLM parsing
    output = {
        "status": "success",
        "topic_name": topic_name,
        "topic_slug": topic_slug,
        "directory": str(topic_dir),
        "files_created": [
            "metadata.json",
            "syllabus.md",
            "progress.md",
            "review_schedule.json",
            "mastery.md"
        ],
        "next_action": "generate_syllabus",
        "llm_directive": f"Immediately generate a comprehensive syllabus for '{topic_name}'. Write content to {topic_dir}/syllabus.md. Include: Overview, Prerequisites, Learning Objectives, 3-4 Phases with hands-on projects (🔨), Teaching Milestones, Resources, and Success Criteria. After writing, inform user syllabus is ready and show first 2-3 learning items.",
        "suggested_response": f"✅ Created learning environment for {topic_name}!\n\nGenerating comprehensive syllabus now..."
    }

    print(json.dumps(output, indent=2))
    return str(topic_dir)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python3 init_learning.py <topic_name> [base_dir]")
        print("\nExample: python3 init_learning.py 'React Hooks' .learning")
        sys.exit(1)

    topic = sys.argv[1]
    base = sys.argv[2] if len(sys.argv) > 2 else ".learning"

    init_learning_topic(topic, base)
