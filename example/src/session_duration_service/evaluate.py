import json
import joblib
import pandas as pd
from sklearn.metrics import mean_absolute_error, r2_score, root_mean_squared_error
from session_duration_service.config import ensure_parent, load_params
from session_duration_service.features import FEATURE_COLUMNS, TARGET_COLUMN


def compute_metrics(y_true, predictions) -> dict[str, float]:
    return {
        "mae": float(mean_absolute_error(y_true, predictions)),
        "rmse": float(root_mean_squared_error(y_true, predictions)),
        "r2": float(r2_score(y_true, predictions)),
    }


def main() -> None:
    params = load_params()
    model = joblib.load(params["promotion"]["candidate_model_path"])
    test_data = pd.read_csv(params["data"]["test_path"])
    predictions = model.predict(test_data[FEATURE_COLUMNS])
    metrics = compute_metrics(test_data[TARGET_COLUMN], predictions)
    ensure_parent("reports/metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    pd.DataFrame({"actual": test_data[TARGET_COLUMN], "prediction": predictions}).to_csv(ensure_parent("reports/predictions.csv"), index=False)
    print(f"Metrics: {metrics}")


if __name__ == "__main__":
    main()
