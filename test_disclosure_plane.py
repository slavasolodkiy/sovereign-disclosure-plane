import unittest
from disclosure_plane import evaluate, Ledger, IRREVERSIBLE


def request(**updates):
    base = {
        "request_id": "DW-TEST",
        "channel_evidence": {"type": "gov_domain_email", "status": "pass", "role": "evidence_only"},
        "principal": {"name": "J. Smith", "verified_out_of_band": True},
        "capacity": {"agency_id": "AG-1", "current": "verified"},
        "mandate": {"legal_basis": "statute-42", "case_id": "C-9", "jurisdiction": "UK"},
        "scope": {"subjects": ["subj-1"], "fields": ["name"], "time_range": "2026"},
        "required_approvals": ["dual_control"],
        "completed_approvals": ["dual_control"],
        "ai_override": False,
    }
    base.update(updates)
    return base


def fixed_clock():
    return "2026-10-11T12:00:00+00:00"


class TestPlane(unittest.TestCase):
    def evaluate(self, req):
        ledger = Ledger(clock=fixed_clock)
        result = evaluate(req, ledger)
        self.assertTrue(ledger.verify())
        return result, ledger

    def test_channel_only_never_releases(self):
        result, _ = self.evaluate(request(principal={"name": None, "verified_out_of_band": False}))
        self.assertEqual(result["state"], "HOLD")
        self.assertIsNone(result["packet_out"])

    def test_missing_approval_never_releases(self):
        result, _ = self.evaluate(request(completed_approvals=[]))
        self.assertEqual(result["state"], "HOLD")
        self.assertFalse(result["gates"]["approvals"])

    def test_ai_cannot_override(self):
        result, _ = self.evaluate(request(ai_override=True))
        self.assertEqual(result["state"], "REJECT")
        self.assertIsNone(result["packet_out"])

    def test_hold_releases_zero_pii(self):
        result, _ = self.evaluate(request(scope={"subjects": [], "fields": [], "time_range": None}))
        self.assertEqual(result["state"], "HOLD")
        for action in IRREVERSIBLE:
            self.assertIn(action, result["forbids"])

    def test_full_chain_releases_only_scoped_packet(self):
        result, _ = self.evaluate(request())
        self.assertEqual(result["state"], "RELEASE")
        self.assertEqual(result["packet_out"]["scope"]["subjects"], ["subj-1"])
        self.assertEqual(result["packet_out"]["completed_approvals"], ["dual_control"])

    def test_every_decision_is_receipted_and_tampering_breaks_chain(self):
        ledger = Ledger(clock=fixed_clock)
        evaluate(request(), ledger)
        evaluate(request(completed_approvals=[]), ledger)
        self.assertTrue(ledger.verify())
        ledger.chain[0]["state"] = "REJECT"
        self.assertFalse(ledger.verify())

if __name__ == "__main__":
    unittest.main(verbosity=2)
