const log = document.getElementById("log"), msg = document.getElementById("msg");
const history = [];

const esc = s => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
const fmt = s => esc(s).replace(/\*\*(.+?)\*\*/g, "<b>$1</b>").replace(/`([^`]+)`/g, "<code>$1</code>")
  .replace(/^- (.*)$/gm, "&bull; $1").replace(/\n/g, "<br>");

function add(role, text, mode) {
  const d = document.createElement("div");
  d.className = "m " + (role === "user" ? "me" : "bot");
  d.innerHTML = fmt(text) + (mode ? `<small>${esc(mode)}</small>` : "");
  log.appendChild(d); log.scrollTop = log.scrollHeight;
  return d;
}

async function send(text) {
  text = (text || msg.value).trim(); if (!text) return;
  msg.value = ""; add("user", text);
  const wait = add("assistant", "Thinking...");
  try {
    const r = await fetch("/api/chat", {method: "POST", headers: {"Content-Type": "application/json"},
      body: JSON.stringify({message: text, history})});
    const j = await r.json(); wait.remove();
    add("assistant", j.reply || j.error, j.mode);
    history.push({role: "user", content: text}, {role: "assistant", content: j.reply || ""});
  } catch (e) { wait.remove(); add("assistant", "Server not reachable. Is app.py running?"); }
}

function upload(id, kind) {
  document.getElementById(id).addEventListener("change", async e => {
    const f = e.target.files[0]; if (!f) return;
    add("user", `Uploaded ${f.name} for ${kind} analysis`);
    const fd = new FormData(); fd.append("file", f);
    const r = await fetch("/api/analyze/" + kind, {method: "POST", body: fd});
    const j = await r.json(); add("assistant", j.reply || j.error, "tool"); e.target.value = "";
  });
}

document.getElementById("send").onclick = () => send();
msg.addEventListener("keydown", e => { if (e.key === "Enter") send(); });
document.querySelectorAll(".chip").forEach(c => c.onclick = () => send(c.dataset.q));
upload("f-access", "access"); upload("f-logs", "logs");

fetch("/api/health").then(r => r.json()).then(h => {
  const s = document.getElementById("status");
  s.textContent = h.llm ? `AI: ${h.model} online` : "Offline mode (knowledge base)";
  s.classList.toggle("on", h.llm);
}).catch(() => {});
add("assistant", "Hi! I'm **IAM Copilot**, built by Abhinav A V. Type `/help` to see what I can do.");
