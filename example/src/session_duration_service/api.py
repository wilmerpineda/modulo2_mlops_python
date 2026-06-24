import json
import os
from functools import lru_cache
from pathlib import Path
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from session_duration_service.features import FEATURE_COLUMNS
from session_duration_service.schemas import BatchPredictionRequest, BatchPredictionResponse, PredictionRequest, PredictionResponse

MODEL_PATH = Path(os.getenv("MODEL_PATH", "artifacts/model.joblib"))
METADATA_PATH = Path(os.getenv("MODEL_METADATA_PATH", "artifacts/model_metadata.json"))
app = FastAPI(title="Session Duration Prediction API", version="0.1.0")


@lru_cache(maxsize=1)
def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model not found at {MODEL_PATH}")
    return joblib.load(MODEL_PATH)


@lru_cache(maxsize=1)
def load_metadata() -> dict:
    if not METADATA_PATH.exists():
        return {}
    return json.loads(METADATA_PATH.read_text(encoding="utf-8"))


def to_frame(items: list[PredictionRequest]) -> pd.DataFrame:
    return pd.DataFrame([item.model_dump() for item in items])[FEATURE_COLUMNS]


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Session Duration API is running"}


@app.get("/health")
def health() -> dict[str, str]:
    try:
        load_model()
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    return {"status": "ok"}


@app.get("/model/metadata")
def model_metadata() -> dict:
    return load_metadata()


@app.post("/predict", response_model=PredictionResponse)
def predict(payload: PredictionRequest) -> PredictionResponse:
    model = load_model()
    prediction = float(model.predict(to_frame([payload]))[0])
    return PredictionResponse(session_minutes=round(prediction, 2), model_type=load_metadata().get("model_type"))


@app.post("/predict/batch", response_model=BatchPredictionResponse)
def predict_batch(payload: BatchPredictionRequest) -> BatchPredictionResponse:
    model = load_model()
    predictions = model.predict(to_frame(payload.items))
    model_type = load_metadata().get("model_type")
    return BatchPredictionResponse(predictions=[PredictionResponse(session_minutes=round(float(value), 2), model_type=model_type) for value in predictions])
