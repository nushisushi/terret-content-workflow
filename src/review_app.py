from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import streamlit as st
import yaml


ROOT = Path(__file__).resolve().parents[1]

DRAFT_PATH = ROOT / "outputs" / "drafts" / "blog_draft_001.md"
IDEA_BRIEF_PATH = ROOT / "outputs" / "idea_briefs" / "idea_brief_001.json"
QUALITY_CHECK_PATH = ROOT / "outputs" / "quality_checks" / "quality_check_001.md"
REVIEW_DECISION_DIR = ROOT / "outputs" / "review_decisions"
REVIEW_DECISION_PATH = REVIEW_DECISION_DIR / "review_decision_001.json"


def rel_path(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_text(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Missing required file: {path}")
    return path.read_text(encoding="utf-8")


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Missing required file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def parse_frontmatter(markdown_text: str) -> tuple[dict[str, Any], str]:
    if not markdown_text.startswith("---"):
        return {}, markdown_text

    parts = markdown_text.split("---", 2)

    if len(parts) < 3:
        return {}, markdown_text

    frontmatter_text = parts[1].strip()
    body = parts[2].strip()

    try:
        frontmatter = yaml.safe_load(frontmatter_text) or {}
    except yaml.YAMLError:
        frontmatter = {}

    return frontmatter, body


def save_review_decision(
    decision: str,
    reviewer: str,
    comments: str,
    frontmatter: dict[str, Any],
) -> Path:
    REVIEW_DECISION_DIR.mkdir(parents=True, exist_ok=True)

    decision_payload = {
        "draft_id": "blog_draft_001",
        "draft_path": rel_path(DRAFT_PATH),
        "idea_brief_path": rel_path(IDEA_BRIEF_PATH),
        "quality_check_path": rel_path(QUALITY_CHECK_PATH),
        "title": frontmatter.get(
            "title",
            "Why CROs Need More Than an LLM on Top of Their Revenue Data",
        ),
        "slug": frontmatter.get(
            "slug",
            "why-cros-need-more-than-an-llm-on-revenue-data",
        ),
        "decision": decision,
        "publish_allowed": decision == "approved",
        "reviewer": reviewer,
        "comments": comments,
        "reviewed_at_utc": datetime.now(timezone.utc).isoformat(),
        "important_gate": (
            "Publishing is allowed only when decision is approved. "
            "Request-edits and rejected decisions must block publishing."
        ),
    }

    REVIEW_DECISION_PATH.write_text(
        json.dumps(decision_payload, indent=2),
        encoding="utf-8",
    )

    return REVIEW_DECISION_PATH


def main() -> None:
    st.set_page_config(
        page_title="Terret Content Review",
        page_icon="✅",
        layout="wide",
    )

    st.title("Terret Content Review Gate")
    st.caption("Human approval is required before any draft can be published.")

    try:
        draft_text = read_text(DRAFT_PATH)
        idea_brief = read_json(IDEA_BRIEF_PATH)
    except FileNotFoundError as error:
        st.error(str(error))
        st.stop()

    frontmatter, body = parse_frontmatter(draft_text)

    st.subheader("Draft Metadata")

    metadata_cols = st.columns(3)
    metadata_cols[0].metric("Status", frontmatter.get("status", "unknown"))
    metadata_cols[1].metric("Author", frontmatter.get("author", "unknown"))
    metadata_cols[2].metric(
        "Source Posts",
        len(frontmatter.get("source_post_ids", [])),
    )

    st.write(f"**Title:** {frontmatter.get('title', 'Unknown title')}")
    st.write(f"**Slug:** `{frontmatter.get('slug', 'unknown-slug')}`")
    st.write(
        f"**Meta description:** {frontmatter.get('meta_description', 'Missing')}"
    )

    with st.expander("Idea brief summary and careful-claims checklist", expanded=False):
        st.write(f"**Core argument:** {idea_brief.get('core_argument', 'Missing')}")

        st.write("**Claims to handle carefully:**")
        for claim in idea_brief.get("claims_to_handle_carefully", []):
            st.write(f"- {claim}")

        st.write("**Human review notes:**")
        for note in idea_brief.get("human_review_notes", []):
            st.write(f"- {note}")

    if QUALITY_CHECK_PATH.exists():
        with st.expander("Automated quality check", expanded=False):
            st.markdown(read_text(QUALITY_CHECK_PATH))
    else:
        st.info(
            "No quality check file found yet. Run `python src/run_workflow.py` "
            "to generate one before review."
        )

    st.subheader("Draft Preview")
    st.caption(
        "Internal review notes are visible to the reviewer here, but "
        "`src/publish.py` strips them before writing the public post."
    )

    preview_tab, raw_tab = st.tabs(["Rendered preview", "Raw Markdown"])

    with preview_tab:
        st.markdown(body)

    with raw_tab:
        st.code(draft_text, language="markdown")

    st.subheader("Human Review Decision")

    reviewer = st.text_input("Reviewer name", value="Demo Marketing Reviewer")

    decision = st.radio(
        "Decision",
        options=["approved", "request_edits", "rejected"],
        format_func={
            "approved": "Approve for publishing",
            "request_edits": "Request edits",
            "rejected": "Reject draft",
        }.get,
    )

    comments = st.text_area(
        "Reviewer comments",
        value=(
            "Approved for demo publish. Product wording, Terret Nexus positioning, "
            "and careful-claims notes should still be reviewed before any real "
            "external publication."
        ),
        height=140,
    )

    if st.button("Save review decision"):
        decision_path = save_review_decision(
            decision=decision,
            reviewer=reviewer,
            comments=comments,
            frontmatter=frontmatter,
        )

        relative_path = rel_path(decision_path)

        if decision == "approved":
            st.success(f"Approved. Review decision saved to {relative_path}.")
            st.info("Publishing is now allowed for the next stage.")
        elif decision == "request_edits":
            st.warning(f"Edits requested. Review decision saved to {relative_path}.")
            st.info("Publishing must remain blocked.")
        else:
            st.error(f"Rejected. Review decision saved to {relative_path}.")
            st.info("Publishing must remain blocked.")


if __name__ == "__main__":
    main()