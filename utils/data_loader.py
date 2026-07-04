import pandas as pd

def load_segments():
    return pd.read_csv(
        "../data/customer_segments.csv"
    )

def load_cluster_profile():
    return pd.read_csv(
        "../data/cluster_profile.csv"
    )

def load_top_products():
    return pd.read_csv(
        "../data/top_products.csv"
    )