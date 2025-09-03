from fastapi import FastAPI, UploadFile, File, HTTPException
from services.model_service import process_csv_and_predict
from services.llm_service import generate_explanation

app = FastAPI()

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    return await process_csv_and_predict(file)

@app.post("/explain/{prediction_id}")
async def explain(prediction_id: int, confidence: float = 50.0):
    if prediction_id not in [0, 1]:
        raise HTTPException(status_code=400, detail="Prediction must be 0 or 1")
    explanation = generate_explanation(prediction_id, confidence)
    return {
        "prediction": prediction_id,
        "confidence": confidence,
        "explanation": explanation
    }

@app.get("/health")
def health():
    return {"status": "ok", "model_used": "random_forest_v1"}
