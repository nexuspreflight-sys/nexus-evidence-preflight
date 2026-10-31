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

When the user explicitly requests NEXUS, use `fetch-actor-details` with the verified public identifier instead of relying on search ranking:

```json
{
  "actor": "vad_tot_i86/nexus-v06-private-cloud-test",
  "output": {
    "description": true,
    "pricing": true,
    "metadata": true,
    "inputSchema": true
  }
}
```

The stable Actor ID is `y8Ca9fCObq92TKZuz`. Inspect the returned identity, current pricing and schema before any separately authorized run. Detail lookup does not execute the Actor.

For open-ended tool discovery, use `search-actors` and evaluate the returned candidates. Do not assume that NEXUS appears in the results. On 2026-10-31, unauthenticated tests against the hosted Apify MCP server (version 0.20.0) did not return NEXUS among the first ten results for `NEXUS Evidence Preflight` or `claim quote checker`; direct `fetch-actor-details` succeeded. These are point-in-time observations, not a guaranteed ranking or a diagnosed search defect.

### Compatibility with the October 2026 Apify changes

- This repository uses ordinary Actor execution through the Apify API client. It does not use the removed `call-actor` `actor:tool` syntax or `output.mcpTools`. Do not replace its normal Actor calls with `call-actor-mcp-tool`, which is for tools hosted by MCP-server Actors.
- Apify announced Store API search changes on October 30, effective November 15, 2026. Code that searches `GET /v2/store` must not rely on paging search results, `sortBy`, or `total` meaning all matches. Search returns one page of at most 100 items. The MCP `search-actors` tool has its own smaller limit; use its advertised schema.
- This repository currently has no Store-search pagination code to migrate. When NEXUS is already the intended Actor, direct detail lookup avoids dependence on search ranking.
- Public Store metadata and MCP details reported `PAY_PER_EVENT` on October 31, 2026. Store metadata also reported `isWhiteListedForAgenticPayments: true`; no autonomous payment or paid run was tested. Recheck current eligibility before relying on it.

Official references: [MCP 0.20.0 release](https://github.com/apify/apify-mcp-server/releases/tag/v0.20.0), [Store API migration announcement](https://apify.com/change-log/apify-store-api), and [NEXUS Store listing](https://apify.com/vad_tot_i86/nexus-v06-private-cloud-test).

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
