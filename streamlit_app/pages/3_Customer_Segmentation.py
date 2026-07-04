import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import DATA_DIR

st.set_page_config(
    page_title="Customer Segmentation",
    layout="wide"
)

# ===================================
# LOAD DATA
# ===================================

segments = pd.read_csv(
    DATA_DIR / "customer_segments.csv"
)

# Create profile dynamically
profile = (
    segments
    .groupby("Segment")[["Recency", "Frequency", "Monetary"]]
    .mean()
    .reset_index()
)

# ===================================
# PAGE TITLE
# ===================================

st.title("👥 Customer Segmentation")

st.markdown(
    "Interactive Customer Segmentation Dashboard Using RFM Analysis"
)

st.divider()

# ===================================
# SIDEBAR FILTER
# ===================================

st.sidebar.header("Filters")

selected_segment = st.sidebar.selectbox(
    "Select Segment",
    ["All"] + sorted(
        segments["Segment"].unique()
    )
)

if selected_segment != "All":

    filtered_df = segments[
        segments["Segment"] == selected_segment
    ]

else:

    filtered_df = segments.copy()

# ===================================
# KPI CARDS
# ===================================

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Customers",
        filtered_df["CustomerID"].nunique()
    )

with col2:

    st.metric(
        "Avg Recency",
        round(
            filtered_df["Recency"].mean(),
            1
        )
    )

with col3:

    st.metric(
        "Avg Frequency",
        round(
            filtered_df["Frequency"].mean(),
            1
        )
    )

with col4:

    st.metric(
        "Avg Monetary",
        f"${filtered_df['Monetary'].mean():,.0f}"
    )

st.divider()

# ===================================
# CUSTOMER LOOKUP
# ===================================

st.subheader("🔍 Customer Lookup")

customer_id = st.number_input(
    "Enter Customer ID",
    min_value=0,
    step=1
)

if customer_id:

    customer = segments[
        segments["CustomerID"] == customer_id
    ]

    if len(customer) > 0:

        st.success("Customer Found")

        st.dataframe(
            customer,
            use_container_width=True
        )

    else:

        st.error(
            "Customer Not Found"
        )

st.divider()

# ===================================
# TOP CUSTOMERS
# ===================================

st.subheader("🏆 Top Customers")

top_customers = (
    filtered_df
    .sort_values(
        "Monetary",
        ascending=False
    )
    .head(10)
)

st.dataframe(
    top_customers[
        [
            "CustomerID",
            "Recency",
            "Frequency",
            "Monetary",
            "Segment"
        ]
    ],
    use_container_width=True
)

st.divider()

# ===================================
# SEGMENT DISTRIBUTION
# ===================================

st.subheader("📊 Segment Distribution")

segment_counts = (
    segments["Segment"]
    .value_counts()
    .reset_index()
)

segment_counts.columns = [
    "Segment",
    "Customers"
]

fig = px.pie(
    segment_counts,
    names="Segment",
    values="Customers",
    hole=0.4,
    title="Customer Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ===================================
# SEGMENT PROFILE TABLE
# ===================================

st.subheader("📋 Segment Profile")

st.dataframe(
    profile,
    use_container_width=True
)

st.divider()

# ===================================
# RECENCY COMPARISON
# ===================================

st.subheader("⏳ Recency Comparison")

fig = px.bar(
    profile,
    x="Segment",
    y="Recency",
    color="Segment",
    text_auto=".1f",
    title="Average Recency By Segment"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ===================================
# FREQUENCY COMPARISON
# ===================================

st.subheader("🔄 Frequency Comparison")

fig = px.bar(
    profile,
    x="Segment",
    y="Frequency",
    color="Segment",
    text_auto=".1f",
    title="Average Frequency By Segment"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ===================================
# MONETARY COMPARISON
# ===================================

st.subheader("💰 Monetary Comparison")

fig = px.bar(
    profile,
    x="Segment",
    y="Monetary",
    color="Segment",
    text_auto=".0f",
    title="Average Monetary By Segment"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ===================================
# RECENCY VS FREQUENCY
# ===================================

st.subheader("📈 Recency vs Frequency")

fig = px.scatter(
    filtered_df,
    x="Recency",
    y="Frequency",
    color="Segment",
    size="Monetary",
    hover_data=["CustomerID"]
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ===================================
# FREQUENCY VS MONETARY
# ===================================

st.subheader("💵 Frequency vs Monetary")

fig = px.scatter(
    filtered_df,
    x="Frequency",
    y="Monetary",
    color="Segment",
    size="Monetary",
    hover_data=["CustomerID"]
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ===================================
# CUSTOMER LIST
# ===================================

st.subheader("👤 Customers In Selected Segment")

st.dataframe(
    filtered_df[
        [
            "CustomerID",
            "Recency",
            "Frequency",
            "Monetary",
            "Segment"
        ]
    ],
    use_container_width=True
)

st.divider()

# ===================================
# BUSINESS RECOMMENDATIONS
# ===================================

st.subheader("📢 Business Recommendations")

recommendations = {

    "Champions":
    "Reward with loyalty programs, VIP benefits and early access offers.",

    "Loyal Customers":
    "Upsell premium products and increase basket size.",

    "Regular Customers":
    "Improve engagement using personalized promotions.",

    "Lost Customers":
    "Run win-back campaigns with discounts and reminders."
}

if selected_segment != "All":

    st.info(
        recommendations.get(
            selected_segment,
            "No recommendation available."
        )
    )

else:

    st.info(
        """
        Champions → Retain and reward

        Loyal Customers → Upsell

        Regular Customers → Increase engagement

        Lost Customers → Reactivate
        """
    )