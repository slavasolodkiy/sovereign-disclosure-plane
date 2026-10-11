# Sovereign Disclosure Plane — Live Case 03 reference model

> **The domain may be real while the authority is not. Channel-only never releases.**

**Status: tested reference model, not a deployment claim.**

- [Canonical incident page](https://www.solodkiy.cv/revolut-incident.html)
- [Full research trail — Sovereign Agent Lab](https://www.solodkiy.cv/sovereign-agent-lab.html)

This repository turns the five authority gates into an executable disclosure rule:

```text
CHANNEL → PRINCIPAL → CAPACITY → MANDATE → SCOPE → REQUIRED APPROVALS
```

The invariant is strict: **zero outbound PII until every gate is green.** Disclosure is irreversible; there is no provisional release and no “minimum dataset” escape hatch. `ai_override = false` always.

## Run

```bash
python3 -m unittest discover -s tests -v
python3 run.py examples/release.json
python3 run.py examples/hold-missing-approval.json
```

## What is implemented now

- HOLD when principal, capacity, mandate, scope or required approvals are incomplete.
- REJECT on attempted AI override.
- RELEASE only as a scoped packet after every gate passes.
- Full SHA-256 chained receipts for every decision.
- Tamper detection and deterministic test clock.
- Synthetic examples only.

## What is deliberately postponed

- Cryptographic credentials and key management.
- Real institutional directories and out-of-band verification.
- Legal interpretation of mandate, jurisdiction and time range.
- Production review UI, audit export and operational integrations.
- Any affiliation with or endorsement by Revolut.

This is the smallest executable answer that preserves the central claim today. Later versions can replace booleans and strings with verifiable credentials, policy engines and real institutional evidence without changing the invariant.

Not legal advice. MIT licence.
