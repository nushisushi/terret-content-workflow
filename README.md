# Terret Agentic Content Workflow

Prototype for the Terret Agentic Workflow Intern take-home project.

This project builds a small, end-to-end content workflow that turns public LinkedIn posts from Justin Shriber into structured Terret blog content with a human review gate before publishing.

The current implementation focuses on building a reliable vertical slice rather than a fragile full automation system. The workflow starts with curated public source posts, grounds generation in Terret product context, creates a structured idea brief, and prepares a review packet for a human marketing reviewer.

## Current Status

Implemented:

* Curated public LinkedIn source post dataset
* Terret product and brand context file
* Prompt blueprint for idea brief generation
* Prompt blueprint for blog draft generation
* Stage 1 workflow script
* Generated idea brief JSON artifact
* Generated idea brief Markdown artifact
* Generated human review packet

Not implemented yet:

* Blog draft generation
* Streamlit human approval dashboard
* Approval/rejection/edit state tracking
* Publish script
* Static site output
* Live LLM API integration

## Workflow Goal

The goal is to model an agentic marketing workflow from raw signal to publishable content:

1. Source: ingest public LinkedIn posts from Justin Shriber.
2. Synthesize: convert those posts into a structured idea brief.
3. Review: create a human-readable review packet before drafting.
4. Draft: generate a structured blog draft from an approved idea brief.
5. Approve: require a human approval gate before publishing.
6. Publish: only approved content should be eligible for CMS/static-site output.

This prototype currently implements steps 1 through 3.

## Why This Scope

I chose to build one clean vertical slice first instead of trying to wire together brittle integrations too early.

The current Stage 1 workflow proves:

* The source data can be read and validated.
* Terret brand/product context is separated from source data.
* The idea brief has a structured schema.
* The same structured data can be rendered into both JSON and Markdown.
* Human review is treated as a required gate, not an afterthought.

## Source Data

Source posts are stored in:

```text
data/source_posts.json
```

The current source batch includes four public LinkedIn posts from Justin Shriber focused on:

* Risks of generic LLM layers over enterprise revenue systems
* Fragmented revenue data
* CRO root-cause questions
* Human middleware and revenue data lake traps
* The shift from answers to action

The source posts are manually captured public posts. This avoids brittle LinkedIn scraping and keeps the prototype focused on workflow architecture, content quality, and human review.

## Brand Context

Terret product and brand grounding is stored in:

```text
data/terret_context.md
```

This file summarizes Terret positioning, audience, editorial voice, product language, Revenue Graph concepts, content guardrails, and evidence boundaries. It is intentionally curated rather than copied directly from the website.

## Stage 1: Idea Brief Generation

The Stage 1 script is:

```text
src/run_workflow.py
```

It reads:

```text
data/source_posts.json
data/terret_context.md
prompts/idea_brief_prompt.md
```

It writes:

```text
outputs/idea_briefs/idea_brief_001.json
outputs/idea_briefs/idea_brief_001.md
outputs/review_packets/review_packet_001.md
```

Run Stage 1 with:

```powershell
python src/run_workflow.py
```

Expected output:

```text
Stage 1 complete: idea brief generated.
- outputs\idea_briefs\idea_brief_001.json
- outputs\idea_briefs\idea_brief_001.md
- outputs\review_packets\review_packet_001.md

Next gate: human review before blog drafting.
```

## Testing

Validate the source JSON:

```powershell
python -m json.tool data/source_posts.json
```

Run the Stage 1 workflow:

```powershell
python src/run_workflow.py
```

Validate the generated idea brief JSON:

```powershell
python -m json.tool outputs/idea_briefs/idea_brief_001.json
```

Open generated artifacts:

```powershell
code outputs/idea_briefs/idea_brief_001.json
code outputs/idea_briefs/idea_brief_001.md
code outputs/review_packets/review_packet_001.md
```

## Current Generated Artifacts

The current generated idea brief is titled:

```text
Why CROs Need More Than an LLM on Top of Their Revenue Data
```

The brief identifies the core argument:

CROs do not need another interface that lets them ask questions of incomplete revenue data. They need a governed system that connects the full revenue picture, produces reliable root-cause analysis, and turns those answers into operational action.

## Human Review Design

The workflow creates a review packet before drafting. The review packet asks a marketing reviewer to decide whether to:

* Approve the idea direction for blog drafting
* Request edits to the angle, title, or outline
* Reject the idea if it is too close to source-post copy or not useful enough for Terret's audience

The workflow does not publish anything at this stage.

## Design Decisions

### Manual LinkedIn capture

I used manual capture of public LinkedIn posts rather than scraping or automating LinkedIn access. This keeps the prototype reliable and avoids spending time on brittle ingestion mechanics that are not central to the workflow design.

In production, this could be replaced with an approved social listening tool, a formal API, or a marketing-managed intake workflow.

### Structured intermediate artifacts

The idea brief is saved as both JSON and Markdown.

JSON supports downstream automation. Markdown supports human review.

### Human approval before publication

The system is designed around a required review gate. Public marketing content should not auto-publish without human approval.

### Deterministic Stage 1 first

The first implementation uses deterministic Python logic to prove the workflow contract and artifact handoff before adding a live LLM API dependency.

A later version can add Gemini/OpenAI generation as an optional mode once the pipeline shape is stable.

## What Breaks / Known Gaps

* The current system does not yet call a live LLM API.
* The idea brief content is currently generated by deterministic Python logic, not model inference.
* Source ingestion is manual.
* There is no deduplication across similar LinkedIn posts yet.
* There is no reviewer authentication.
* There is no persistent approval state yet.
* There is no CMS integration yet.
* Generated outputs are file-based rather than stored in a database.
* The workflow assumes one active content batch at a time.
* SEO/AEO/GEO fields are structured but not externally validated.
* Claims from source posts still need human review before publication.

## Next Steps

Planned next build steps:

1. Extend `src/run_workflow.py` to generate a structured blog draft from the idea brief.
2. Create `outputs/drafts/blog_draft_001.md`.
3. Build a Streamlit review dashboard for approve, reject, and request edits.
4. Save human review decisions as structured JSON.
5. Add a publish script that only publishes approved drafts.
6. Generate static Markdown/HTML output in `site/posts/`.

## Project Structure

```text
terret-content-workflow/
  data/
    source_posts.json
    terret_context.md
  prompts/
    idea_brief_prompt.md
    blog_generation_prompt.md
    quality_check_prompt.md
  src/
    run_workflow.py
    review_app.py
    publish.py
  outputs/
    idea_briefs/
    drafts/
    review_packets/
    published/
  site/
    posts/
  README.md
  requirements.txt
```
