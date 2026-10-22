import pandas as pd
from sklearn.ensemble import IsolationForest

class LogAnomalyDetector:
    def __init__(self, contamination=0.05):
        self.model = IsolationForest(contamination=contamination, random_state=42)

    def train_and_predict(self, X: pd.DataFrame) -> pd.DataFrame:
        self.model.fit(X)
        scores = self.model.decision_function(X)
        predictions = self.model.predict(X)
        
        results = X.copy()
        results['anomaly_score'] = -scores 
        results['is_anomaly'] = predictions == -1
        return results
