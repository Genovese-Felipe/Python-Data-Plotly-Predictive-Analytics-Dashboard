from sklearn.datasets import load_iris
import pandas as pd

def load_iris_dataset():
    iris = load_iris()
    df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
    df['target'] = iris.target
    df['target_names'] = df['target'].apply(lambda x: iris.target_names[x])
    return df

if __name__ == '__main__':
    df_iris = load_iris_dataset()
    print(df_iris.head())
    df_iris.to_csv('iris.csv', index=False)
    print('Dataset Iris salvo em iris.csv')


