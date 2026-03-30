import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from src.ml.feature_engineering import load_dataset


MODEL_PATH = "models/peer_score_model.pkl"


def train():
    X, y = load_dataset("data/raw/swarm_logs.csv")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42
    )

    model.fit(X_train, y_train)

    score = model.score(X_test, y_test)
    print(f"Model R² score: {score:.4f}")

    joblib.dump(model, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")


if __name__ == "__main__":
    train()
