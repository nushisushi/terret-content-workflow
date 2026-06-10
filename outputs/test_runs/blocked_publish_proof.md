# Blocked Publish Proof

This artifact shows that the workflow does not publish a draft unless a human reviewer approves it.

## Test Case

The publish script was tested against a non-approved review decision.

Example blocked decision:

```json
{
  "decision": "request_edits",
  "publish_allowed": false,
  "reviewer": "Demo Marketing Reviewer",
  "reviewed_at_utc": "2026-06-10T00:00:00+00:00",
  "review_notes": "Blocked-publish proof: reviewer requested edits."
}
```

## Expected Behavior

Publishing should be blocked.

The workflow should not write or update the public post unless the saved review decision is approved and `publish_allowed` is true.

## Actual Result

The blocked run output was saved here:

```text
outputs/test_runs/blocked_publish_output.txt
```

The publish script exited with code `1`, which confirms that the publish step failed closed instead of publishing without approval.

## Enforcement Layer

The approval gate is enforced in `src/publish.py`.

The script only publishes when:

```text
decision == "approved"
publish_allowed == true
```

Any rejected, request-edits, missing, or malformed decision blocks publication.

## Why This Matters

The project brief says that a human approval step before publishing is non-negotiable. This test proves that the workflow treats review state as a required publishing condition, not just a UI formality.

## Production Note

In a production version, this would become an automated unit test or CI check. For this prototype, it is documented as a manual proof artifact so the failure path is visible during review.
