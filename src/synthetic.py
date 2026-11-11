import numpy as np
import pandas as pd

NORMAL = ["/", "/index.html", "/about", "/docs", "/api/products", "/api/v1/user/profile",
          "/static/css/style.css", "/images/logo.png", "/dashboard", "/contact"]
ATTACKS = ["/api/login?user=admin' OR '1'='1", "/../../../etc/passwd", "/search?q=<script>alert(1)</script>",
           "/product?id=1 UNION SELECT username,password FROM users--", "/.env", "/wp-login.php"]


def generate_traffic(n: int = 600, attack_ratio: float = 0.04, seed: int = 7) -> pd.DataFrame:
    """Mixed normal + attack traffic with a ground-truth `is_attack` column for evaluation."""
    rng = np.random.default_rng(seed)
    rows = []
    for _ in range(n):
        if rng.random() < attack_ratio:
            bad = rng.random() < 0.5
            rows.append({"ip": f"10.0.0.{rng.integers(80, 90)}", "request_path": str(rng.choice(ATTACKS)),
                         "status_code": int(rng.choice([401, 403, 500])), "response_size": int(rng.integers(5000, 16000)),
                         "is_attack": True})
        else:
            rows.append({"ip": f"192.168.1.{rng.integers(2, 60)}", "request_path": str(rng.choice(NORMAL)),
                         "status_code": int(rng.choice([200, 200, 200, 304, 404])), "response_size": int(rng.integers(300, 2500)),
                         "is_attack": False})
    return pd.DataFrame(rows)
