"""Sovereign Disclosure Plane — Live Case 03 reference model.

Reference implementation, not a deployment claim.
Invariant: zero outbound PII until channel, principal, capacity, mandate,
scope and required approvals are complete. AI override is always rejected.
"""
from __future__ import annotations
import hashlib
import json
from datetime import datetime, timezone

IRREVERSIBLE = ("release_pii", "export_kyc", "disclose_tx_history")


def utc_now():
    return datetime.now(timezone.utc).isoformat()


class Ledger:
    def __init__(self, clock=utc_now):
        self.chain = []
        self.clock = clock

    def append(self, event):
        previous = self.chain[-1]["hash"] if self.chain else "GENESIS"
        entry = {"previous_hash": previous, "timestamp": self.clock(), **event}
        payload = json.dumps(entry, sort_keys=True, separators=(",", ":"))
        entry["hash"] = hashlib.sha256(payload.encode()).hexdigest()
        self.chain.append(entry)
        return entry

    def verify(self):
        for index, entry in enumerate(self.chain):
            previous = self.chain[index - 1]["hash"] if index else "GENESIS"
            if entry.get("previous_hash") != previous:
                return False
            body = {key: value for key, value in entry.items() if key != "hash"}
            payload = json.dumps(body, sort_keys=True, separators=(",", ":"))
            if hashlib.sha256(payload.encode()).hexdigest() != entry.get("hash"):
                return False
        return True


def _non_empty(value):
    return bool(value) and value not in {"unknown", "unverified", "stale"}


def evaluate(request, ledger):
    required = set(request.get("required_approvals", []))
    completed = set(request.get("completed_approvals", []))
    scope = request.get("scope", {})
    mandate = request.get("mandate", {})
    gates = {
        "channel": request.get("channel_evidence", {}).get("status") == "pass",
        "principal": request.get("principal", {}).get("verified_out_of_band") is True,
        "capacity": request.get("capacity", {}).get("current") == "verified",
        "mandate": all(_non_empty(mandate.get(key)) for key in ("legal_basis", "case_id", "jurisdiction")),
        "scope": bool(scope.get("subjects")) and bool(scope.get("fields")) and _non_empty(scope.get("time_range")),
        "approvals": required.issubset(completed),
    }

    if request.get("ai_override"):
        decision = {"state": "REJECT", "reason": "ai_override_attempt", "packet_out": None, "gates": gates}
    elif not all(gates.values()):
        decision = {
            "state": "HOLD",
            "reason": "incomplete_authority_chain",
            "permits": ["preserve", "prepare_internal", "restrict_deletion", "escalate"],
            "forbids": list(IRREVERSIBLE),
            "packet_out": None,
            "gates": gates,
        }
    else:
        packet = {
            "decision": "DATA_OUT",
            "request_id": request.get("request_id"),
            "scope": scope,
            "completed_approvals": sorted(completed),
        }
        decision = {"state": "RELEASE", "reason": "all_gates_green", "packet_out": packet, "gates": gates}

    receipt = ledger.append({
        "type": "DISCLOSURE_DECISION",
        "request_id": request.get("request_id"),
        "state": decision["state"],
        "reason": decision["reason"],
        "gates": gates,
        "packet_hash": hashlib.sha256(json.dumps(decision["packet_out"], sort_keys=True).encode()).hexdigest() if decision["packet_out"] else None,
    })
    return {**decision, "receipt": receipt}
