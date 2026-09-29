#!/usr/bin/env python3
"""Synthetic integration example for the public NEXUS Evidence Preflight Actor.

Default mode only constructs and prints input matching the published Actor schema.
It does not access the network or run the Actor. Submitting can incur Apify PPE
charges and is deliberately gated behind --submit and --confirm-costs.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import uuid
from typing import Any


ACTOR_ID = "vad_tot_i86/nexus-v06-private-cloud-test"

# Synthetic example of text already extracted from a public page. This script
# does not fetch a webpage or perform OCR. Replace this only with authorized,
# public, non-sensitive text in an actual integration.
EXTRACTED_PAGE_TEXT = (
    "Unit price: $100. Total price: $500. Quantity 5."
)

# These represent structured claims produced by an upstream extraction step.
# Evidence is copied verbatim from the supplied page text.
EXTRACTED_CLAIMS = [
    {
        "claim_id": "price-1",
        "field": "unit_price",
        "semantic_field": "unit_price",
        "page": 1,
        "evidence": "Unit price: $100",
        "value": "$100",
    },
    {
        "claim_id": "total-1",
        "field": "total_price",
        "semantic_field": "total_price",
        "page": 1,
        "evidence": "Total price: $500",
        "value": "$500",
    },
]


def build_input() -> dict[str, Any]:
    """Build the exact top-level structure required by the published schema."""
    return {
        "request_id": str(uuid.uuid4()),
        # This is the caller's confirmation, not a NEXUS privacy scan.
        "public_non_sensitive_confirmed": True,
        "source": {
            "document_id": "synthetic-public-price-page-demo",
            # Caller declaration only; NEXUS does not check the URL or source.
            "provenance": "public_source",
        },
        "pages": [{"page": 1, "text": EXTRACTED_PAGE_TEXT}],
        "claims": EXTRACTED_CLAIMS,
    }


def submit(input_data: dict[str, Any]) -> dict[str, Any]:
    """Call the published Actor. This is billable and is never called by default."""
    token = os.environ.get("APIFY_TOKEN")
    if not token:
        raise RuntimeError("Set APIFY_TOKEN in your environment; never put it in code.")

    from apify_client import ApifyClient

    client = ApifyClient(token)
    run = client.actor(ACTOR_ID).call(run_input=input_data)
    if not run or not run.get("defaultDatasetId"):
        raise RuntimeError("Run returned no default dataset; inspect the run in Apify.")
    items = client.dataset(run["defaultDatasetId"]).list_items().items
    return {"run_status": run.get("status"), "items": items}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--submit",
        action="store_true",
        help="Submit to Apify (billable); omitted by default.",
    )
    parser.add_argument(
        "--confirm-costs",
        action="store_true",
        help="Required together with --submit to acknowledge Apify PPE charges.",
    )
    args = parser.parse_args()
    input_data = build_input()

    if not args.submit:
        print(json.dumps(input_data, indent=2))
        print("Dry run only: no Actor call was made.", file=sys.stderr)
        return 0

    if not args.confirm_costs:
        parser.error("--submit is billable; add --confirm-costs only after owner approval.")

    result = submit(input_data)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
