# IAM Copilot

**Built by Abhinav A V**

A local, privacy-friendly AI agent for **Identity & Access Management (IAM)** and cybersecurity. It runs on your own machine, answers IAM questions (SailPoint, OAuth/OIDC/SAML, PAM, Zero Trust, QA automation), and ships with practical security tools. It can also answer general questions when a local LLM (Ollama) is connected.
<img width="902" height="852" alt="image" src="https://github.com/user-attachments/assets/8aa14f55-8bac-45d0-9b41-e9bd45ccb8c0" />

## Features
- **RAG knowledge base** (BM25 search over Markdown files in `knowledge/`) - works with no AI model installed
- **Optional local LLM** via [Ollama](https://ollama.com) - answers stay on your device
- **Access review tool**: upload a CSV to find SoD conflicts, dormant, orphan and over-privileged users
- **Auth-log analyzer**: detects brute force, password spraying, success-after-failures
- **JWT decoder/auditor** (`/jwt`) and **password strength checker** (`/password`)
- Flask REST API + dark-themed web UI, unit tests, GitHub Actions CI

## Architecture
```
Browser UI (HTML/CSS/JS) -> Flask API (app.py) -> Agent (agent/core.py)
                                                   |- tools.py      (deterministic security tools)
                                                   |- knowledge.py  (BM25 retrieval over knowledge/*.md)
                                                   '- llm.py        (optional Ollama client)
```

## Quick start (VS Code)
1. Install Python 3.10+ and open this folder in VS Code (`File > Open Folder`).
2. Open a terminal in VS Code and run:
```bash
python -m venv .venv
# Windows:  .venv\Scripts\activate      Mac/Linux:  source .venv/bin/activate
pip install -r requirements.txt
python app.py
```
3. Open http://127.0.0.1:5000

### Optional: enable full AI answers
```bash
# install Ollama from https://ollama.com, then:
ollama pull llama3.2
# optional overrides: OLLAMA_MODEL=llama3.2  OLLAMA_URL=http://localhost:11434
```
Restart the app; the badge shows "AI: llama3.2 online".

## Try it
- Ask: `What is SoD?`, `Explain aggregation and correlation in SailPoint`, `OAuth vs OIDC vs SAML`
- Click **Upload access CSV** and pick `sample_data/access.csv`
- Click **Upload auth-log CSV** and pick `sample_data/auth_log.csv`
- Type `/password Summer2024!` or `/jwt <token>`

## Run tests
```bash
python -m unittest discover -s tests -v
```

## Extend it
- Add Markdown files to `knowledge/` using `## Question-style headings`
- Add SoD rules in `agent/tools.py` (`SOD_RULES`)
- Add new slash commands in `agent/core.py`



## Disclaimer
Educational/portfolio project. Knowledge-base answers are summaries; verify against vendor documentation before production decisions. The JWT tool does not verify signatures.

## License
MIT (c) 2026 Abhinav A V
