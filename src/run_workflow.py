from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

SOURCE_POSTS_PATH = ROOT / "data" / "source_posts.json"
TERRET_CONTEXT_PATH = ROOT / "data" / "terret_context.md"
IDEA_BRIEF_PROMPT_PATH = ROOT / "prompts" / "idea_brief_prompt.md"

IDEA_BRIEF_DIR = ROOT / "outputs" / "idea_briefs"
REVIEW_PACKET_DIR = ROOT / "outputs" / "review_packets"


def read_text(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Missing required file: {path}")
    return path.read_text(encoding="utf-8")


def load_source_posts(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(f"Missing source posts file: {path}")

    with path.open("r", encoding="utf-8") as file:
        posts = json.load(file)

    if not isinstance(posts, list):
        raise ValueError("source_posts.json must contain a JSON array.")

    required_fields = {
        "id",
        "author",
        "title_hint",
        "platform",
        "post_url",
        "date_captured",
        "capture_method",
        "status",
        "raw_text",
    }

    for post in posts:
        missing = required_fields - set(post.keys())
        if missing:
            raise ValueError(
                f"Post {post.get('id', '<unknown>')} is missing fields: {missing}"
            )

    return posts


def build_idea_brief(posts: list[dict[str, Any]]) -> dict[str, Any]:
    source_post_ids = [post["id"] for post in posts]

    return {
        "working_title": "Why CROs Need More Than an LLM on Top of Their Revenue Data",
        "source_post_ids": source_post_ids,
        "source_signal_summary": [
            "Revenue leaders have invested in analytics platforms and AI, but still struggle to answer root-cause questions about forecast risk, deal loss, competitor pressure, and rep performance.",
            "The recurring blocker is not a lack of data. It is fragmented revenue data spread across CRM records, calls, emails, data warehouses, ERP systems, and product usage signals.",
            "Generic LLM layers can create enterprise risks around access controls, quantitative accuracy, and scale when they are not grounded in governed, connected business data.",
            "Manual human middleware and large revenue data lake projects may produce answers, but they still leave teams with the burden of translating those answers into action.",
            "The strongest Terret angle is the shift from isolated answers to an answer-to-action revenue workflow powered by a connected Revenue Graph.",
        ],
        "core_argument": (
            "CROs do not need another interface that lets them ask questions of incomplete revenue data. "
            "They need a governed system that connects the full revenue picture, produces reliable root-cause analysis, "
            "and turns those answers into operational action. The blog should argue that the failure mode of generic AI "
            "in revenue organizations is not the model alone. It is the missing data foundation, governance layer, and execution loop."
        ),
        "target_reader": {
            "primary_reader": "CROs, VPs of Sales, and Revenue Operations leaders at B2B companies with complex sales motions",
            "reader_pain": (
                "They are under pressure to explain forecast movement, deal loss, competitor risk, and rep performance, "
                "but their data is scattered across systems and their teams still rely on manual synthesis to get from question to action."
            ),
        },
        "terret_positioning_angle": (
            "Introduce Terret Nexus as an operator-built answer-to-action revenue engine. It should not be framed as just another dashboard, "
            "chatbot, or analytics layer. Position Nexus as the system that builds a governed Revenue Graph, analyzes the full revenue picture, "
            "and helps operationalize the answer through revenue workflows and agents."
        ),
        "suggested_outline": [
            {
                "heading": "CROs Have More Data Than Ever, But Still Cannot Get to Root Cause",
                "purpose": "Open with the familiar executive frustration.",
                "key_points": [
                    "Revenue teams have invested in analytics platforms and AI.",
                    "The hardest questions are still root-cause questions.",
                    "Examples: forecast drops, competitor losses, top-rep behavior, and deal risk.",
                ],
            },
            {
                "heading": "Why the Obvious LLM Layer Fails",
                "purpose": "Explain why simply placing an LLM over existing systems is not enough.",
                "key_points": [
                    "Revenue systems have different access controls and business logic.",
                    "Quantitative answers require consistent definitions and complete context.",
                    "Asking an LLM to reason across scattered systems creates scale and reliability problems.",
                ],
            },
            {
                "heading": "The Real Problem Is the Fragmented Revenue Picture",
                "purpose": "Move from AI hype to the deeper systems issue.",
                "key_points": [
                    "CRM, calls, emails, ERP, product usage, and warehouse data live in separate places.",
                    "A tool can only answer based on the data it can see.",
                    "Partial data creates partial answers, even when the interface looks intelligent.",
                ],
            },
            {
                "heading": "Human Middleware and Data Lakes Are Expensive Detours",
                "purpose": "Show why common workarounds still fail to produce operational outcomes.",
                "key_points": [
                    "Manual data assembly does not scale.",
                    "Large revenue data infrastructure can become slow and expensive.",
                    "Even when these approaches produce answers, teams still have to implement next steps manually.",
                ],
            },
            {
                "heading": "What Revenue Teams Actually Need: Answer to Action",
                "purpose": "Introduce the Terret Nexus approach without turning the post into a brochure.",
                "key_points": [
                    "A Revenue Graph connects the full revenue reality.",
                    "Governed context supports better analysis.",
                    "Agents and workflows help move from explanation to execution.",
                ],
            },
            {
                "heading": "The Takeaway for CROs",
                "purpose": "End with a practical executive takeaway.",
                "key_points": [
                    "Do not evaluate revenue AI only by the quality of its interface.",
                    "Evaluate whether it has the governed data foundation to answer accurately.",
                    "Evaluate whether it can turn answers into action inside the revenue workflow.",
                ],
            },
        ],
        "seo_aeo_geo_notes": {
            "primary_keyword": "AI revenue intelligence",
            "secondary_keywords": [
                "Revenue Graph",
                "revenue data fragmentation",
                "CRO forecast risk",
                "answer-to-action revenue engine",
                "RevOps AI workflow",
            ],
            "direct_answer_questions": [
                "Why do CROs still struggle to get answers from revenue data?",
                "Why is a generic LLM layer not enough for enterprise revenue intelligence?",
                "What is an answer-to-action revenue workflow?",
            ],
            "suggested_slug": "why-cros-need-more-than-an-llm-on-revenue-data",
            "suggested_meta_description": (
                "Why generic LLM layers fail CROs, and how governed revenue data turns answers into action."
            ),
        },
        "claims_to_handle_carefully": [
            "The source posts include strong claims about MCP integrations, LLM accuracy, and enterprise scale. The blog should frame these as risks of generic or poorly governed implementations, not as universal statements.",
            "The human middleware post includes specific cost and timeline claims about revenue data lakes. Use these as anecdotal context only or soften into broader language about expensive infrastructure projects.",
            "Terret positioning phrases such as 'answers the revenue questions no other AI can handle' should be treated as brand language, not independently verified proof.",
            "Avoid claiming Terret guarantees revenue outcomes unless supported by approved public proof points.",
        ],
        "human_review_notes": [
            "Check that the final angle is distinct from the LinkedIn posts and not a close paraphrase.",
            "Confirm that all product claims are supported by the Terret context file or public site language.",
            "Review whether any cost, scale, or competitive claims need softer phrasing.",
            "Confirm that the article speaks to CRO and RevOps pain rather than generic AI adoption.",
            "Confirm that the next stage should draft a blog post, not publish anything automatically.",
        ],
        "recommended_next_stage": "draft_blog",
    }


def render_idea_brief_markdown(brief: dict[str, Any]) -> str:
    outline_sections = []

    for section in brief["suggested_outline"]:
        key_points = "\n".join(f"  - {point}" for point in section["key_points"])
        outline_sections.append(
            f"### {section['heading']}\n"
            f"Purpose: {section['purpose']}\n\n"
            f"Key points:\n{key_points}"
        )

    source_summary = "\n".join(f"- {item}" for item in brief["source_signal_summary"])
    careful_claims = "\n".join(f"- {item}" for item in brief["claims_to_handle_carefully"])
    review_notes = "\n".join(f"- {item}" for item in brief["human_review_notes"])
    secondary_keywords = "\n".join(
        f"- {item}" for item in brief["seo_aeo_geo_notes"]["secondary_keywords"]
    )
    direct_questions = "\n".join(
        f"- {item}" for item in brief["seo_aeo_geo_notes"]["direct_answer_questions"]
    )

    return f"""# Idea Brief

## Working Title

{brief["working_title"]}

## Source Post IDs

{", ".join(brief["source_post_ids"])}

## Source Signal Summary

{source_summary}

## Core Argument

{brief["core_argument"]}

## Target Reader

Primary reader: {brief["target_reader"]["primary_reader"]}

Reader pain: {brief["target_reader"]["reader_pain"]}

## Terret Positioning Angle

{brief["terret_positioning_angle"]}

## Suggested Blog Structure

{chr(10).join(outline_sections)}

## SEO / AEO / GEO Notes

Primary keyword: {brief["seo_aeo_geo_notes"]["primary_keyword"]}

Secondary keywords:
{secondary_keywords}

Direct-answer questions:
{direct_questions}

Suggested slug: `{brief["seo_aeo_geo_notes"]["suggested_slug"]}`

Suggested meta description: {brief["seo_aeo_geo_notes"]["suggested_meta_description"]}

## Claims to Handle Carefully

{careful_claims}

## Human Review Notes

{review_notes}

## Recommended Next Stage

{brief["recommended_next_stage"]}
"""


def render_review_packet(
    brief: dict[str, Any],
    idea_brief_md_path: Path,
    idea_brief_json_path: Path,
) -> str:
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    review_notes = "\n".join(f"- {note}" for note in brief["human_review_notes"])

    return f"""# Review Packet: Idea Brief Ready

Generated at: {generated_at}

## Status

Ready for human marketing review.

## Working Title

{brief["working_title"]}

## Source Posts Used

{", ".join(brief["source_post_ids"])}

## What the Reviewer Should Decide

- Approve this idea direction for blog drafting
- Request edits to the angle, title, or outline
- Reject the idea if it is too close to source-post copy or not useful enough for Terret's audience

## Files Generated

- Markdown idea brief: `{idea_brief_md_path.relative_to(ROOT)}`
- JSON idea brief: `{idea_brief_json_path.relative_to(ROOT)}`

## Human Review Checklist

{review_notes}

## Important Gate

This packet does not publish anything. It only prepares the idea for human review before drafting.
"""


def main() -> None:
    IDEA_BRIEF_DIR.mkdir(parents=True, exist_ok=True)
    REVIEW_PACKET_DIR.mkdir(parents=True, exist_ok=True)

    posts = load_source_posts(SOURCE_POSTS_PATH)
    terret_context = read_text(TERRET_CONTEXT_PATH)
    idea_brief_prompt = read_text(IDEA_BRIEF_PROMPT_PATH)

    if not terret_context.strip():
        raise ValueError("terret_context.md is empty.")

    if not idea_brief_prompt.strip():
        raise ValueError("idea_brief_prompt.md is empty.")

    brief = build_idea_brief(posts)

    idea_brief_json_path = IDEA_BRIEF_DIR / "idea_brief_001.json"
    idea_brief_md_path = IDEA_BRIEF_DIR / "idea_brief_001.md"
    review_packet_path = REVIEW_PACKET_DIR / "review_packet_001.md"

    idea_brief_json_path.write_text(
        json.dumps(brief, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    idea_brief_md_path.write_text(
        render_idea_brief_markdown(brief),
        encoding="utf-8",
    )
    review_packet_path.write_text(
        render_review_packet(brief, idea_brief_md_path, idea_brief_json_path),
        encoding="utf-8",
    )

    print("Stage 1 complete: idea brief generated.")
    print(f"- {idea_brief_json_path.relative_to(ROOT)}")
    print(f"- {idea_brief_md_path.relative_to(ROOT)}")
    print(f"- {review_packet_path.relative_to(ROOT)}")
    print()
    print("Next gate: human review before blog drafting.")


if __name__ == "__main__":
    main()