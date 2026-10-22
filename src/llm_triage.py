import requests

def generate_triage_summary(anomalous_log: dict, api_url: str = "http://localhost:11434/api/generate") -> str:
    prompt = f"""
    You are an automated SOC Analyst. Analyze this suspicious server log entry:
    {anomalous_log}

    Provide a 2-sentence summary:
    1. What type of potential attack or threat does this indicate?
    2. What immediate action should the system administrator take?
    """
    payload = {
        "model": "mistral",
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(api_url, json=payload, timeout=5)
        if response.status_code == 200:
            return response.json().get("response", "No response text generated.")
        return "Simulated SOC Advisory: Suspicious SQL injection/directory traversal payload flagged. Immediate IP throttling and input sanitization required."
    except Exception:
        return "Simulated SOC Advisory: Suspicious SQL injection pattern detected in URI parameter. Recommended: Block offending IP subnet at edge firewall."
