import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from session_duration_service.config import ensure_parent, load_params
from session_duration_service.features import CATEGORICAL_FEATURES, FEATURE_COLUMNS, NUMERIC_FEATURES, TARGET_COLUMN


def build_pipeline(model_params: dict) -> Pipeline:
    numeric_pipeline = Pipeline([("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())])
    categorical_pipeline = Pipeline([("imputer", SimpleImputer(strategy="most_frequent")), ("encoder", OneHotEncoder(handle_unknown="ignore"))])
    preprocessor = ColumnTransformer([("numeric", numeric_pipeline, NUMERIC_FEATURES), ("categorical", categorical_pipeline, CATEGORICAL_FEATURES)])
    if model_params["type"] == "linear_regression":
        regressor = LinearRegression()
    elif model_params["type"] == "random_forest":
        regressor = RandomForestRegressor(n_estimators=int(model_params["n_estimators"]), max_depth=int(model_params["max_depth"]), random_state=int(model_params["random_state"]), n_jobs=-1)
    else:
        raise ValueError(f"Unsupported model type: {model_params['type']}")
    return Pipeline([("preprocessor", preprocessor), ("regressor", regressor)])


def main() -> None:
    params = load_params()
    train_data = pd.read_csv(params["data"]["train_path"])
    pipeline = build_pipeline(params["model"])
    pipeline.fit(train_data[FEATURE_COLUMNS], train_data[TARGET_COLUMN])
    output_path = ensure_parent(params["promotion"]["candidate_model_path"])
    joblib.dump(pipeline, output_path)
    print(f"Candidate model saved to {output_path}.")


if __name__ == "__main__":
    main()
