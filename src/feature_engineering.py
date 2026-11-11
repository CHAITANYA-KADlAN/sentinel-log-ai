import math
import re

import numpy as np
import pandas as pd

SIGNATURES = {
    "SQL injection": re.compile(r"('|%27|--|;|\bunion\b|\bselect\b|\bor\b\s*['\d]|1=1)", re.I),
    "Path traversal": re.compile(r"(\.\./|%2e%2e|/etc/(passwd|shadow)|\\\.\.\\)", re.I),
    "XSS": re.compile(r"(<script|%3cscript|onerror=|javascript:)", re.I),
    "Recon / probing": re.compile(r"(wp-login|wp-admin|phpmyadmin|\.env|\.git/|xmlrpc)", re.I),
}
REQUIRED = ["ip", "request_path", "status_code", "response_size"]


def clean_logs(df: pd.DataFrame) -> pd.DataFrame:
    """Coerce types and drop unusable rows without mutating the input."""
    out = df.copy()
    out["request_path"] = out["request_path"].astype(str)
    out["status_code"] = pd.to_numeric(out["status_code"], errors="coerce").fillna(200).astype(int)
    out["response_size"] = pd.to_numeric(out["response_size"], errors="coerce").fillna(0).astype(int)
    return out.reset_index(drop=True)


def find_signatures(path: str) -> list:
    return [name for name, rx in SIGNATURES.items() if rx.search(path)]


def _entropy(s: str) -> float:
    if not s:
        return 0.0
    return -sum((s.count(c) / len(s)) * math.log2(s.count(c) / len(s)) for c in set(s))


def extract_features(df: pd.DataFrame) -> pd.DataFrame:
    """Numeric features: payload shape, path anomalies, and per-IP behaviour."""
    paths = df["request_path"]
    X = pd.DataFrame(index=df.index)
    X["log_size"] = np.log1p(df["response_size"])
    X["status_class"] = df["status_code"] // 100
    X["path_len"] = paths.str.len()
    X["path_entropy"] = paths.map(_entropy)
    X["special_chars"] = paths.str.count(r"[^A-Za-z0-9/_.\-]")
    X["pct_encoded"] = paths.str.count("%")
    for name in SIGNATURES:
        X["sig_" + name.split()[0].lower()] = paths.map(lambda p, n=name: int(bool(SIGNATURES[n].search(p))))
    grp = df.assign(_err=(df["status_code"] >= 400).astype(int)).groupby("ip")
    X["ip_requests"] = grp["ip"].transform("size")
    X["ip_error_ratio"] = grp["_err"].transform("mean")
    X["ip_unique_paths"] = grp["request_path"].transform("nunique")
    return X
