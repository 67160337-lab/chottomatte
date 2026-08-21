from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import pandas as pd
import pickle

from pathlib import Path

from ..database import get_db
from ..models import AIPrediction
from ..schemas import AIPredictRequest


router = APIRouter(
    prefix="/ai",
    tags=["AI Prediction"]
)


# =========================
# Model Path
# =========================

BASE_DIR = Path(__file__).resolve().parents[2]

MODEL_PATH = (
    BASE_DIR
    / "model"
    / "water_treatment_ai_v1.pkl"
)


# =========================
# Load Model
# =========================

model = None

if MODEL_PATH.exists():

    with open(
        MODEL_PATH,
        "rb"
    ) as file:

        model = pickle.load(file)


# =========================
# Prediction
# =========================

@router.post("/predict")
def predict(
    user_id: int,
    data: AIPredictRequest,
    db: Session = Depends(get_db)
):

    if model is None:

        raise HTTPException(
            status_code=500,
            detail=(
                "AI model not found: "
                f"{MODEL_PATH}"
            )
        )

    # =========================
    # Model Input
    # =========================

    input_data = pd.DataFrame([
        {
            "influent_cod": data.influent_cod,
            "flow_rate": data.flow_rate,
            "water_temp": data.water_temp,
            "current_do": data.current_do
        }
    ])

    # =========================
    # AI Prediction
    # =========================

    predicted_speed = float(
        model.predict(input_data)[0]
    )

    # จำกัด 0-100%
    predicted_speed = max(
        0,
        min(
            100,
            predicted_speed
        )
    )

    # =========================
    # Save Prediction
    # =========================

    prediction = AIPrediction(

        user_id=user_id,

        influent_cod=data.influent_cod,

        flow_rate=data.flow_rate,

        water_temp=data.water_temp,

        current_do=data.current_do,

        predicted_speed=predicted_speed
    )

    db.add(prediction)

    db.commit()

    db.refresh(prediction)

    return {

        "message": "AI prediction successful",

        "predicted_speed": round(
            predicted_speed,
            2
        ),

        "unit": "%",

        "prediction_id": prediction.id,

    }


# =========================
# Prediction History
# =========================

@router.get("/history")
def prediction_history(
    user_id: int,
    db: Session = Depends(get_db)
):

    data = db.query(
        AIPrediction
    ).filter(
        AIPrediction.user_id == user_id
    ).order_by(
        AIPrediction.created_at.desc()
    ).all()

    return [

        {


            "influent_cod":
                item.influent_cod,

            "flow_rate":
                item.flow_rate,

            "water_temp":
                item.water_temp,

            "current_do":
                item.current_do,

            "predicted_speed":
                item.predicted_speed,

            "created_at":
                str(item.created_at)
        }

        for item in data
    ]


# =========================
# Latest Prediction
# =========================

@router.get("/latest")
def latest_prediction(
    user_id: int,
    db: Session = Depends(get_db)
):

    item = db.query(
        AIPrediction
    ).filter(
        AIPrediction.user_id == user_id
    ).order_by(
        AIPrediction.created_at.desc()
    ).first()

    if not item:

        return {
            "message": "No prediction data"
        }

    return {

        "predicted_speed":
            item.predicted_speed,

        "influent_cod":
            item.influent_cod,

        "flow_rate":
            item.flow_rate,

        "water_temp":
            item.water_temp,

        "current_do":
            item.current_do,

        "created_at":
            str(item.created_at)
    }