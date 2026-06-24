import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from session_duration_service.config import ensure_parent, load_params


def main() -> None:
    params = load_params()
    metrics = json.loads(Path("reports/metrics.json").read_text(encoding="utf-8"))
    threshold = float(params["promotion"]["max_rmse"])
    rmse = float(metrics["rmse"])
    if rmse > threshold:
        raise RuntimeError(f"Model rejected: rmse={rmse:.4f} is above max_rmse={threshold:.4f}")
    source = Path(params["promotion"]["candidate_model_path"])
    target = ensure_parent(params["promotion"]["production_model_path"])
    shutil.copy2(source, target)
    metadata = {
        "promoted_at": datetime.now(timezone.utc).isoformat(),
        "model_type": params["model"]["type"],
        "metric": "rmse",
        "rmse": rmse,
        "max_rmse": threshold,
        "model_path": str(target),
    }
    ensure_parent(params["promotion"]["metadata_path"]).write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    print(f"Model promoted to {target}.")


if __name__ == "__main__":
    main()
