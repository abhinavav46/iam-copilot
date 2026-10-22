"""Deterministic IAM/security tools. No network, no AI needed."""
import base64
import csv
import io
import json
import math
import re
from collections import defaultdict
from datetime import datetime, timezone

COMMON = {"password", "123456", "qwerty", "letmein", "admin", "welcome", "iloveyou", "abc123", "password1", "admin123"}

# (entitlement A, entitlement B, why it is a conflict) - Segregation of Duties rules
SOD_RULES = [
    ("create_vendor", "approve_payment", "Same person can create a vendor and pay it (fraud risk)"),
    ("submit_expense", "approve_expense", "Self-approval of expenses"),
    ("developer", "prod_admin", "Developer with production admin access"),
    ("create_user", "approve_access", "Can create accounts and approve their access"),
    ("request_access", "approve_access", "Can request and approve own access"),
]


def check_password(pw: str) -> str:
    if not pw:
        return "Usage: `/password <text>`"
    pool = 26 * bool(re.search(r"[a-z]", pw)) + 26 * bool(re.search(r"[A-Z]", pw)) \
        + 10 * bool(re.search(r"\d", pw)) + 32 * bool(re.search(r"[^A-Za-z0-9]", pw))
    bits = len(pw) * math.log2(pool) if pool else 0
    tips = []
    if len(pw) < 12:
        tips.append("use 12+ characters (a passphrase of 4+ random words is best)")
    if pool < 62:
        tips.append("mix upper/lower case, digits and symbols")
    if pw.lower() in COMMON or re.search(r"(.)\1{2,}", pw) or re.search(r"(?:0123|1234|2345|abcd|qwer)", pw.lower()):
        bits = min(bits, 20)
        tips.append("avoid common words, repeats and keyboard/number sequences")
    rating = "Very weak" if bits < 40 else "Fair" if bits < 60 else "Strong" if bits < 80 else "Very strong"
    out = f"**Password strength: {rating}** (~{bits:.0f} bits entropy)\nNote: nothing is stored or sent anywhere."
    return out + ("\nSuggestions:\n- " + "\n- ".join(tips) if tips else "")


def _b64(part: str) -> dict:
    return json.loads(base64.urlsafe_b64decode(part + "=" * (-len(part) % 4)))


def decode_jwt(token: str) -> str:
    parts = token.strip().split(".")
    if len(parts) != 3:
        return "That does not look like a JWT (expected 3 dot-separated parts). Usage: `/jwt <token>`"
    try:
        header, payload = _b64(parts[0]), _b64(parts[1])
    except Exception:
        return "Could not decode the token - it is malformed."
    warn = []
    alg = str(header.get("alg", "?"))
    if alg.lower() == "none":
        warn.append("alg=none: unsigned token, must be rejected by servers")
    elif alg.startswith("HS"):
        warn.append("HMAC-signed: shared secret needed; make sure it is long and random")
    exp = payload.get("exp")
    if exp is None:
        warn.append("no `exp` claim: token never expires")
    else:
        when = datetime.fromtimestamp(exp, tz=timezone.utc)
        warn.append(f"expires {when:%Y-%m-%d %H:%M} UTC ({'EXPIRED' if when < datetime.now(timezone.utc) else 'still valid'})")
    for c in ("iss", "aud", "sub"):
        if c not in payload:
            warn.append(f"missing `{c}` claim")
    return ("**Header:** `" + json.dumps(header) + "`\n**Payload:** `" + json.dumps(payload) + "`\n**Findings:**\n- "
            + "\n- ".join(warn) + "\nSignature is NOT verified by this tool.")


def _rows(text: str):
    rows = list(csv.DictReader(io.StringIO(text)))
    return [{(k or "").strip().lower(): (v or "").strip() for k, v in r.items()} for r in rows]


def analyze_access(text: str, today: datetime = None) -> str:
    """CSV columns: user,entitlement,manager,last_login(YYYY-MM-DD). Finds SoD, dormant, orphan, over-privileged."""
    today = today or datetime.now()
    rows = _rows(text)
    ents, mgr, login = defaultdict(set), {}, {}
    for r in rows:
        u = r.get("user")
        if not u:
            continue
        ents[u].add(r.get("entitlement", "").lower())
        mgr[u] = r.get("manager", "")
        try:
            d = datetime.strptime(r.get("last_login", ""), "%Y-%m-%d")
            login[u] = max(d, login.get(u, d))
        except ValueError:
            pass
    sod = [(u, why) for u, e in ents.items() for a, b, why in SOD_RULES if a in e and b in e]
    dormant = [(u, (today - d).days) for u, d in login.items() if (today - d).days > 90]
    orphan = [u for u in ents if not mgr.get(u)]
    heavy = [(u, len(e)) for u, e in ents.items() if len(e) >= 5]
    out = [f"**Access review: {len(ents)} users, {len(rows)} assignments**"]
    out.append("\n**SoD conflicts:** " + ("none" if not sod else "\n- " + "\n- ".join(f"{u}: {w}" for u, w in sod)))
    out.append("**Dormant (>90 days):** " + ("none" if not dormant else "\n- " + "\n- ".join(f"{u}: {d} days" for u, d in dormant)))
    out.append("**No manager (orphan):** " + (", ".join(orphan) or "none"))
    out.append("**Over-privileged (5+ entitlements):** " + (", ".join(f"{u} ({n})" for u, n in heavy) or "none"))
    out.append("\n_Recommendation: revoke dormant access, remove one side of each SoD pair, assign owners to orphans, then re-certify._")
    return "\n".join(out)


def analyze_logs(text: str) -> str:
    """CSV columns: timestamp,user,ip,result(SUCCESS|FAIL). Finds brute force, spraying, success-after-failures."""
    rows = sorted(_rows(text), key=lambda r: r.get("timestamp", ""))
    fails, ip_users, streak, hits = defaultdict(int), defaultdict(set), defaultdict(int), []
    for r in rows:
        u, ip, ok = r.get("user", ""), r.get("ip", ""), r.get("result", "").upper().startswith("S")
        if ok:
            if streak[u] >= 3:
                hits.append(f"{u} logged in from {ip} after {streak[u]} failures - possible compromise")
            streak[u] = 0
        else:
            fails[u] += 1
            streak[u] += 1
            ip_users[ip].add(u)
    brute = [f"{u}: {n} failed logins" for u, n in fails.items() if n >= 5]
    spray = [f"{ip}: failed against {len(us)} accounts" for ip, us in ip_users.items() if len(us) >= 4]
    out = [f"**Auth log analysis: {len(rows)} events**"]
    out.append("**Brute force:** " + ("none" if not brute else "\n- " + "\n- ".join(brute)))
    out.append("**Password spraying:** " + ("none" if not spray else "\n- " + "\n- ".join(spray)))
    out.append("**Success after failures:** " + ("none" if not hits else "\n- " + "\n- ".join(hits)))
    out.append("\n_Recommendation: lockout/rate-limit, enforce MFA, block offending IPs, force reset on flagged accounts._")
    return "\n".join(out)
