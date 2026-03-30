import matplotlib.pyplot as plt
import joblib
import pandas as pd

model = joblib.load("models/peer_score_model.pkl")

features = [
    "upload_rate",
    "reliability",
    "availability",
    "latency"
]

importances = model.feature_importances_

feature_importance_df = pd.DataFrame({
    "feature": features,
    "importance": importances
}).sort_values(by="importance", ascending=False)

print(feature_importance_df)


plt.bar(feature_importance_df["feature"],
        feature_importance_df["importance"])

plt.xlabel("Feature")
plt.ylabel("Importance")
plt.title("Feature Importance in ML-based Peer Scoring")
plt.show()
