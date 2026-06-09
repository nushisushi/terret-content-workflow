from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

SOURCE_POSTS_PATH = ROOT / "data" / "source_posts.json"
TERRET_CONTEXT_PATH = ROOT / "data" / "terret_context.md"
IDEA_BRIEF_PROMPT_PATH = ROOT / "prompts" / "idea_brief_prompt.md"
BLOG_GENERATION_PROMPT_PATH = ROOT / "prompts" / "blog_generation_prompt.md"

IDEA_BRIEF_DIR = ROOT / "outputs" / "idea_briefs"
DRAFT_DIR = ROOT / "outputs" / "drafts"
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
    blog_draft_path: Path,
) -> str:
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    review_notes = "\n".join(f"- {note}" for note in brief["human_review_notes"])

    return f"""# Review Packet: Draft Ready

Generated at: {generated_at}

## Status

Ready for human marketing review.

## Working Title

{brief["working_title"]}

## Source Posts Used

{", ".join(brief["source_post_ids"])}

## What the Reviewer Should Decide

- Approve this draft for publishing
- Request edits to the angle, title, structure, claims, or product language
- Reject the draft if it is too close to source-post copy or not useful enough for Terret's audience

## Files Generated

- Markdown idea brief: `{idea_brief_md_path.relative_to(ROOT)}`
- JSON idea brief: `{idea_brief_json_path.relative_to(ROOT)}`
- Blog draft: `{blog_draft_path.relative_to(ROOT)}`

## Human Review Checklist

{review_notes}

## Important Gate

This packet does not publish anything. The blog draft remains blocked until a human reviewer approves it.
"""


def yaml_list(items: list[str]) -> str:
    return "\n".join(f"  - {item}" for item in items)


def render_blog_draft(brief: dict[str, Any]) -> str:
    title = brief["working_title"]
    slug = brief["seo_aeo_geo_notes"]["suggested_slug"]
    meta_description = brief["seo_aeo_geo_notes"]["suggested_meta_description"]
    source_post_ids = brief["source_post_ids"]

    tags = [
        "AI revenue intelligence",
        "Revenue Graph",
        "RevOps",
        "CRO",
        "answer-to-action",
    ]

    return f"""---
title: "{title}"
slug: "{slug}"
meta_description: "{meta_description}"
author: "Terret"
status: "draft"
tags:
{yaml_list(tags)}
source_post_ids:
{yaml_list(source_post_ids)}
---

# {title}

CROs have more revenue data than ever. They have dashboards, analytics platforms, call transcripts, CRM fields, pipeline reports, data warehouse tables, and now a growing stack of AI tools layered on top.

Yet the most important questions are often still the hardest to answer.

What is driving the drop in forecast? Why are top performers converting deals that others cannot? Why are competitive losses increasing in one segment but not another? Which deals need immediate action?

The problem is not that revenue teams lack data. The problem is that the data does not add up to a complete revenue picture.

## The Obvious Move Is to Put an LLM on Top

It is easy to understand why teams want to point an LLM at their revenue systems. The promise sounds simple: connect the systems, ask a natural-language question, and get the answer without waiting on manual analysis.

For revenue leaders, that sounds like a way out of the reporting queue. Instead of asking RevOps to pull together another one-off analysis, a CRO could ask directly what changed, where the risk is, and what to do next.

But for enterprise revenue work, the obvious solution creates new problems if it is not grounded in the right data architecture.

Revenue systems have different permissions, definitions, and business logic. A forecast number is not just a number. It depends on stage definitions, close-date behavior, commit rules, segment rules, rep judgment, historical conversion, and inspection context. If an AI system does not understand those definitions, the answer can look confident while being operationally wrong.

## The Real Problem Is Fragmented Revenue Reality

Most revenue organizations are not struggling because they have too little data. They are struggling because the useful data is scattered.

CRM data sits in one place. Call transcripts sit somewhere else. Email threads, ERP data, product usage signals, customer expansion indicators, and warehouse data all live in separate systems. Each system holds part of the story, but none of them carries the full revenue context on its own.

That fragmentation changes what AI can answer.

If a tool can only see the CRM, it can only answer CRM-shaped questions. If it can only see call transcripts, it can only answer conversation-shaped questions. If it cannot connect activity, deal progression, competitive pressure, product usage, and rep behavior, it cannot explain root cause with enough confidence for a CRO to act.

That is why a better interface is not enough. The interface can only be as useful as the revenue reality underneath it.

## Answers Are Not the Same as Outcomes

Even when teams manage to produce an answer, the workflow often stops too soon.

A human operator might manually pull the data together, create the analysis, and send around a summary. That can work once, but it does not scale across every forecast call, segment review, competitor threat, and pipeline inspection.

A revenue data lake can centralize more information, but it can also become expensive, slow to modify, and disconnected from the daily operating rhythm of the revenue team. Even when the analysis is useful, someone still has to turn that answer into action.

That is the difference between insight and execution.

A CRO does not only need to know that forecast risk increased in the Enterprise segment. They need to know which deals changed, why they changed, which reps need support, what playbook should run, who should be alerted, and what should happen next.

## What an Answer-to-Action Revenue Workflow Requires

A useful revenue AI system needs more than access to scattered data. It needs a governed foundation that connects the full revenue picture and keeps business context intact.

That is the role of Terret Nexus.

Nexus is positioned as an answer-to-action revenue engine for teams that need root-cause analysis and operational follow-through. The foundation is the Revenue Graph: a connected view of revenue data across systems, designed to preserve context, governance, and workflow relevance.

The important shift is not just from dashboard to chatbot. It is from partial answers to operational action.

In practice, that means the system should help revenue teams move from a question like “Why did forecast move?” to the underlying drivers, the affected deals, the relevant team behaviors, and the next steps required to respond.

## Why This Matters for CROs and RevOps Leaders

CROs are not looking for more AI theater. They are looking for a faster path from business question to operational response.

That requires three things.

First, the data foundation has to be connected enough to represent the actual revenue motion.

Second, the analysis has to respect governance, access controls, definitions, and business context.

Third, the output has to move toward action. A useful system should support alerts, playbooks, coaching, workflow updates, and execution steps, not just a polished paragraph explaining what happened.

## Takeaway for Revenue Leaders

Do not evaluate revenue AI only by the quality of the interface. A clean chat experience can still produce shallow answers if the system underneath it cannot see the full picture.

The better question is whether the system can connect revenue data, explain root cause, and help the team act.

For CROs and RevOps leaders, that is the real dividing line. The next generation of revenue intelligence will not be defined by who can generate the most fluent answer. It will be defined by who can turn the right answer into the next right action.

## Review Notes

- Review product wording around Terret Nexus and the Revenue Graph before publication.
- The source posts include strong claims about MCP integrations, LLM accuracy, and enterprise scale. This draft softens those claims into risks of poorly governed or incomplete implementations.
- The source posts include anecdotal claims about revenue data lake cost and implementation burden. This draft avoids repeating specific dollar amounts.
- The draft treats Terret positioning as brand framing, not independently verified proof.
- The draft should be checked for similarity to Justin Shriber's LinkedIn posts before approval.
- Recommended reviewer decision: approve with light edits if product language matches approved Terret positioning.
"""


def main() -> None:
    IDEA_BRIEF_DIR.mkdir(parents=True, exist_ok=True)
    DRAFT_DIR.mkdir(parents=True, exist_ok=True)
    REVIEW_PACKET_DIR.mkdir(parents=True, exist_ok=True)

    posts = load_source_posts(SOURCE_POSTS_PATH)
    terret_context = read_text(TERRET_CONTEXT_PATH)
    idea_brief_prompt = read_text(IDEA_BRIEF_PROMPT_PATH)
    blog_generation_prompt = read_text(BLOG_GENERATION_PROMPT_PATH)

    if not terret_context.strip():
        raise ValueError("terret_context.md is empty.")

    if not idea_brief_prompt.strip():
        raise ValueError("idea_brief_prompt.md is empty.")

    if not blog_generation_prompt.strip():
        raise ValueError("blog_generation_prompt.md is empty.")

    brief = build_idea_brief(posts)

    idea_brief_json_path = IDEA_BRIEF_DIR / "idea_brief_001.json"
    idea_brief_md_path = IDEA_BRIEF_DIR / "idea_brief_001.md"
    blog_draft_path = DRAFT_DIR / "blog_draft_001.md"
    review_packet_path = REVIEW_PACKET_DIR / "review_packet_001.md"

    idea_brief_json_path.write_text(
        json.dumps(brief, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    idea_brief_md_path.write_text(
        render_idea_brief_markdown(brief),
        encoding="utf-8",
    )
    blog_draft_path.write_text(
        render_blog_draft(brief),
        encoding="utf-8",
    )
    review_packet_path.write_text(
        render_review_packet(
            brief,
            idea_brief_md_path,
            idea_brief_json_path,
            blog_draft_path,
        ),
        encoding="utf-8",
    )

    print("Stage 1 complete: idea brief generated.")
    print(f"- {idea_brief_json_path.relative_to(ROOT)}")
    print(f"- {idea_brief_md_path.relative_to(ROOT)}")
    print()
    print("Stage 2 complete: blog draft generated.")
    print(f"- {blog_draft_path.relative_to(ROOT)}")
    print()
    print("Review packet updated.")
    print(f"- {review_packet_path.relative_to(ROOT)}")
    print()
    print("Next gate: human review before publishing.")

if __name__ == "__main__":
    main()