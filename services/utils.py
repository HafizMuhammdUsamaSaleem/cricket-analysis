from fastapi import HTTPException

def clean_columns(df):
    df.columns = [c.strip().lower() for c in df.columns]
    return df

def validate_columns(df, required):
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise HTTPException(status_code=400, detail=f"Missing required columns: {missing}")

def filter_rows(df):
    return df[(df["balls_left"] < 60) & (df["target"] > 120)]
