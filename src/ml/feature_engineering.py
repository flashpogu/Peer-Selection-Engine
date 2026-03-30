import pandas as pd


FEATURES = [
    "upload_rate",
    "reliability",
    "availability",
    "latency"
]

TARGET = "score"


def load_dataset(csv_path):
    df = pd.read_csv(csv_path)

    X = df[FEATURES]
    y = df[TARGET]

    return X, y
