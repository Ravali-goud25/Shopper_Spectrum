import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DATA_DIR = BASE_DIR / "data"

MODELS_DIR = BASE_DIR / "models"
st.set_page_config(
    page_title="EDA",
    layout="wide"
)

st.title("📊 Exploratory Data Analysis")

@st.cache_data
def load_data():
    df = pd.read_csv(
    DATA_DIR / "cleaned_online_retail.csv"
)

    df["InvoiceDate"] = pd.to_datetime(
        df["InvoiceDate"]
    )

    return df

df = load_data()

# ==========================
# Sidebar Filters
# ==========================

st.sidebar.header("Filters")

country = st.sidebar.selectbox(
    "Select Country",
    ["All"] + sorted(df["Country"].unique().tolist())
)

if country != "All":
    filtered_df = df[
        df["Country"] == country
    ]
else:
    filtered_df = df.copy()

# ==========================
# KPIs
# ==========================

total_revenue = filtered_df["Revenue"].sum()

total_orders = filtered_df["InvoiceNo"].nunique()

total_customers = filtered_df["CustomerID"].nunique()

col1,col2,col3 = st.columns(3)

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

st.divider()

# ==========================
# Top Countries
# ==========================

st.subheader("Top Countries By Revenue")

country_sales = (
    df.groupby("Country")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

fig = px.bar(
    x=country_sales.values,
    y=country_sales.index,
    orientation="h",
    labels={
        "x":"Revenue",
        "y":"Country"
    }
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================
# Top Products
# ==========================

st.subheader("Top Selling Products")

top_products = (
    filtered_df
    .groupby("Description")["Quantity"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

fig = px.bar(
    x=top_products.values,
    y=top_products.index,
    orientation="h",
    labels={
        "x":"Quantity Sold",
        "y":"Product"
    }
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================
# Monthly Revenue
# ==========================

st.subheader("Monthly Revenue Trend")

filtered_df["Month"] = (
    filtered_df["InvoiceDate"]
    .dt.to_period("M")
    .astype(str)
)

monthly_sales = (
    filtered_df
    .groupby("Month")["Revenue"]
    .sum()
    .reset_index()
)

fig = px.line(
    monthly_sales,
    x="Month",
    y="Revenue",
    markers=True
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================
# Revenue Distribution
# ==========================

st.subheader("Revenue Distribution")

fig = px.histogram(
    filtered_df,
    x="Revenue",
    nbins=50
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================
# Top Customers
# ==========================

st.subheader("Top Customers")

top_customers = (
    filtered_df
    .groupby("CustomerID")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

top_customers_df = pd.DataFrame({
    "CustomerID":top_customers.index,
    "Revenue":top_customers.values
})

st.dataframe(
    top_customers_df,
    use_container_width=True
)