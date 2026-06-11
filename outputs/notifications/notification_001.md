# Notification: Blog Draft Ready for Review

Generated at: 2026-06-11 16:21:10

Hi Marketing Reviewer,

A new Terret blog draft is ready for review.

## Draft

Title: Why CROs Need More Than an LLM on Top of Their Revenue Data

Source posts used: justin_post_001, justin_post_002, justin_post_003, justin_post_004, justin_post_005

Source post details are available in `data/source_posts.json`, including original LinkedIn URLs, capture method, and raw captured text.

Draft file: `outputs/drafts/blog_draft_001.md`

Review packet: `outputs/review_packets/review_packet_001.md`

Quality check: `outputs/quality_checks/quality_check_001.md`

Source evidence map: `outputs/source_maps/source_evidence_map_001.md`

## Reviewer Decision Card

**Recommended status:** Ready for human review

**Reason:** Draft is structurally ready, but product language, source similarity, and claim strength need human review.

**Required action:** Approve, request edits, or reject in the Streamlit review gate.

**Publishing status:** Blocked until explicit approval.

**Primary risks:**
- Product-claim precision
- Similarity to Justin Shriber source posts
- Whether AI Architect language should appear publicly

## Why You Are Being Notified

This draft has been generated, but it is not eligible for publishing yet. A human reviewer must approve, request edits, or reject it before the publish script can run successfully.

## Reviewer Checklist

- Check that the final angle is distinct from the LinkedIn posts and not a close paraphrase.
- Confirm that all product claims are supported by the Terret context file or public site language.
- Review whether any cost, scale, or competitive claims need softer phrasing.
- Confirm that the article speaks to CRO and RevOps pain rather than generic AI adoption.
- Check whether AI Architect terminology should appear in the public blog or stay as internal/source framing.
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
