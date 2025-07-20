import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import joblib
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.data_preprocessing import preprocess_data

def train_predictive_model(df):
    X_train, X_test, y_train, y_test, scaler = preprocess_data(df)

    model = LogisticRegression(max_iter=200)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)

    print(f"Acurácia do modelo: {accuracy}")
    print("Relatório de Classificação:\n", report)

    joblib.dump(model, 'models/logistic_regression_model.pkl')
    joblib.dump(scaler, 'models/scaler.pkl')
    print("Modelo e scaler salvos em models/")
    return model, scaler

if __name__ == '__main__':
    df_iris = pd.read_csv("iris.csv")
    train_predictive_model(df_iris)


