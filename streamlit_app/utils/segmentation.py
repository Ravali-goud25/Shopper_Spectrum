import joblib

kmeans = joblib.load(
    "../models/kmeans_model.pkl"
)

scaler = joblib.load(
    "../models/scaler.pkl"
)

def predict_segment(
    recency,
    frequency,
    monetary
):

    scaled = scaler.transform(
        [[
            recency,
            frequency,
            monetary
        ]]
    )

    cluster = kmeans.predict(
        scaled
    )[0]

    return cluster