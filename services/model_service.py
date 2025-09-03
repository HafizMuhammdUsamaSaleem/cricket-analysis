import io
import os
import time
import logging
import joblib
import pandas as pd
from fastapi import UploadFile, HTTPException
from services.utils import clean_columns, validate_columns, filter_rows

RESULTS_DIR = "outputs"
MODELS_DIR = "models"
MODEL_VERSION = "random_forest_v1"
MODEL_FILE = os.path.join(MODELS_DIR, f"{MODEL_VERSION}.pkl")

os.makedirs(RESULTS_DIR, exist_ok=True)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("t20-predictor")

try:
    model = joblib.load(MODEL_FILE)
except Exception as e:
    logger.error(f"Failed to load model: {e}")
    model = None

REQUIRED_COLUMNS = ["total_runs", "wickets", "target", "balls_left"]

async def process_csv_and_predict(file: UploadFile):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Please upload a CSV file")

    try:
        content = await file.read()
        df = pd.read_csv(io.BytesIO(content))
        df = clean_columns(df)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid CSV: {e}")

    total_rows = len(df)
    validate_columns(df, REQUIRED_COLUMNS)
    filtered = filter_rows(df)
    filtered_rows = len(filtered)

    if filtered_rows == 0:
        return {
            "status": "success",
            "predictions_file": None,
            "metadata": {
                "total_rows": total_rows,
                "filtered_rows": 0,
                "predictions_made": 0,
                "model_used": MODEL_VERSION
            }
        }

    try:
        X = filtered[["total_runs", "wickets", "target", "balls_left"]]
        preds = model.predict(X)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {e}")

    filtered["won"] = preds.astype(int)
    ts = time.strftime("%Y%m%d-%H%M")
    out_path = os.path.join(RESULTS_DIR, f"predictions_{ts}.csv")
    filtered.to_csv(out_path, index=False)

    return {
        "status": "success",
        "predictions_file": out_path,
        "metadata": {
            "total_rows": total_rows,
            "filtered_rows": filtered_rows,
            "predictions_made": len(filtered),
            "model_used": MODEL_VERSION
        }
    }
