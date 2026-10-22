"""Agent brain: slash-commands -> tools, otherwise RAG over the IAM knowledge base, optionally with a local LLM."""
from pathlib import Path

from . import llm, tools
from .knowledge import KB

SYSTEM = (
    "You are IAM Copilot, a local assistant built by Abhinav A V. You are an expert in Identity & Access "
    "Management (SailPoint, Saviynt, CyberArk, OAuth/OIDC/SAML, PAM, Zero Trust) and QA automation. "
    "Prefer the provided context for IAM questions. If the user asks something general, help them anyway. "
    "Be concise, practical and accurate; say when you are unsure."
)

HELP = """**IAM Copilot - built by Abhinav A V**
Ask any IAM / security question, or use tools:
- `/password <text>` - password strength check
- `/jwt <token>` - decode and audit a JWT
- `/topics` - list knowledge-base topics
- Buttons below the chat: upload an **access CSV** (SoD / dormant / orphan review) or an **auth-log CSV** (brute force / spraying)
Install Ollama for full AI answers; otherwise answers come from the built-in knowledge base."""


class Agent:
    def __init__(self):
        self.kb = KB(Path(__file__).resolve().parent.parent / "knowledge")

    def command(self, text: str) -> dict:
        cmd, _, arg = text.partition(" ")
        cmd = cmd.lower()
        if cmd == "/password":
            return {"reply": tools.check_password(arg.strip()), "mode": "tool"}
        if cmd == "/jwt":
            return {"reply": tools.decode_jwt(arg), "mode": "tool"}
        if cmd == "/topics":
            return {"reply": "**Topics:**\n- " + "\n- ".join(t for t, _, _ in self.kb.docs), "mode": "tool"}
        return {"reply": HELP, "mode": "tool"}

    def reply(self, message: str, history=None) -> dict:
        if message.startswith("/"):
            return self.command(message)
        hits = self.kb.search(message)
        history = [{"role": h["role"], "content": str(h["content"])[:2000]} for h in (history or [])
                   if isinstance(h, dict) and h.get("role") in ("user", "assistant") and "content" in h][-6:]
        if llm.available():
            ctx = "\n\n".join(f"[{h['title']}]\n{h['text']}" for h in hits)
            msgs = [{"role": "system", "content": f"{SYSTEM}\n\nContext:\n{ctx}"}] + history + [{"role": "user", "content": message}]
            try:
                return {"reply": llm.chat(msgs), "mode": "llm+rag", "sources": [h["title"] for h in hits]}
            except Exception:
                pass  # fall through to knowledge-base mode
        if hits and hits[0]["score"] >= 1.5:
            top = hits[0]
            more = [h["title"] for h in hits[1:]]
            text = f"**{top['title']}**\n{top['text']}" + (f"\n\nRelated: {', '.join(more)}" if more else "")
            return {"reply": text, "mode": "knowledge-base", "sources": [top["title"]]}
        return {"reply": "I don't have that in my built-in knowledge base. Install Ollama (see README) to answer "
                         "general questions, or try `/topics` to see what I know.", "mode": "none"}
