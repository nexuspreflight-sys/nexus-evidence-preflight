# NEXUS Evidence Preflight — Technical Brief

**Public Actor:** [`vad_tot_i86/nexus-v06-private-cloud-test`](https://apify.com/vad_tot_i86/nexus-v06-private-cloud-test)  
**Purpose:** narrow, deterministic consistency checks over caller-supplied, already-extracted English text.  
**Not:** a fact checker, authenticity/provenance verifier, OCR/parser, or general semantic verifier.

## Agent workflow

1. Extract text and candidate claims in the agent's existing authorized workflow. NEXUS does not fetch the source or extract claims.
2. Discover/inspect public Actors using the read-only configuration in [`NEXUS_MCP_READONLY_CONFIG.json`](NEXUS_MCP_READONLY_CONFIG.json). This configuration exposes only `search-actors` and `fetch-actor-details`; it cannot run an Actor.
3. Validate the request against the live Apify Input schema linked from the Store Actor page. Required top-level fields include `request_id`, `public_non_sensitive_confirmed`, `source`, `pages`, and `claims`. The confirmation flag is only a caller declaration.
4. Obtain explicit cost approval, then call the Actor through Apify API or an authenticated official client. One Python example is in [`examples/agent_preflight_integration.py`](examples/agent_preflight_integration.py); its default is a local dry run and cloud submission requires both `--submit` and `--confirm-costs`.
5. Read result item(s) from the run's default dataset and preserve status/reason codes. Failed requests use the sanitized `OUTPUT` key-value-store record rather than a successful dataset report.
6. Require human review before consequential use.

The official Apify API runs an Actor with a `POST` to `https://api.apify.com/v2/actors/{actorId}/runs`; the run response provides the default dataset ID used to fetch results. See [Run Actor](https://docs.apify.com/api/v2/actors-runs-post) and [Apify's integration guide](https://docs.apify.com/integrations/actors/integrating-actors-via-api). Run calls are not part of this repository's validation and may incur charges.

## Input and result semantics

Each claim supplies its ID, field labels, page number, a short exact evidence quote, and extracted value. The current live schema is authoritative for precise types, limits, defaults, and controlled-field requirements; inspect it before integrating.

- `supported_by_schema_anchored_text`: the supplied quote/page/value and supported field association passed the narrow text checks. It does **not** assert that the source or claim is true.
- `review`: the checker abstained or found uncertainty, contradiction, unsupported field/anchor, incompatible units, ambiguous candidates, or untrusted/unknown provenance. Human review is required.
- `rejected`: supplied quote/page/value consistency did not pass. This does not establish that the real-world claim is false.

Successful output marks `truth_verified`, `document_authenticity_verified`, and `source_provenance_verified` false and `requires_human_review` true. It does not include the entire submitted page text or evidence quote, though it may include caller claim values and a document identifier. Do not submit private/confidential content, personal data, secrets, or documents lacking authorization.

## API usage example

The checked-in Python example uses `apify-client`, reads `APIFY_TOKEN` from the environment, and deliberately requires cost-confirmation flags for submission. Never commit a token. Equivalent SDK call shape:

```python
import os

from apify_client import ApifyClient

client = ApifyClient(token=os.environ["APIFY_TOKEN"])
run = client.actor("vad_tot_i86/nexus-v06-private-cloud-test").call(
    run_input=input_data,
)
dataset_id = run["defaultDatasetId"]
items = client.dataset(dataset_id).list_items().items
```

This code is illustrative and billable if executed. Confirm live pricing and obtain authorization first. The included example defaults to printing synthetic JSON and does not call the network.

## Current public PPE rates

Verified from the public Actor details through Apify MCP on **2026-09-29**:

- `result`: **$0.002 per event**, described as one result in the default dataset.
- `Actor Start`: **$0.00005 per event**. Apify reports that event count depends on Actor memory (one per GB, at least one event).

These rates can change. The actual event total depends on how many billable events the run produces and its allocated memory; check the live [pricing page](https://apify.com/vad_tot_i86/nexus-v06-private-cloud-test/pricing) before every paid use. Other account/platform charges may depend on current Apify terms and storage usage. No autonomous-payment eligibility is asserted here.

## Example validation and privacy

[`examples/sample_input.json`](examples/sample_input.json) contains synthetic values and is supplied only as an input-shape illustration. [`examples/agent_preflight_integration.py`](examples/agent_preflight_integration.py) defaults to local input generation. Do not replace sample data with confidential/private material in public issues, pull requests, or logs.
