# Terret Agentic Content Workflow

Prototype for the Terret Agentic Workflow Intern take-home project.

I built this as a small local version of the content workflow Terret described: take public posts from Justin Shriber, turn them into a Terret-style blog draft, make a human reviewer approve or reject it, and only then allow it to publish.

I kept the system file-based on purpose. Instead of spending most of the time wiring up external services, I wanted to show the core workflow clearly: source data comes in, the system creates an idea brief and draft, a reviewer checks the draft in a Streamlit app, the review decision is saved as JSON, and the publish script checks that decision before writing the final post.

## What It Does

The local workflow is:

```text
source posts
→ idea brief
→ blog draft
→ review packet
→ human review app
→ review decision JSON
→ approval-gated publish script
→ static-site-style Markdown output
```

The current live example is a blog post titled:

```text
Why CROs Need More Than an LLM on Top of Their Revenue Data
```

This project does not call a live LLM API, send real Slack/email notifications, authenticate reviewers, or publish to a real CMS yet. The goal here was to show the workflow shape, the handoff between artifacts, and the human approval gate.

## How to Run It

From the repo root, generate the idea brief, draft, and review packet:

```powershell
python src/run_workflow.py
```

This writes:

```text
outputs/idea_briefs/idea_brief_001.json
outputs/idea_briefs/idea_brief_001.md
outputs/drafts/blog_draft_001.md
outputs/review_packets/review_packet_001.md
```

Then open the review app:

```powershell
python -m streamlit run src/review_app.py
```

In the app, review the draft, open the careful-claims checklist, choose approve, request edits, or reject, and save the decision.

The app writes:

```text
outputs/review_decisions/review_decision_001.json
```

The demo decision currently looks like:

```json
{
  "decision": "approved",
  "publish_allowed": true,
  "reviewer": "Demo Marketing Reviewer"
}
```

Then publish the approved post:

```powershell
python src/publish.py
```

If approval is missing, rejected, or marked request-edits, the script blocks publishing. If approval is valid, it writes:

```text
outputs/published/blog_post_001.md
site/posts/why-cros-need-more-than-an-llm-on-revenue-data.md
```

To check that internal review notes were removed from the public post:

```powershell
Select-String -Path site\posts\why-cros-need-more-than-an-llm-on-revenue-data.md -Pattern "Review Notes"
```

A clean result prints nothing.

## Source Data and Context

Source posts are stored in:

```text
data/source_posts.json
```

The source file contains four public LinkedIn posts from Justin Shriber. I picked posts that all center on the same problem: revenue teams have plenty of tools and data, but still struggle to answer practical CRO questions like why forecast changed, why deals are slipping, or what the team should do next.

I added the posts manually instead of scraping LinkedIn. That was a deliberate shortcut. For this project, the interesting part was not building a LinkedIn scraper. It was showing what happens after the source signal is captured: how it becomes an idea brief, how that turns into a draft, how a reviewer checks it, and how publishing stays blocked until approval.

Terret product and brand context is stored in:

```text
data/terret_context.md
```

That file gives the workflow shared context on Terret positioning, audience, editorial voice, product language, Revenue Graph concepts, content standards, and evidence boundaries.

## Prompt Files

Prompt blueprints are stored in:

```text
prompts/idea_brief_prompt.md
prompts/blog_generation_prompt.md
prompts/quality_check_prompt.md
```

The current workflow uses deterministic Python logic so the pipeline is stable and easy to inspect. The prompt files show where a live Gemini or OpenAI call would fit later.

## Human Review Gate

The review app is the human-facing control layer. The publish script is the enforcement layer.

A draft existing on disk is not enough to publish. `src/publish.py` reads the saved review decision first. It only publishes when the decision is approved and `publish_allowed` is true.

Before writing the public post, the script also validates the draft metadata and removes the internal review notes from the body.

## Current Artifacts

The main generated files are:

```text
outputs/idea_briefs/idea_brief_001.json
outputs/idea_briefs/idea_brief_001.md
outputs/drafts/blog_draft_001.md
outputs/review_packets/review_packet_001.md
outputs/review_decisions/review_decision_001.json
outputs/published/blog_post_001.md
site/posts/why-cros-need-more-than-an-llm-on-revenue-data.md
```

The core argument of the example post is that CROs do not need another interface for incomplete revenue data. They need a governed system that connects the full revenue picture, produces reliable root-cause analysis, and turns answers into operational action.

## Design Choices

I kept the project narrow on purpose.

The LinkedIn posts are manual inputs because scraping was not the point of the assignment. The intermediate files are visible because I wanted each stage to be inspectable. JSON is used when the next step needs structured state. Markdown is used when a person needs to read or review the output.

The generation step is deterministic for now. That made it easier to prove the workflow before adding model variability. A live LLM call could be added later behind the existing prompt files.

The main guardrail is the publish step. `src/publish.py` does not publish just because a draft exists. It checks the review decision, validates the draft metadata, removes review-only content, and then writes the public Markdown file.

## What Still Breaks

This is still a local prototype. It does not call a live LLM API, send a real Slack or email notification, authenticate reviewers, connect to a real CMS, or handle multiple content batches.

Review state is stored in a JSON file, so rerunning the review app can overwrite the previous decision. Source posts are added by hand. The SEO/AEO/GEO fields are formatted but not checked against an external SEO tool. The final output is Markdown in `site/posts/`, not a deployed website.

The biggest content risk is still claims review. The draft is based on public founder posts and Terret positioning notes, but any real external publication would still need a human to check product language, evidence boundaries, and whether any claims should be softened.

## Future Improvements

The next thing I would add is a lightweight notification artifact when a draft is ready for review, probably `outputs/notifications/notification_001.md`. That would model the “marketing colleague gets notified” step without spending time on Slack setup.

After that, I would add a quality-check stage before human review, tests for blocked publishing, support for multiple batches, reviewer authentication, a real Slack/email integration, and eventually a CMS or deployed static-site target.

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
    review_decisions/
    published/
  site/
    posts/
  README.md
  requirements.txt
```
