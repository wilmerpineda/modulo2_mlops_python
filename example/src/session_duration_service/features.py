TARGET_COLUMN = "session_minutes"
NUMERIC_FEATURES = [
    "historical_avg_session_minutes",
    "historical_sessions_last_7d",
    "days_since_last_session",
    "hour_of_day",
    "day_of_week",
    "push_received_last_24h",
]
CATEGORICAL_FEATURES = ["segment", "device_os", "site", "entry_point"]
FEATURE_COLUMNS = NUMERIC_FEATURES + CATEGORICAL_FEATURES
