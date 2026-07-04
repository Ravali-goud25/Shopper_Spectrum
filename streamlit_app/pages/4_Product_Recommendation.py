import streamlit as st
import pandas as pd
import plotly.express as px
import joblib

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Product Recommendation",
    layout="wide"
)

# =====================================================
# LOAD DATA
# =====================================================

similarity_df = joblib.load(
    "../models/similarity_matrix.pkl"
)

top_products = pd.read_csv(
    "../data/top_products.csv"
)

customer_products = pd.read_csv(
    "../data/customer_products.csv"
)

segment_products = pd.read_csv(
    "../data/segment_recommendations.csv"
)

country_products = pd.read_csv(
    "../data/country_recommendations.csv"
)

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title(
    "📦 Recommendation Engine"
)

st.sidebar.metric(
    "Products",
    len(similarity_df.columns)
)

st.sidebar.metric(
    "Customers",
    customer_products["CustomerID"].nunique()
)

st.sidebar.metric(
    "Countries",
    country_products["Country"].nunique()
)

# =====================================================
# HEADER
# =====================================================

st.title(
    "🛒 AI Product Recommendation System"
)

st.markdown(
    """
    Product Recommendation using Collaborative Filtering
    """
)

st.divider()

# =====================================================
# PRODUCT RECOMMENDATION
# =====================================================

st.subheader(
    "🔍 Product Recommendation"
)

st.caption(
    "Search a product and get similar product recommendations"
)

all_products = sorted(
    similarity_df.columns.tolist()
)

selected_product = st.selectbox(
    "Choose Product",
    options=all_products
)

if st.button(
    "🚀 Get Recommendations",
    use_container_width=True
):

    recommendations = (
        similarity_df[
            selected_product
        ]
        .sort_values(
            ascending=False
        )
        .iloc[1:6]
    )

    recommendation_df = pd.DataFrame(
        {
            "Recommended Product":
            recommendations.index,

            "Similarity Score":
            recommendations.values
        }
    )

    col1, col2 = st.columns(
        [1,1]
    )

    with col1:

        st.success(
            f"Recommendations for: {selected_product}"
        )

        st.dataframe(
            recommendation_df,
            use_container_width=True
        )

    with col2:

        fig = px.bar(
            recommendation_df,
            x="Similarity Score",
            y="Recommended Product",
            orientation="h",
            color="Similarity Score",
            title="Top Similar Products"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

st.divider()

# =====================================================
# CUSTOMER HISTORY
# =====================================================

st.subheader(
    "👤 Customer Purchase History"
)

customer_ids = sorted(
    customer_products[
        "CustomerID"
    ].unique()
)

customer_id = st.selectbox(
    "Select Customer",
    customer_ids
)

history = customer_products[
    customer_products[
        "CustomerID"
    ]
    ==
    customer_id
]

if len(history) > 0:

    col1, col2 = st.columns(
        [2,1]
    )

    with col1:

        st.dataframe(
            history
            .sort_values(
                "Quantity",
                ascending=False
            )
            .head(20),
            use_container_width=True
        )

    with col2:

        st.metric(
            "Products Purchased",
            history[
                "Description"
            ].nunique()
        )

        st.metric(
            "Total Quantity",
            int(
                history[
                    "Quantity"
                ].sum()
            )
        )

st.divider()

# =====================================================
# SEGMENT RECOMMENDATIONS
# =====================================================

st.subheader(
    "👥 Segment Based Recommendations"
)

segments = sorted(
    segment_products[
        "Segment"
    ].unique()
)

selected_segment = st.selectbox(
    "Select Customer Segment",
    segments
)

segment_df = (
    segment_products[
        segment_products[
            "Segment"
        ]
        ==
        selected_segment
    ]
    .sort_values(
        "Quantity",
        ascending=False
    )
    .head(10)
)

col1, col2 = st.columns(
    [1,1]
)

with col1:

    st.dataframe(
        segment_df,
        use_container_width=True
    )

with col2:

    fig = px.bar(
        segment_df,
        x="Quantity",
        y="Description",
        orientation="h",
        title=f"Top Products for {selected_segment}"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# =====================================================
# COUNTRY RECOMMENDATIONS
# =====================================================

st.subheader(
    "🌍 Country Based Recommendations"
)

countries = sorted(
    country_products[
        "Country"
    ].unique()
)

selected_country = st.selectbox(
    "Select Country",
    countries
)

country_df = (
    country_products[
        country_products[
            "Country"
        ]
        ==
        selected_country
    ]
    .sort_values(
        "Quantity",
        ascending=False
    )
    .head(10)
)

col1, col2 = st.columns(
    [1,1]
)

with col1:

    st.dataframe(
        country_df,
        use_container_width=True
    )

with col2:

    fig = px.bar(
        country_df,
        x="Quantity",
        y="Description",
        orientation="h",
        title=f"Top Products in {selected_country}"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# =====================================================
# TOP PRODUCTS
# =====================================================

st.subheader(
    "🏆 Top Selling Products"
)

top10 = (
    top_products
    .sort_values(
        "Quantity",
        ascending=False
    )
    .head(10)
)

col1, col2 = st.columns(
    [1,1]
)

with col1:

    st.dataframe(
        top10,
        use_container_width=True
    )

with col2:

    fig = px.bar(
        top10,
        x="Quantity",
        y=top10.index,
        orientation="h",
        title="Top Selling Products"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# =====================================================
# PROJECT SUMMARY
# =====================================================

st.subheader(
    "📊 Dataset Summary"
)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Products",
        len(similarity_df.columns)
    )

with c2:
    st.metric(
        "Customers",
        customer_products["CustomerID"].nunique()
    )

with c3:
    st.metric(
        "Countries",
        country_products["Country"].nunique()
    )

with c4:
    st.metric(
        "Transactions",
        len(customer_products)
    )