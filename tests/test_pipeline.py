import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from feature_engineering import brute_force_mask, clean_logs, extract_features, find_signatures  # noqa: E402
from model import LogAnomalyDetector  # noqa: E402
from synthetic import generate_traffic  # noqa: E402


def test_signatures():
    assert "SQL injection" in find_signatures("/login?u=admin' OR '1'='1")
    assert "Path traversal" in find_signatures("/../../etc/passwd")
    assert find_signatures("/index.html") == []


def test_detector_recall_on_synthetic():
    df = clean_logs(generate_traffic())
    res = LogAnomalyDetector(contamination=0.06).train_and_predict(extract_features(df))
    caught = (res["is_anomaly"] & df["is_attack"]).sum() / df["is_attack"].sum()
    assert caught > 0.7
    assert res["anomaly_score"].between(0, 1).all()


def test_brute_force_mask():
    import pandas as pd
    df = pd.DataFrame({"ip": ["1.1.1.1"] * 3 + ["2.2.2.2"], "request_path": ["/login"] * 4, "status_code": [401, 401, 403, 200], "response_size": [1] * 4})
    assert brute_force_mask(df).tolist() == [True, True, True, False]
