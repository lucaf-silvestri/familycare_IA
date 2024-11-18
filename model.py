import pickle
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
from sklearn.naive_bayes import MultinomialNB

def load_model():
    with open('modelo.pkl', 'rb') as f:
        model, vectorizer = pickle.load(f)
    return model, vectorizer

def train_model():
    feedbacks = pd.read_csv('feedbacks.csv')
    X = feedbacks['feedback']
    y = feedbacks['classificacao']

    vectorizer = CountVectorizer()
    X_vectorized = vectorizer.fit_transform(X)

    model = MultinomialNB()
    model.fit(X_vectorized, y)

    with open('modelo.pkl', 'wb') as f:
        pickle.dump((model, vectorizer), f)
