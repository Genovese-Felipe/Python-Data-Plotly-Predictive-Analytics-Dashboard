import dash
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
import joblib
import numpy as np

# Carregar dados e modelo
df_iris = pd.read_csv("iris.csv")
model = joblib.load("models/logistic_regression_model.pkl")
scaler = joblib.load("models/scaler.pkl")

def create_layout():
    return html.Div([
        html.H1("Dashboard de Análise Preditiva - Iris Dataset", 
                style={'textAlign': 'center', 'marginBottom': 30}),
        
        html.Div([
            html.Div([
                html.H3("Visualizações Exploratórias"),
                dcc.Graph(
                    id='scatter-plot',
                    figure=px.scatter(df_iris, x="sepal length (cm)", y="sepal width (cm)", 
                                    color="target_names", title="Comprimento vs Largura da Sépala")
                ),
                dcc.Graph(
                    id='histogram',
                    figure=px.histogram(df_iris, x="petal length (cm)", color="target_names",
                                      title="Distribuição do Comprimento da Pétala")
                )
            ], style={'width': '48%', 'display': 'inline-block'}),
            
            html.Div([
                html.H3("Predição Interativa"),
                html.Label("Comprimento da Sépala (cm):"),
                dcc.Slider(
                    id='sepal-length-slider',
                    min=df_iris['sepal length (cm)'].min(),
                    max=df_iris['sepal length (cm)'].max(),
                    value=df_iris['sepal length (cm)'].mean(),
                    marks={i: str(i) for i in range(int(df_iris['sepal length (cm)'].min()), 
                                                   int(df_iris['sepal length (cm)'].max()) + 1)},
                    step=0.1
                ),
                
                html.Label("Largura da Sépala (cm):"),
                dcc.Slider(
                    id='sepal-width-slider',
                    min=df_iris['sepal width (cm)'].min(),
                    max=df_iris['sepal width (cm)'].max(),
                    value=df_iris['sepal width (cm)'].mean(),
                    marks={i: str(i) for i in range(int(df_iris['sepal width (cm)'].min()), 
                                                   int(df_iris['sepal width (cm)'].max()) + 1)},
                    step=0.1
                ),
                
                html.Label("Comprimento da Pétala (cm):"),
                dcc.Slider(
                    id='petal-length-slider',
                    min=df_iris['petal length (cm)'].min(),
                    max=df_iris['petal length (cm)'].max(),
                    value=df_iris['petal length (cm)'].mean(),
                    marks={i: str(i) for i in range(int(df_iris['petal length (cm)'].min()), 
                                                   int(df_iris['petal length (cm)'].max()) + 1)},
                    step=0.1
                ),
                
                html.Label("Largura da Pétala (cm):"),
                dcc.Slider(
                    id='petal-width-slider',
                    min=df_iris['petal width (cm)'].min(),
                    max=df_iris['petal width (cm)'].max(),
                    value=df_iris['petal width (cm)'].mean(),
                    marks={i: str(i) for i in range(int(df_iris['petal width (cm)'].min()), 
                                                   int(df_iris['petal width (cm)'].max()) + 1)},
                    step=0.1
                ),
                
                html.Div(id='prediction-output', style={'marginTop': 20, 'fontSize': 18})
            ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
        ])
    ])

@callback(
    Output('prediction-output', 'children'),
    [Input('sepal-length-slider', 'value'),
     Input('sepal-width-slider', 'value'),
     Input('petal-length-slider', 'value'),
     Input('petal-width-slider', 'value')]
)
def update_prediction(sepal_length, sepal_width, petal_length, petal_width):
    # Preparar dados para predição
    features = np.array([[sepal_length, sepal_width, petal_length, petal_width]])
    features_scaled = scaler.transform(features)
    
    # Fazer predição
    prediction = model.predict(features_scaled)[0]
    probability = model.predict_proba(features_scaled)[0]
    
    species_names = ['setosa', 'versicolor', 'virginica']
    predicted_species = species_names[prediction]
    confidence = max(probability) * 100
    
    return html.Div([
        html.H4(f"Predição: {predicted_species}"),
        html.P(f"Confiança: {confidence:.1f}%"),
        html.P(f"Probabilidades:"),
        html.Ul([
            html.Li(f"Setosa: {probability[0]:.3f}"),
            html.Li(f"Versicolor: {probability[1]:.3f}"),
            html.Li(f"Virginica: {probability[2]:.3f}")
        ])
    ])

