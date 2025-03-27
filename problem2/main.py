import re
import pickle
import numpy as np
import pandas as pd
from typing import List, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix

# Loading the cleaned dataset
cleaned_file_path = "D:/Project Files/GOML-ML-ASSIGNMENT/data/AirlineReviews_Cleaned.csv" # Located inside 'data' folder
df = pd.read_csv(cleaned_file_path)

# Converting 'Recommended' (1 = positive, 0 = negative)
df["label"] = df["Recommended"].map({1: "positive", 0: "negative"})

def preprocess_text(text: str) -> str:
    """ Cleans and preprocesses input text. """
    if not isinstance(text, str):  # Converting non-string values to empty string
        return ""
    text = text.lower()
    text = re.sub(r'\W+', ' ', text)  # Removing special characters
    return text.strip()


def train_sentiment_model(df: pd.DataFrame) -> Pipeline:
    """ Trains a Logistic Regression model for sentiment classification. """
    df["Review"] = df["Review"].apply(preprocess_text)
    
    X_train, X_test, y_train, y_test = train_test_split(df["Review"], df["label"], test_size=0.2, random_state=42)
    
    model = Pipeline([
        ("tfidf", TfidfVectorizer()),
        ("classifier", LogisticRegression(max_iter=200))
    ])
    
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    print("Model Accuracy:", accuracy_score(y_test, y_pred))
    print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
    
    with open("sentiment_model.pkl", "wb") as f:
        pickle.dump(model, f)
    
    return model

def predict_sentiment(model: Pipeline, new_text: str) -> str:
    """ Predicts sentiment of new input text. """
    return model.predict([preprocess_text(new_text)])[0]


if __name__ == "__main__":
    trained_model = train_sentiment_model(df)
    
    print(predict_sentiment(trained_model, "I love to travel India in this airway"))
    print(predict_sentiment(trained_model, "Worst airline experience ever"))
