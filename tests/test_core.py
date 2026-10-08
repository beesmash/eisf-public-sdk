import json
import unittest

from eisf.core import build_prompt, validate_case
from eisf.providers import MockProvider


class CoreTests(unittest.TestCase):
    def valid_case(self):
        return {
            "event": {"statement": "A change occurred."},
            "impacts": [{"statement": "A system is affected."}],
            "scenarios": [{"statement": "One plausible branch exists."}],
            "adaptations": [{"statement": "A mitigation is available."}],
            "decision": {"statement": "Proceed with review.", "status": "decided"}
        }

    def test_valid_case(self):
        self.assertTrue(validate_case(self.valid_case()).valid)

    def test_missing_stage(self):
        case = self.valid_case()
        del case["decision"]
        self.assertFalse(validate_case(case).valid)

    def test_empty_array(self):
        case = self.valid_case()
        case["impacts"] = []
        self.assertFalse(validate_case(case).valid)

    def test_confidence_range(self):
        case = self.valid_case()
        case["event"]["confidence"] = 1.5
        self.assertFalse(validate_case(case).valid)

    def test_deferred_decision(self):
        case = self.valid_case()
        case["decision"]["status"] = "deferred"
        self.assertTrue(validate_case(case).valid)

    def test_mock_provider_returns_core_case(self):
        raw = MockProvider().generate("instructions", "Example event")
        self.assertTrue(validate_case(json.loads(raw)).valid)

    def test_developer_prompt(self):
        prompt = build_prompt("Feature request", developer=True)
        self.assertIn("security", prompt)
        self.assertIn("rollback", prompt)


if __name__ == "__main__":
    unittest.main()
