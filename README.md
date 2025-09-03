# Cricket Analysis API

## Overview

This project is a T20 cricket chase prediction system built with FastAPI and a Random Forest& Logistic Regresson model.

**It provides three main capabilities:**

- [POST] /predict - Upload a CSV of match situations and get predictions.

- [POST] /explain/{prediction_id} - Generate human-readable explanations of predictions using Gemini (Google Generative AI).

- [GET] /health - Quick service + model version check.

**The system also includes:**

- Input validation & filtering logic.

- Null-row handling (drops rows with missing values).

- Logging and error handling.

- Automated testing with pytest.

- Modular project structure for clarity and scalability.

## Directory Structure

```
|   app.py
|   EDA.ipynb
|   README.md
|   requirements.txt
+---data
|       cricket_dataset.csv
|       cricket_dataset_clean.csv
|       cricket_dataset_test.csv
|
+---models
|       logreg_v1.pkl
|       random_forest_v1.pkl
|
+---notebooks
+---outputs
|       predictions_20250903-162451.csv
|       predictions_20250903-1628.csv
|
+---prompts
|   |   prompt.py
|
+---services
|   |   llm_service.py
|   |   model_service.py
|   |   utils.py
|
+---tests
|   |   test_integration.py

```

## Setup Instructions

1. Clone the Repository
```
git clone <repo_url>
cd cricket-analysis
```

2. Create Virtual Environment
```
python -m venv venv
```

3. Install Dependencies
```
pip install -r requirements.txt
```

4. Environment Variables

Create a .env file in the project root with:
```
GOOGLE_API_KEY=your_google_gemini_api_key
```

## Running the API

Start the server:

uvicorn app:app --reload


By default, it runs at:

```
http://127.0.0.1:8000
```

**API Docs**

```
Swagger UI → http://127.0.0.1:8000/docs

```

## API Usage
1. Predict Endpoint
```
curl -X POST "http://127.0.0.1:8000/predict" \
  -F "file=@sample.csv"
```

**Response Example**

```
{
  "status": "success",
  "predictions_file": "outputs/predictions_20250903-183211.csv",
  "metadata": {
    "total_rows": 150,
    "filtered_rows": 89,
    "predictions_made": 89,
    "model_used": "random_forest_v1"
  }
}
```
2. Explain Endpoint
```
curl -X POST "http://127.0.0.1:8000/explain/1?confidence=85"
```

**Response Example**

```
{
  "prediction": 1,
  "confidence": 85.0,
  "explanation": "The chasing team is in a strong position with wickets in hand and the required run rate under control. They will likely secure the win unless momentum shifts dramatically."
}
```

3. Health Check
```
curl http://127.0.0.1:8000/health
```

**Response Example**

```
{
  "status": "ok",
  "model_used": "random_forest_v1"
}
```

## Testing

Run a test file:

```
pytest tests/test_integration.py
```