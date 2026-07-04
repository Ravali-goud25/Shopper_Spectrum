import joblib

similarity_df = joblib.load(
    "../models/similarity_matrix.pkl"
)

def get_recommendations(
    product_name,
    top_n=5
):

    product_name = product_name.upper()

    if product_name not in similarity_df.columns:
        return None

    recommendations = (
        similarity_df[product_name]
        .sort_values(
            ascending=False
        )
        .iloc[1:top_n+1]
    )

    return recommendations