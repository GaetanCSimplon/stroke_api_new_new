import pandas as pd

def load_data():
    df = pd.read_csv("df_final_test.csv")
    if "Unnamed: 0" in df.columns:
        df = df.drop(columns=["Unnamed: 0"])
    return df
