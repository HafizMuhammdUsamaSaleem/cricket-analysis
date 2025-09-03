import io
import os
import pytest
import pandas as pd
from fastapi.testclient import TestClient
import app as app_module
app = app_module.app


client = TestClient(app)

def make_csv_bytes(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8")

def test_predict_endpoint_creates_predictions_file(tmp_path):
    df = pd.DataFrame({
        "total_runs": [100, 120],
        "wickets":    [2,   5],
        "target":     [150, 160],
        "balls_left": [50,  40],
        "won":        [0,   0]
    })

    csv_bytes = make_csv_bytes(df)

    response = client.post(
        "/predict",
        files={"file": ("sample.csv", io.BytesIO(csv_bytes), "text/csv")}
    )

    assert response.status_code == 200, f"Bad status: {response.status_code} {response.text}"
    payload = response.json()
    assert payload["status"] == "success"
    assert "metadata" in payload
    meta = payload["metadata"]
    assert meta["total_rows"] == 2
    assert meta["predictions_made"] <= meta["total_rows"]
    pred_path = payload.get("predictions_file")
    if pred_path:
        assert os.path.exists(pred_path), f"Predictions file not found: {pred_path}"
