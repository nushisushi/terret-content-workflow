# Notification: Blog Draft Ready for Review

Generated at: 2026-06-10 16:56:14

Hi Marketing Reviewer,

A new Terret blog draft is ready for review.

## Draft

Title: Why CROs Need More Than an LLM on Top of Their Revenue Data

Source posts used: justin_post_001, justin_post_002, justin_post_003, justin_post_004

Draft file: `outputs/drafts/blog_draft_001.md`

Review packet: `outputs/review_packets/review_packet_001.md`

Quality check: `outputs/quality_checks/quality_check_001.md`

## Why You Are Being Notified

This draft has been generated, but it is not eligible for publishing yet. A human reviewer must approve, request edits, or reject it before the publish script can run successfully.

## Reviewer Checklist

- Check that the final angle is distinct from the LinkedIn posts and not a close paraphrase.
- Confirm that all product claims are supported by the Terret context file or public site language.
- Review whether any cost, scale, or competitive claims need softer phrasing.
- Confirm that the article speaks to CRO and RevOps pain rather than generic AI adoption.
- Confirm that the next stage should draft a blog post, not publish anything automatically.

## Suggested Next Action

Open the review app by running:

    python -m streamlit run src/review_app.py

Then review the draft and save one of these decisions:

- Approve for publishing
- Request edits
- Reject draft

## Publishing Gate

The publish script will remain blocked unless the saved review decision says `approved` and `publish_allowed` is `true`.
