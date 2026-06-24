from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    segment: str = Field(examples=["active"])
    historical_avg_session_minutes: float = Field(ge=0, examples=[18.5])
    historical_sessions_last_7d: int = Field(ge=0, examples=[5])
    days_since_last_session: int = Field(ge=0, examples=[2])
    hour_of_day: int = Field(ge=0, le=23, examples=[20])
    day_of_week: int = Field(ge=0, le=6, examples=[4])
    device_os: str = Field(examples=["android"])
    site: str = Field(examples=["product"])
    entry_point: str = Field(examples=["recommendation"])
    push_received_last_24h: int = Field(ge=0, le=1, examples=[1])


class PredictionResponse(BaseModel):
    session_minutes: float
    model_type: str | None = None


class BatchPredictionRequest(BaseModel):
    items: list[PredictionRequest]


class BatchPredictionResponse(BaseModel):
    predictions: list[PredictionResponse]
