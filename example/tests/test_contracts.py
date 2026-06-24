from session_duration_service.data import build_mock_sessions
from session_duration_service.evaluate import compute_metrics
from session_duration_service.features import FEATURE_COLUMNS, TARGET_COLUMN


def test_mock_dataset_contract() -> None:
    data = build_mock_sessions(n_samples=30, random_state=42, noise_std=3.0)
    assert set(FEATURE_COLUMNS + [TARGET_COLUMN]).issubset(data.columns)
    assert len(data) == 30
    assert data[TARGET_COLUMN].min() > 0


def test_metrics_contract() -> None:
    metrics = compute_metrics([10.0, 20.0, 30.0], [11.0, 19.0, 32.0])
    assert set(metrics) == {"mae", "rmse", "r2"}
