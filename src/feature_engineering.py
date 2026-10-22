import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

def extract_features(df: pd.DataFrame):
    features = pd.DataFrame()
    features['response_size'] = df['response_size'].fillna(0)
    features['status_code'] = df['status_code'].fillna(200)
    
    vectorizer = TfidfVectorizer(max_features=10)
    tfidf_matrix = vectorizer.fit_transform(df['request_path'].astype(str)).toarray()
    
    tfidf_df = pd.DataFrame(tfidf_matrix, columns=[f"tfidf_{i}" for i in range(tfidf_matrix.shape[1])])
    
    X = pd.concat([features.reset_index(drop=True), tfidf_df.reset_index(drop=True)], axis=1)
    return X
