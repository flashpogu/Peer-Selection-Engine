import joblib
import pandas as pd

MODEL_PATH = "models/peer_score_model.pkl"

model = joblib.load(MODEL_PATH)


def predict_peer_score(peer):
    data = pd.DataFrame([{
        "upload_rate": peer.upload_rate,
        "reliability": peer.reliability,
        "availability": peer.availability,
        "latency": peer.latency
    }])

    return model.predict(data)[0]
