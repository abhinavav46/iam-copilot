import base64
import json
import sys
import unittest
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from agent import tools  # noqa: E402
from agent.core import Agent  # noqa: E402


def b64(d):
    return base64.urlsafe_b64encode(json.dumps(d).encode()).decode().rstrip("=")


class ToolTests(unittest.TestCase):
    def test_weak_password(self):
        self.assertIn("Very weak", tools.check_password("password"))

    def test_strong_password(self):
        self.assertIn("Very strong", tools.check_password("c0rrect-Horse-Battery-staple!9"))

    def test_jwt_none_alg(self):
        tok = f"{b64({'alg': 'none'})}.{b64({'sub': 'x'})}."
        out = tools.decode_jwt(tok.rstrip(".") + ".sig")
        self.assertIn("alg=none", out)
        self.assertIn("no `exp`", out)

    def test_access_review(self):
        out = tools.analyze_access((ROOT / "sample_data/access.csv").read_text(), today=datetime(2026, 10, 21))
        self.assertIn("alice: Same person can create a vendor", out)
        self.assertIn("erin: 233 days", out)
        self.assertIn("gina", out)
        self.assertIn("henry (5)", out)

    def test_log_analysis(self):
        out = tools.analyze_logs((ROOT / "sample_data/auth_log.csv").read_text())
        self.assertIn("gina: 5 failed logins", out)
        self.assertIn("203.0.113.9: failed against 5 accounts", out)
        self.assertIn("gina logged in", out)


class AgentTests(unittest.TestCase):
    def test_kb_answer(self):
        r = Agent().reply("What is segregation of duties?")
        self.assertIn("SoD", r["reply"])

    def test_commands(self):
        self.assertIn("IAM Copilot", Agent().reply("/help")["reply"])


if __name__ == "__main__":
    unittest.main()
