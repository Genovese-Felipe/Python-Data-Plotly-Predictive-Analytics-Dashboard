import pandas as pd
import plotly.express as px

def perform_eda(df):
    print("Informações do DataFrame:")
    df.info()
    print("\nEstatísticas Descritivas:")
    print(df.describe())
    print("\nContagem de valores para a coluna target_names:")
    print(df["target_names"].value_counts())

    # Visualizações
    fig_scatter = px.scatter(df, x="sepal length (cm)", y="sepal width (cm)", color="target_names",
                             title="Comprimento vs Largura da Sépala por Espécie")
    fig_scatter.write_html("assets/sepal_scatter.html")

    fig_hist = px.histogram(df, x="petal length (cm)", color="target_names",
                            title="Distribuição do Comprimento da Pétala por Espécie")
    fig_hist.write_html("assets/petal_hist.html")

    print("Análise exploratória concluída. Gráficos salvos em assets/")

if __name__ == '__main__':
    df_iris = pd.read_csv("iris.csv")
    perform_eda(df_iris)


