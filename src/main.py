import argparse
from pathlib import Path

import joblib
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


def train_model(output_path: Path) -> float:
    iris = load_iris()
    X_train, X_test, y_train, y_test = train_test_split(
        iris.data, iris.target, test_size=0.2, random_state=42
    )

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, output_path)
    return accuracy_score(y_test, model.predict(X_test))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Train and save an Iris classifier.")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("/app/artifacts/iris_model.joblib"),
        help="Path where the trained model will be saved.",
    )
    args = parser.parse_args()

    accuracy = train_model(args.output)
    print(f"Model training successful. Test accuracy: {accuracy:.2f}")
    print(f"Model saved to: {args.output}")