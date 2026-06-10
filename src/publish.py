from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]

DRAFT_PATH = ROOT / "outputs" / "drafts" / "blog_draft_001.md"
REVIEW_DECISION_PATH = ROOT / "outputs" / "review_decisions" / "review_decision_001.json"

PUBLISHED_OUTPUT_DIR = ROOT / "outputs" / "published"
SITE_POSTS_DIR = ROOT / "site" / "posts"


def read_text(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Missing required file: {path}")
    return path.read_text(encoding="utf-8")


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(
            f"Missing review decision file: {path}. "
            "Publishing is blocked until a human review decision exists."
        )
    return json.loads(path.read_text(encoding="utf-8"))


def parse_frontmatter(markdown_text: str) -> tuple[dict[str, Any], str]:
    if not markdown_text.startswith("---"):
        raise ValueError("Draft is missing YAML frontmatter.")

    parts = markdown_text.split("---", 2)

    if len(parts) < 3:
        raise ValueError("Draft frontmatter is malformed.")

    frontmatter_text = parts[1].strip()
    body = parts[2].strip()

    frontmatter = yaml.safe_load(frontmatter_text) or {}

    if not isinstance(frontmatter, dict):
        raise ValueError("Draft frontmatter must parse to a dictionary.")

    return frontmatter, body


def require_approval(review_decision: dict[str, Any]) -> None:
    decision = review_decision.get("decision")
    publish_allowed = review_decision.get("publish_allowed")

    if decision != "approved" or publish_allowed is not True:
        raise PermissionError(
            "Publishing blocked. A human reviewer must approve the draft before publication."
        )


def validate_frontmatter(frontmatter: dict[str, Any]) -> None:
    required_fields = [
        "title",
        "slug",
        "meta_description",
        "author",
        "tags",
        "source_post_ids",
    ]

    missing_fields = [
        field for field in required_fields if not frontmatter.get(field)
    ]

    if missing_fields:
        raise ValueError(f"Draft frontmatter is missing fields: {missing_fields}")

    if not isinstance(frontmatter["tags"], list):
        raise ValueError("Draft frontmatter field 'tags' must be a list.")

    if not isinstance(frontmatter["source_post_ids"], list):
        raise ValueError("Draft frontmatter field 'source_post_ids' must be a list.")


def remove_internal_review_notes(body: str) -> str:
    marker = "\n## Review Notes\n"

    if marker not in body:
        return body.strip()

    public_body = body.split(marker, 1)[0]
    return public_body.strip()


def render_yaml_list(items: list[str]) -> str:
    return "\n".join(f"  - {item}" for item in items)


def render_published_post(
    frontmatter: dict[str, Any],
    public_body: str,
    review_decision: dict[str, Any],
) -> str:
    published_at = datetime.now(timezone.utc).isoformat()

    title = frontmatter["title"]
    slug = frontmatter["slug"]
    meta_description = frontmatter["meta_description"]
    author = frontmatter["author"]
    tags = frontmatter["tags"]
    source_post_ids = frontmatter["source_post_ids"]

    reviewer = review_decision.get("reviewer", "Unknown reviewer")
    reviewed_at_utc = review_decision.get("reviewed_at_utc", "Unknown review time")

    return f"""---
title: "{title}"
slug: "{slug}"
meta_description: "{meta_description}"
author: "{author}"
status: "published"
published_at_utc: "{published_at}"
reviewed_by: "{reviewer}"
reviewed_at_utc: "{reviewed_at_utc}"
tags:
{render_yaml_list(tags)}
source_post_ids:
{render_yaml_list(source_post_ids)}
---

{public_body}
"""


def publish_post() -> tuple[Path, Path]:
    draft_text = read_text(DRAFT_PATH)
    review_decision = read_json(REVIEW_DECISION_PATH)

    require_approval(review_decision)

    frontmatter, body = parse_frontmatter(draft_text)
    validate_frontmatter(frontmatter)

    public_body = remove_internal_review_notes(body)

    if "## Review Notes" in public_body:
        raise ValueError("Internal review notes were not removed from public body.")

    published_post = render_published_post(
        frontmatter=frontmatter,
        public_body=public_body,
        review_decision=review_decision,
    )

    slug = frontmatter["slug"]

    PUBLISHED_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    SITE_POSTS_DIR.mkdir(parents=True, exist_ok=True)

    published_output_path = PUBLISHED_OUTPUT_DIR / "blog_post_001.md"
    site_post_path = SITE_POSTS_DIR / f"{slug}.md"

    published_output_path.write_text(published_post, encoding="utf-8")
    site_post_path.write_text(published_post, encoding="utf-8")

    return published_output_path, site_post_path


def main() -> None:
    try:
        published_output_path, site_post_path = publish_post()
    except Exception as error:
        print("Publishing blocked.")
        print(f"Reason: {error}")
        raise SystemExit(1)

    print("Publishing complete.")
    print(f"- {published_output_path.relative_to(ROOT)}")
    print(f"- {site_post_path.relative_to(ROOT)}")
    print()
    print("Human approval was verified before publishing.")


if __name__ == "__main__":
    main()