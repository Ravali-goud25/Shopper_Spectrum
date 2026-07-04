import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Segment Predictor",
    layout="wide"
)

# ==================================================
# LOAD MODELS
# ==================================================

kmeans = joblib.load(
    "../models/kmeans_model.pkl"
)

scaler = joblib.load(
    "../models/scaler.pkl"
)

segments_df = pd.read_csv(
    "../data/customer_segments.csv"
)

# ==================================================
# CLUSTER → SEGMENT MAPPING
# ==================================================

cluster_mapping = (
    segments_df[
        ["Cluster", "Segment"]
    ]
    .drop_duplicates()
)

cluster_to_segment = dict(
    zip(
        cluster_mapping["Cluster"],
        cluster_mapping["Segment"]
    )
)

# ==================================================
# PAGE HEADER
# ==================================================

st.title(
    "🤖 AI Customer Segment Predictor"
)

st.markdown(
    """
    Enter Recency, Frequency and Monetary values to predict the customer segment instantly.
    """
)

st.divider()

# ==================================================
# LAYOUT
# ==================================================

left_col, right_col = st.columns(
    [1.1, 1]
)

# ==================================================
# LEFT PANEL
# ==================================================

with left_col:

    st.subheader(
        "📥 Enter Customer RFM Values"
    )

    recency = st.number_input(
        "📅 Recency (Days Since Last Purchase)",
        min_value=0,
        value=30
    )

    frequency = st.number_input(
        "🔄 Frequency (Number Of Orders)",
        min_value=1,
        value=5
    )

    monetary = st.number_input(
        "💰 Monetary (Total Spend)",
        min_value=0.0,
        value=1000.0
    )

    predict_button = st.button(
        "🚀 Predict Customer Segment",
        use_container_width=True
    )

# ==================================================
# RIGHT PANEL
# ==================================================

with right_col:

    st.subheader(
        "📊 Prediction Result"
    )

    placeholder = st.empty()

# ==================================================
# PREDICTION
# ==================================================

if predict_button:

    scaled_input = scaler.transform(
        [[
            recency,
            frequency,
            monetary
        ]]
    )

    predicted_cluster = int(
        kmeans.predict(
            scaled_input
        )[0]
    )

    predicted_segment = (
        cluster_to_segment.get(
            predicted_cluster,
            "Unknown Segment"
        )
    )

    # ===============================================
    # HEALTH SCORE
    # ===============================================

    recency_score = max(
        0,
        100 - min(recency, 100)
    )

    frequency_score = min(
        frequency * 5,
        100
    )

    monetary_score = min(
        monetary / 100,
        100
    )

    health_score = int(
        (
            recency_score +
            frequency_score +
            monetary_score
        ) / 3
    )

    # ===============================================
    # RECOMMENDATIONS
    # ===============================================

    recommendation_dict = {

        "Champions":
        "Reward with VIP programs, early access offers and premium benefits.",

        "Loyal Customers":
        "Upsell premium products and increase basket size.",

        "Regular Customers":
        "Increase engagement using personalized promotions and discounts.",

        "Lost Customers":
        "Run win-back campaigns and reactivation offers."
    }

    recommendation = (
        recommendation_dict.get(
            predicted_segment,
            "No recommendation available."
        )
    )

    # ===============================================
    # GAUGE CHART
    # ===============================================

    gauge = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=health_score,
            title={
                "text":
                "Customer Health Score"
            },
            gauge={
                "axis":
                {"range": [0, 100]},

                "bar":
                {"thickness": 0.3},

                "steps": [

                    {
                        "range": [0, 40],
                        "color": "red"
                    },

                    {
                        "range": [40, 70],
                        "color": "orange"
                    },

                    {
                        "range": [70, 100],
                        "color": "green"
                    }
                ]
            }
        )
    )

    # ===============================================
    # RESULT PANEL
    # ===============================================

    with placeholder.container():

        st.success(
            f"Predicted Segment: {predicted_segment}"
        )

        st.plotly_chart(
            gauge,
            use_container_width=True
        )

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Cluster",
                predicted_cluster
            )

        with col2:

            st.metric(
                "Health Score",
                f"{health_score}/100"
            )

        st.subheader(
            "📌 Recommended Action"
        )

        st.info(
            recommendation
        )

# ==================================================
# INPUT SUMMARY
# ==================================================

        st.subheader(
            "📋 Input Summary"
        )

        summary_df = pd.DataFrame({

            "Metric": [
                "Recency",
                "Frequency",
                "Monetary"
            ],

            "Value": [
                recency,
                frequency,
                monetary
            ]
        })

        st.dataframe(
            summary_df,
            use_container_width=True
        )

# ==================================================
# REFERENCE GUIDE
# ==================================================

st.divider()

st.subheader(
    "📖 RFM Reference Guide"
)

guide1, guide2, guide3 = st.columns(3)

with guide1:

    st.info(
        """
        📅 Recency

        Lower value is better.

        Measures how recently the customer purchased.
        """
    )

with guide2:

    st.info(
        """
        🔄 Frequency

        Higher value is better.

        Measures purchase count.
        """
    )

with guide3:

    st.info(
        """
        💰 Monetary

        Higher value is better.

        Measures total spending.
        """
    )

# ==================================================
# SAMPLE CUSTOMERS
# ==================================================

st.divider()

st.subheader(
    "🧪 Example Inputs"
)

sample_df = pd.DataFrame({

    "Segment": [
        "Champions",
        "Loyal Customers",
        "Regular Customers",
        "Lost Customers"
    ],

    "Recency": [
        5,
        20,
        60,
        300
    ],

    "Frequency": [
        50,
        20,
        5,
        1
    ],

    "Monetary": [
        5000,
        2500,
        1000,
        100
    ]
})

st.dataframe(
    sample_df,
    use_container_width=True
)