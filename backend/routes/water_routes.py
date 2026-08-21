from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import WaterQuality, Alert
from ..schemas import WaterQualityRequest


router = APIRouter(
    prefix="/water",
    tags=["Water Quality"]
)


# =========================
# Add Water Quality
# =========================

@router.post("/")
def add_water_quality(
    user_id: int,
    data: WaterQualityRequest,
    db: Session = Depends(get_db)
):

    water = WaterQuality(
        user_id=user_id,
        do=data.do,
        temperature=data.temperature,
        flow_rate=data.flow_rate,
        cod=data.cod,
        status=data.status
    )

    db.add(water)

    # =========================
    # สร้าง Alert ถ้า DO ต่ำ
    # =========================

    if data.do < 2:

        alert = Alert(
            user_id=user_id,
            message="DO level is low",
            do_value=data.do
        )

        db.add(alert)

    db.commit()

    db.refresh(water)

    return {
        "message": "Water quality saved",
        "id": water.id,
        "user_id": user_id
    }


# =========================
# Get All
# =========================

@router.get("/")
def get_water_quality(
    user_id: int,
    db: Session = Depends(get_db)
):

    data = db.query(
        WaterQuality
    ).filter(
        WaterQuality.user_id == user_id
    ).order_by(
        WaterQuality.created_at.desc()
    ).all()

    return [
        {
            "id": item.id,
            "do": item.do,
            "temperature": item.temperature,
            "flow_rate": item.flow_rate,
            "cod": item.cod,
            "status": item.status,
            "created_at": str(
                item.created_at
            )
        }

        for item in data
    ]


# =========================
# Latest
# =========================

@router.get("/latest")
def latest_water_quality(
    user_id: int,
    db: Session = Depends(get_db)
):

    item = db.query(
        WaterQuality
    ).filter(
        WaterQuality.user_id == user_id
    ).order_by(
        WaterQuality.created_at.desc()
    ).first()

    if not item:

        raise HTTPException(
            status_code=404,
            detail="No water quality data"
        )

    return {
        "id": item.id,
        "user_id": item.user_id,
        "do": item.do,
        "temperature": item.temperature,
        "flow_rate": item.flow_rate,
        "cod": item.cod,
        "status": item.status,
        "created_at": str(
            item.created_at
        )
    }