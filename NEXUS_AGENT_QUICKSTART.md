# NEXUS Evidence Preflight — AI Agent Quickstart

Use this guide to add a narrow text-consistency preflight to an agent workflow. The Actor accepts **already-extracted English text** and claims from that same text. It does not fetch pages, perform OCR, establish factual truth, or verify document authenticity or source provenance.

## Discover NEXUS through read-only Apify MCP

The following server URL enables only Apify Store search and Actor-detail lookup. Apify documents these two tools as available without authentication. It does not expose Actor execution tools:

```json
{
  "mcpServers": {
    "apify-discovery": {
      "url": "https://mcp.apify.com?tools=search-actors,fetch-actor-details"
    }
  }
}
```

Search by task rather than assuming a result, then inspect the returned Actor details and schema. Example generic searches: `check extracted values against quoted text` or `document claim evidence consistency`. Discovery does not guarantee that NEXUS will appear, be suitable, or be eligible for autonomous payments.

## Integration sequence

1. Obtain public, authorized page text and extract candidate claims upstream. Do not send confidential documents, personal data, credentials, or material you are not authorized to process.
2. Build an input that matches the Actor's current Apify Input schema. The caller's `public_non_sensitive_confirmed: true` is an assertion, not a privacy scan.
3. Ask for owner/operator approval before any billable Actor run. The public Actor uses native Apify Pay Per Event; current listed event prices can change. Check the Store page immediately before calling.
4. Call `vad_tot_i86/nexus-v06-private-cloud-test` using the official Apify API client and read the run's default dataset.
5. Treat `supported_by_schema_anchored_text` only as a lexical/schema-anchor match against caller-supplied text. Route `review` and any consequential decision to a human. `rejected` means the supplied quote/page/value check failed, not that the real-world claim is false.

## Synthetic example

The included [`examples/agent_preflight_integration.py`](examples/agent_preflight_integration.py) builds a schema-shaped request and makes no network call by default:

```bash
python examples/agent_preflight_integration.py
```

The command prints a synthetic request and does not access the network. The script's explicit `--submit --confirm-costs` flags are required before it can call the Actor. That call may incur the current PPE charges; review the price and obtain cost approval first. Never put an Apify token in source code; provide it through a protected environment/secret manager.

## Important limits

- English pre-extracted text only; no webpage fetching, OCR, PDF parsing, table/layout interpretation, or claim extraction.
- NEXUS does not verify truth, authenticity, signatures, source identity, provenance, authority, or general semantic entailment.
- A positive-looking result may still be based on incorrect or forged input. Successful reports explicitly require human review.
- Do not use NEXUS as the sole basis for legal, financial, safety, identity, fraud, compliance, or other consequential decisions.
- The Actor and pricing are independent Apify Store offerings; MCP discovery does not imply free execution or agentic-payment eligibility.

## References

- [NEXUS Evidence Preflight on Apify Store](https://apify.com/vad_tot_i86/nexus-v06-private-cloud-test)
- [Apify MCP documentation](https://docs.apify.com/integrations/mcp)
- [Apify Pay Per Event documentation](https://docs.apify.com/actors/publishing/monetize/pay-per-event)
