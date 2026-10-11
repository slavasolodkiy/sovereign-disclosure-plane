<!-- ============================================================
SOVEREIGN DISCLOSURE PLANE · LIVE CASE 03 · README
Teenage-Engineering × Nothing × acid-glitch aesthetic
Sovereign Agent Lab · design system v2
============================================================ -->

<div align="center">

<pre>
██████╗ ██╗███████╗ ██████╗██╗      ██████╗ ███████╗██╗   ██╗██████╗ ███████╗
██╔══██╗██║██╔════╝██╔════╝██║     ██╔═══██╗██╔════╝██║   ██║██╔══██╗██╔════╝
██║  ██║██║███████╗██║     ██║     ██║   ██║█████╗  ██║   ██║██████╔╝█████╗
██║  ██║██║╚════██║██║     ██║     ██║   ██║██╔══╝  ██║   ██║██╔══██╗██╔══╝
██████╔╝██║███████║╚██████╗███████╗╚██████╔╝██║     ╚██████╔╝██║  ██║███████╗
╚═════╝ ╚═╝╚══════╝ ╚═════╝╚══════╝ ╚═════╝ ╚═╝      ╚═════╝ ╚═╝  ╚═╝╚══════╝
██╗      █████╗ ███╗   ██╗███████╗
██║     ██╔══██╗████╗  ██║██╔════╝
██║     ███████║██╔██╗ ██║█████╗
██║     ██╔══██║██║╚██╗██║██╔══╝
███████╗███████║██║ ╚████║███████╗
╚══════╝╚══════╝╚═╝  ╚═══╝╚══════╝
L I V E   C A S E   0 3
</pre>

# `SOVEREIGN DISCLOSURE PLANE`

**Live Case 03 reference model.**

> **The domain may be real while the authority is not. Channel-only never releases.**

<img src="https://img.shields.io/badge/STATUS-tested%20reference%20model%20%C2%B7%20not%20a%20deployment%20claim-c8ff00?style=for-the-badge&labelColor=0b0d11" alt="status">
<img src="https://img.shields.io/badge/INVARIANT-zero%20outbound%20PII%20until%20all%20gates%20green-ff2d9a?style=for-the-badge&labelColor=0b0d11" alt="invariant">
<img src="https://img.shields.io/badge/RECEIPTS-SHA--256%20chained-35f2ff?style=for-the-badge&labelColor=0b0d11" alt="receipts">
<img src="https://img.shields.io/badge/DATA-synthetic%20only-9b7bff?style=for-the-badge&labelColor=0b0d11" alt="data">
<img src="https://img.shields.io/badge/LICENCE-MIT-00e676?style=for-the-badge&labelColor=0b0d11" alt="mit">

[Canonical incident page](https://www.solodkiy.cv/revolut-incident.html) · [Full research trail — Sovereign Agent Lab](https://www.solodkiy.cv/sovereign-agent-lab.html)

</div>

---

## ▚ THE RULE AS A PIPELINE

This repository turns the five authority gates into an executable disclosure rule:

```text
CHANNEL → PRINCIPAL → CAPACITY → MANDATE → SCOPE → REQUIRED APPROVALS
```

The invariant is strict: **zero outbound PII until every gate is green.** Disclosure is irreversible; there is no provisional release and no “minimum dataset” escape hatch. `ai_override = false` always.

```text
        ┌─────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐  ┌────────┐  ┌───────────┐
  PII ─►│ CHANNEL │─►│ PRINCIPAL│─►│ CAPACITY │─►│ MANDATE │─►│ SCOPE  │─►│ APPROVALS │
 request└────┬────┘  └────┬─────┘  └────┬─────┘  └────┬────┘  └───┬────┘  └─────┬─────┘
             │            │             │             │            │             │
             ▼            ▼             ▼             ▼            ▼             ▼
          [gate 1]     [gate 2]      [gate 3]      [gate 4]     [gate 5]     [approval]
             │            │             │             │            │             │
             └────────────┴───── any red ────────────┴────────────┴─────────────┘
                                    │
                                    ▼
              ┌────────────────────────────────────────────────────┐
              │ HOLD    · missing gate → decision + chained receipt│
              │ REJECT  · AI override attempt → always             │
              │ RELEASE · scoped packet only → SHA-256 receipt     │
              └────────────────────────────────────────────────────┘
```

## ▚ RUN

```bash
python3 -m unittest discover -s tests -v
python3 run.py examples/release.json
python3 run.py examples/hold-missing-approval.json
```

## ▚ WHAT IS IMPLEMENTED NOW

- HOLD when principal, capacity, mandate, scope or required approvals are incomplete.
- REJECT on attempted AI override.
- RELEASE only as a scoped packet after every gate passes.
- Full SHA-256 chained receipts for every decision.
- Tamper detection and deterministic test clock.
- Synthetic examples only.

## ▚ WHAT IS DELIBERATELY POSTPONED

- Cryptographic credentials and key management.
- Real institutional directories and out-of-band verification.
- Legal interpretation of mandate, jurisdiction and time range.
- Production review UI, audit export and operational integrations.
- Any affiliation with or endorsement by Revolut.

This is the smallest executable answer that preserves the central claim today. Later versions can replace booleans and strings with verifiable credentials, policy engines and real institutional evidence without changing the invariant.

## ▚ COLOPHON

Not legal advice. MIT licence.

<div align="center">

`CHANNEL → PRINCIPAL → CAPACITY → MANDATE → SCOPE · ZERO OUTBOUND PII UNTIL ALL GATES GREEN`

</div>
