def _cards(items):
    return '<div class="grid">' + "".join(f'<div class="fc"><span class="n">{n}</span><b>{t}</b><p>{d}</p></div>' for n, t, d in items) + "</div>"


HERO = ('<div class="hero5"><div class="ttlbox"><h1 class="big"><span>SENTINEL LOG AI</span></h1></div><div class="sub"><h2>Threat detection, in plain sight</h2>'
        '<p>An open-source dashboard that finds suspicious requests in your server logs with machine learning and signature rules, '
        'then explains every incident in plain English. It runs entirely on your own machine.</p></div></div>')

HOME_BODY = (
    '<div class="panel-h"><i></i>How it works</div>'
    + _cards([("01", "Ingest", "Load a CSV or raw access log, a preset scenario, or a 600-request synthetic dataset."),
              ("02", "Detect", "An Isolation Forest scores every request while signature rules catch known attack patterns."),
              ("03", "Triage", "Each incident gets a short threat summary and a suggested action, from a local LLM or an offline heuristic."),
              ("04", "Act", "Review the incident queue, then export a report or an IP blocklist.")])
    + '<div class="panel-h"><i></i>Feature manual</div>'
    + _cards([("A", "Data sources", "Upload .csv, .log or .txt files. CSVs need ip, request_path, status_code and response_size columns."),
              ("B", "Anomaly scoring", "Features include path entropy, special characters, payload size and per-IP behaviour. Scores run 0 to 1; the sensitivity slider sets the expected anomaly rate."),
              ("C", "Signatures and MITRE tags", "SQL injection, path traversal, XSS and recon patterns are labelled and mapped to MITRE ATT&amp;CK technique IDs."),
              ("D", "Brute-force detection", "Three or more failed (401/403) requests from one IP against one path are flagged."),
              ("E", "Local AI triage", "Uses Ollama on your computer. Without it, the app falls back to a rule-based summary and says so."),
              ("F", "Exports and controls", "Download the incident report (CSV) or an IP blocklist (TXT). Use the gear icon to reset logs or switch light and dark mode.")]))

SPECS = (
    '<div class="panel-h"><i></i>Specs &amp; info</div>'
    + _cards([("ML", "Detection engine", "scikit-learn Isolation Forest, 300 trees, StandardScaler, adjustable contamination (1 to 50%)."),
              ("FX", "Feature set", "Path length and entropy, special and percent-encoded characters, response size, status class, signature flags, per-IP request count, error ratio and path diversity."),
              ("UI", "Stack", "Python, Streamlit, pandas, NumPy, Altair, Requests. Optional local LLM through Ollama (default model: mistral)."),
              ("PV", "Privacy and cost", "No accounts, API keys or telemetry from the app itself. Logs stay on your machine and there are no usage fees."),
              ("LM", "Limitations", "Unsupervised detection on small or synthetic data is a demo, not proof. Signatures catch known patterns only, and LLM output can be wrong; verify before acting."),
              ("V5", "Version", "v5. Open source under the MIT License.")]))

_L = [("License (MIT)", "SentinelLog AI is released under the MIT License. Copyright (c) 2026 SentinelLog AI contributors. You may use, copy, modify, merge, publish, distribute, sublicense and sell copies of the software, provided the copyright and permission notice are included in all copies. The full text is in the LICENSE file."),
      ("No warranty", "THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY ARISING FROM THE USE OF THE SOFTWARE."),
      ("Not a substitute for security tooling", "Results are statistical and may include false positives and false negatives. AI-generated triage text may be inaccurate. This tool does not replace professional security monitoring, incident response or legal advice."),
      ("Authorized use only", "Analyze only logs you own or are explicitly authorized to analyze. You are responsible for complying with applicable laws, workplace policies and the privacy rights of the people whose activity appears in the logs."),
      ("Privacy", "The app processes data locally in your browser session and on your machine and does not transmit logs to the developers. If you deploy it publicly or point it at a hosted LLM, data may leave your machine; warn users and review that provider's terms."),
      ("Third-party software and trademarks", "Built with Streamlit, scikit-learn, pandas, NumPy, Altair and Requests, each under its own open-source license. Optional triage uses Ollama and a model such as Mistral, subject to their licenses. MITRE ATT&amp;CK&reg; is a registered trademark of The MITRE Corporation. All other names belong to their owners, and this project is not affiliated with or endorsed by them.")]

LEGAL = ('<div id="learn"></div><div class="panel-h"><i></i>Learn more<em>legal notices</em></div>'
         + "".join(f'<details class="legal"><summary>{t}</summary><p>{d}</p></details>' for t, d in _L)
         + '<p style="text-align:center;opacity:.6;font-size:.8rem;margin:2rem 0 1rem">SentinelLog AI is free, open-source software.</p>')
