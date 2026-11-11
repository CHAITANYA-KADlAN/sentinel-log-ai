import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler


class LogAnomalyDetector:
    """Unsupervised Isolation Forest over scaled log features."""

    def __init__(self, contamination: float = 0.05, n_estimators: int = 300):
        self.scaler = StandardScaler()
        self.model = IsolationForest(
            n_estimators=n_estimators, contamination=contamination, random_state=42
        )

    def train_and_predict(self, X: pd.DataFrame) -> pd.DataFrame:
        Z = self.scaler.fit_transform(X)
        self.model.fit(Z)
        raw = -self.model.decision_function(Z)  # higher = more anomalous
        span = raw.max() - raw.min()
        results = X.copy()
        results["anomaly_score"] = (raw - raw.min()) / span if span else 0.0  # 0..1
        results["is_anomaly"] = self.model.predict(Z) == -1
        return results


def severity(score: float) -> str:
    return "Critical" if score >= 0.8 else "High" if score >= 0.6 else "Medium" if score >= 0.4 else "Low"
