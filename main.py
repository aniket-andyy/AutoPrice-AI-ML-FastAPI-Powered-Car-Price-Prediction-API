import os
from pathlib import Path

import joblib
import pandas as pd
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# Load environment variables
load_dotenv()

# --------------------------------------------------
# FastAPI App
# --------------------------------------------------

app = FastAPI(
    title="AutoPrice AI",
    description="ML-powered Car Price Prediction API",
    version="1.0.0",
)

# --------------------------------------------------
# Model Configuration
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

# Change this ONLY if your model is stored somewhere else
MODEL_PATH = BASE_DIR / "model" / "car_price_model.pkl"

model = None
model_error = None

try:
    model = joblib.load(MODEL_PATH)
    print(f"Model loaded successfully from: {MODEL_PATH}")

except Exception as e:
    model_error = str(e)
    print(f"Model loading failed: {e}")


# --------------------------------------------------
# Request Schema
# --------------------------------------------------

class CarInput(BaseModel):
    Car_Name: str = Field(..., description="Car name")
    Year: int = Field(..., description="Manufacturing year")
    Present_Price: float = Field(..., description="Current showroom price in lakh")
    Kms_Driven: int = Field(..., description="Kilometers driven")
    Fuel_Type: str = Field(..., description="Petrol, Diesel or CNG")
    Seller_Type: str = Field(..., description="Dealer or Individual")
    Transmission: str = Field(..., description="Manual or Automatic")
    Owner: int = Field(..., description="Number of previous owners")


# --------------------------------------------------
# Root Endpoint
# --------------------------------------------------

@app.get("/")
def root():
    return {
        "message": "AutoPrice AI API is running",
        "status": "online",
        "version": "1.0.0",
    }


# --------------------------------------------------
# Health Check
# --------------------------------------------------

@app.get("/health")
def health():
    return {
        "status": "healthy" if model is not None else "unhealthy",
        "model_loaded": model is not None,
        "model_path": str(MODEL_PATH),
        "model_error": model_error,
    }


# --------------------------------------------------
# Prediction Endpoint
# --------------------------------------------------

@app.post("/predict")
def predict_car_price(car: CarInput):

    if model is None:
        raise HTTPException(
            status_code=500,
            detail="ML model is not loaded. Check the model path and model file.",
        )

    try:
        # Create DataFrame with the same feature names
        # used during model training.
        input_data = pd.DataFrame(
            [
                {
                    "Car_Name": car.Car_Name,
                    "Year": car.Year,
                    "Present_Price": car.Present_Price,
                    "Kms_Driven": car.Kms_Driven,
                    "Fuel_Type": car.Fuel_Type,
                    "Seller_Type": car.Seller_Type,
                    "Transmission": car.Transmission,
                    "Owner": car.Owner,
                }
            ]
        )

        # Make prediction
        prediction = model.predict(input_data)[0]

        return {
            "success": True,
            "prediction_price": float(prediction),
            "currency": "INR Lakh",
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}",
        )
