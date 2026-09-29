# NEXUS Evidence Preflight

## AI-extracted claim and source quote verification

NEXUS is a deterministic lexical preflight for AI-extracted claims. It compares caller-supplied, pre-extracted English text with quoted passages, page anchors, claimed values, and controlled-field labels, then returns structured results for human review. It does not establish factual truth, document authenticity, source provenance, or general semantic entailment.

Use NEXUS when an AI agent needs to:

- Check whether an extracted price appears in its cited source text.
- Compare extracted values with supporting source quotes.
- Detect unsupported values before taking automated actions.
- Route uncertain or conflicting extracted claims for human review.

The Actor returns structured supported, rejected, or review results. Use them to flag items for a human reviewer before a downstream workflow proceeds—not to make the decision for that reviewer.

## Suitable uses

- Check page, quote, value, and controlled-field consistency in already extracted public text.
- Produce structured claim-level flags for a human review queue.
- Add a deterministic, limited preflight step before an agent proposes a consequential action.

## Do not use it for

- Establishing factual truth, general semantic entailment, legal validity, financial accuracy, or compliance.
- Verifying document authenticity, source identity, provenance, signatures, or whether a source is authoritative.
- OCR, PDF parsing, layout/table interpretation, document fetching, or extracting claims from documents.
- Private/confidential documents, personal data, credentials, secrets, or any content you are not authorized to process.
- Replacing professional judgment or human review in legal, financial, safety, identity, fraud, or other consequential decisions.

## Input

Submit JSON matching the Actor's Input schema. Required fields are `request_id` (canonical UUID), `public_non_sensitive_confirmed` (`true` is a caller declaration, not a privacy scanner), `source` (`document_id` and caller-declared `provenance`), `pages` (1–25 page objects with pre-extracted English `text`, 1–40,000 characters each), and `claims` (1–100 structured claims). Each claim contains `claim_id`, `field`, `semantic_field`, `page`, a short exact `evidence` quote (1–220 characters), and `value`. Extra properties are rejected. The complete constraints and controlled field requirements are in the Input schema.

The Actor does not fetch the document or verify the caller's source declaration. Keep submitted material public, non-sensitive, and authorized for processing. Runs execute on Apify infrastructure and are billed under the native PPE events described below. The current Store listing shows no separate platform-usage fee for this Actor; post-run dataset operations may still incur standard platform storage charges.

## Output and statuses

Successful reports are items in the default dataset (`reports`). A failed request writes a sanitized structured error to the default key-value store record `OUTPUT`; failed requests are not dataset report items. Inspect the Output and Dataset schemas for the exact machine-readable fields.

- `supported_by_schema_anchored_text`: a narrow quote/page/value and controlled-field match against supplied text only. **It does not mean the claim is true.**
- `review`: NEXUS abstained or detected uncertainty/contradiction, an unsupported field/anchor, incompatible units, ambiguous candidates, or unknown provenance. A human must review it.
- `rejected`: the supplied quote/page/value consistency check failed. This does not prove the underlying real-world claim is false.

Every successful result has `truth_verified: false`, `document_authenticity_verified: false`, `source_provenance_verified: false`, and `requires_human_review: true`. Output may include the caller's claim values and document identifier, but not the full supplied page text or evidence quote. A text hash is not an authenticity check.

## Synthetic example

For the synthetic input with page text `Unit price: $100. Total price: $500.`, a claim quoting `Unit price: $100` for controlled field `unit_price` and value `$100` can receive `supported_by_schema_anchored_text`. A claim associating the same quote with `total_price` should not be treated as supported. These are text-consistency examples only; neither result validates a real document or fact.

## Calling the Actor

The published Actor can be called by an authenticated Apify API client using its Store ID, then the run's default dataset can be read. This example loads the included synthetic sample input:

```python
import json

from apify_client import ApifyClient

client = ApifyClient("<APIFY_TOKEN>")
with open("examples/sample_input.json", encoding="utf-8") as f:
    run_input = json.load(f)
run = client.actor("vad_tot_i86/nexus-v06-private-cloud-test").call(
    run_input=run_input,
)
items = client.dataset(run["defaultDatasetId"]).list_items().items
```

Never put an API token in this README, input, source text, or a public repository. To let an MCP client discover Store Actors without granting run access, configure the official Apify MCP discovery tools:

```json
{
  "mcpServers": {
    "apify-discovery": {
      "url": "https://mcp.apify.com?tools=search-actors,fetch-actor-details"
    }
  }
}
```

An authenticated Apify MCP client can additionally use `call-actor`; read-only discovery uses `search-actors` and `fetch-actor-details`. Discovery does not imply autonomous-payment eligibility.

## Pricing and support

The public Store listing currently uses native Apify **Pay Per Event (PPE)** billing:

- **Result:** `$0.002` for each item saved to the default dataset (`apify-default-dataset-item`).
- **Actor Start:** `$0.00005` per event (`apify-actor-start`). The number of start events depends on allocated memory: one event per GB, with a minimum of one. At the current default of 1 GB, one start event is charged.

At the current default memory, a run that writes one report incurs `$0.00205` in listed PPE event charges. These are the rates returned for the FREE user tier on 2026-09-29; check the live Store price before quoting them because pricing may change.

The current public listing shows no separate platform-usage fee for this Actor; its run infrastructure is represented by the listed PPE pricing. Standard post-run dataset operations may still incur platform storage charges. The custom `context-check-report` charging path in this codebase is limited to Apify's local billing simulation and fails closed in hosted runs; it is not used for the public Actor's native PPE events.

For questions about this community-maintained Actor, contact **nexus.preflight@gmail.com**. NEXUS is an independent project and is not an Apify-maintained Actor or an endorsement by Apify.
