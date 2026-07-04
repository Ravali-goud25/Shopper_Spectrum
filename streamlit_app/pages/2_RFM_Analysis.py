import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import DATA_DIR

st.set_page_config(
    page_title="RFM Analysis",
    layout="wide"
)

# ==================================
# LOAD DATA
# ==================================

rfm = pd.read_csv(
    DATA_DIR / "customer_segments.csv"
)

# ==================================
# PAGE TITLE
# ==================================

st.title("🎯 RFM Customer Analysis")
st.markdown(
    "Customer Segmentation using Recency, Frequency and Monetary Analysis"
)

st.divider()

# ==================================
# SIDEBAR FILTER
# ==================================

st.sidebar.header("Filters")

selected_segment = st.sidebar.selectbox(
    "Select Segment",
    ["All"] + sorted(rfm["Segment"].unique())
)

if selected_segment != "All":
    filtered_rfm = rfm[
        rfm["Segment"] == selected_segment
    ]
else:
    filtered_rfm = rfm.copy()

# ==================================
# KPI SECTION
# ==================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Customers",
        filtered_rfm["CustomerID"].nunique()
    )

with col2:
    st.metric(
        "Avg Recency",
        round(filtered_rfm["Recency"].mean(), 1)
    )

with col3:
    st.metric(
        "Avg Frequency",
        round(filtered_rfm["Frequency"].mean(), 1)
    )

with col4:
    st.metric(
        "Avg Monetary",
        f"${filtered_rfm['Monetary'].mean():,.0f}"
    )

st.divider()

# ==================================
# CUSTOMER LOOKUP
# ==================================

st.subheader("🔍 Customer Lookup")

customer_id = st.number_input(
    "Enter Customer ID",
    min_value=0,
    step=1
)

if customer_id:

    customer = filtered_rfm[
        filtered_rfm["CustomerID"] == customer_id
    ]

    if len(customer) > 0:

        st.success("Customer Found")

        st.dataframe(
            customer,
            use_container_width=True
        )

    else:

        st.error("Customer Not Found")

st.divider()

# ==================================
# TOP CUSTOMERS TABLE
# ==================================

st.subheader("🏆 Top Customers")

top_customers = (
    filtered_rfm
    .sort_values(
        "Monetary",
        ascending=False
    )
    .head(20)
)

st.dataframe(
    top_customers,
    use_container_width=True
)

st.divider()

# ==================================
# SEGMENT DISTRIBUTION
# ==================================

st.subheader("📊 Customer Segment Distribution")

segment_counts = (
    rfm["Segment"]
    .value_counts()
    .reset_index()
)

segment_counts.columns = [
    "Segment",
    "Customers"
]

fig = px.bar(
    segment_counts,
    x="Segment",
    y="Customers",
    color="Segment",
    text="Customers"
)

fig.update_layout(
    height=500
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==================================
# RECENCY ANALYSIS
# ==================================

st.subheader("⏳ Average Recency By Segment")

recency_chart = (
    rfm.groupby("Segment")["Recency"]
    .mean()
    .reset_index()
    .sort_values(
        "Recency",
        ascending=False
    )
)

fig = px.bar(
    recency_chart,
    x="Segment",
    y="Recency",
    color="Segment",
    text_auto=".2f"
)

fig.update_layout(
    height=500
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==================================
# FREQUENCY ANALYSIS
# ==================================

st.subheader("🔄 Average Frequency By Segment")

frequency_chart = (
    rfm.groupby("Segment")["Frequency"]
    .mean()
    .reset_index()
)

fig = px.bar(
    frequency_chart,
    x="Segment",
    y="Frequency",
    color="Segment",
    text_auto=".2f"
)

fig.update_layout(
    height=500
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==================================
# MONETARY ANALYSIS
# ==================================

st.subheader("💰 Average Monetary Value By Segment")

monetary_chart = (
    rfm.groupby("Segment")["Monetary"]
    .mean()
    .reset_index()
)

fig = px.bar(
    monetary_chart,
    x="Segment",
    y="Monetary",
    color="Segment",
    text_auto=".0f"
)

fig.update_layout(
    height=500
)

st.plotly_chart(
    fig,
    use_container_width=True
)