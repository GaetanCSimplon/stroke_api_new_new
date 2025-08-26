import pandas as pd

def load_data():
    """Load data from a csv

    Returns:
        df: Creates a dataframe out of the csv
    """
    df = pd.read_csv("df_final_test.csv")
    if "Unnamed: 0" in df.columns:
        df = df.drop(columns=["Unnamed: 0"])
    return df
