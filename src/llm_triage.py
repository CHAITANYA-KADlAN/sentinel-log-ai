import os

import requests

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral")

ADVICE = {
    "SQL injection": ("Likely SQL injection attempt.", "Block the source IP, review WAF rules, and use parameterized queries."),
    "Path traversal": ("Likely directory traversal / sensitive file access attempt.", "Block the source, verify file permissions, and normalize request paths."),
    "XSS": ("Likely cross-site scripting probe.", "Enable output encoding and a Content-Security-Policy; block the source."),
    "Recon / probing": ("Likely automated reconnaissance or credential attack.", "Rate-limit or block the IP and enforce MFA on the targeted endpoint."),
}


def _heuristic(row: dict, signatures: list) -> str:
    if signatures:
        what, do = ADVICE[signatures[0]]
        return f"{what} {do}"
    return ("Statistically unusual request (no known signature matched). "
            "Review the source IP's other activity and compare against its normal baseline.")


def generate_triage_summary(row: dict, signatures: list | None = None) -> tuple:
    """Returns (text, source) where source is 'llm' or 'heuristic'."""
    prompt = (
        "You are a SOC analyst. Analyze this suspicious log entry and answer in exactly two "
        f"sentences: (1) likely threat type, (2) immediate action.\n\n{row}"
    )
    try:
        r = requests.post(OLLAMA_URL, json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False}, timeout=30)
        if r.status_code == 200 and r.json().get("response"):
            return r.json()["response"].strip(), "llm"
    except requests.RequestException:
        pass
    return _heuristic(row, signatures or []), "heuristic"
