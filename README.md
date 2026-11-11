# 🛡️ SentinelLog AI

Anomaly detection for server logs: an Isolation Forest finds statistically unusual requests, signature rules label known attack patterns, and a local LLM (Ollama) writes short incident triage notes. Without Ollama it falls back to an offline heuristic and labels it as such.

## Run

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
streamlit run src/app.py
```

Optional LLM triage: install [Ollama](https://ollama.com), `ollama pull mistral`. Override with `OLLAMA_MODEL` / `OLLAMA_URL`.

## How it works

```text
raw logs → clean → features (path entropy, special chars, payload size, per-IP rate & error ratio)
         → StandardScaler → Isolation Forest (0–1 anomaly score)
         → + signature rules (SQLi, traversal, XSS, recon) → incident queue → LLM triage
```

The synthetic dataset carries ground-truth labels, so the dashboard reports recall and precision. Run tests with `pytest tests`.

## Limitations (honest)

- Unsupervised detection on synthetic data is a demo, not proof; next step is a public dataset (e.g. CIC-IDS / HTTP CSIC 2010) with a proper evaluation.
- Signatures catch known patterns; the ML layer is what can surface unfamiliar behaviour, so call it anomaly detection, not "zero-day" detection.
