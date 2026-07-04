import streamlit as st
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DATA_DIR = BASE_DIR / "data"

MODELS_DIR = BASE_DIR / "models"

st.set_page_config(
    page_title="Shopper Spectrum",
    page_icon="🛒",
    layout="wide"
)


@st.cache_data
def load_data():
    return pd.read_csv(
    DATA_DIR / "cleaned_online_retail.csv"
)

df = load_data()

total_revenue = df["Revenue"].sum()

total_orders = df["InvoiceNo"].nunique()

total_customers = df["CustomerID"].nunique()

total_products = df["Description"].nunique()

countries = df["Country"].nunique()

st.title("🛒 Shopper Spectrum")

st.markdown(
"""
Customer Analytics &
Product Recommendation System
"""
)

col1,col2,col3,col4,col5 = st.columns(5)

with col1:
    st.metric(
        "Revenue",
        f"${total_revenue:,.0f}"
    )

with col2:
    st.metric(
        "Orders",
        f"{total_orders:,}"
    )

with col3:
    st.metric(
        "Customers",
        f"{total_customers:,}"
    )

with col4:
    st.metric(
        "Products",
        f"{total_products:,}"
    )

with col5:
    st.metric(
        "Countries",
        f"{countries}"
    )

st.divider()

st.subheader("Project Overview")

st.write(
"""
This application analyzes customer purchasing behavior using:

• Exploratory Data Analysis

• RFM Analysis

• Customer Segmentation

• Product Recommendation

Use the left sidebar to navigate.
"""
)