import joblib
import numpy as np

# Load trained model
model = joblib.load("models/peer_score_model.pkl")


def predict_score(peer):
    features = np.array([[
        peer["upload_rate"],
        peer["reliability"],
        peer["availability"],
        peer["latency"]
    ]])

    return model.predict(features)[0]


def select_best_peer(peers, self_id):
    scored_peers = []

    for pid, info in peers.items():
        if pid == self_id:
            continue

        # 🔥 Simulated metrics (IMPORTANT)
        peer_features = {
            "upload_rate": np.random.uniform(50, 200),
            "reliability": np.random.uniform(0.5, 1.0),
            "availability": np.random.uniform(0.5, 1.0),
            "latency": np.random.uniform(10, 100)
        }

        score = predict_score(peer_features)

        scored_peers.append((pid, info, score))

    if not scored_peers:
        return None

    # Pick best
    best = max(scored_peers, key=lambda x: x[2])

    print(f"Selected peer {best[0]} with score {best[2]:.2f}")

    return best[0], best[1]
