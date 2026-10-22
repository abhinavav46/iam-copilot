"""IAM Copilot - local IAM/cybersecurity AI agent. Built by Abhinav A V."""
from flask import Flask, jsonify, request, send_from_directory

from agent import llm, tools
from agent.core import Agent

app = Flask(__name__, static_folder="static", static_url_path="")
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024  # 2 MB upload limit
agent = Agent()


@app.get("/")
def index():
    return send_from_directory("static", "index.html")


@app.get("/api/health")
def health():
    return jsonify(status="ok", llm=llm.available(), model=llm.MODEL, kb_sections=len(agent.kb.docs))


@app.post("/api/chat")
def chat():
    data = request.get_json(silent=True) or {}
    message = str(data.get("message", "")).strip()
    if not message:
        return jsonify(error="Empty message"), 400
    return jsonify(agent.reply(message[:4000], data.get("history")))


@app.post("/api/analyze/<kind>")
def analyze(kind):
    fn = {"access": tools.analyze_access, "logs": tools.analyze_logs}.get(kind)
    f = request.files.get("file")
    if not fn or not f:
        return jsonify(error="Use /api/analyze/access or /logs with a CSV 'file'"), 400
    try:
        return jsonify(reply=fn(f.read().decode("utf-8-sig")), mode="tool")
    except Exception as e:  # malformed CSV etc.
        return jsonify(reply=f"Could not parse the CSV: {e}", mode="tool"), 400


if __name__ == "__main__":
    print("IAM Copilot running at http://127.0.0.1:5000  (built by Abhinav A V)")
    app.run(host="127.0.0.1", port=5000, debug=False)
