from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from ..database import get_db
from ..models import Aerator
from ..schemas import AeratorRequest


router = APIRouter(
    prefix="/aerator",
    tags=["Aerator"]
)


# =========================
# Get Current Aerator
# =========================

@router.get("/")
def get_aerator(
    user_id: int,
    db: Session = Depends(get_db)
):

    aerator = db.query(
        Aerator
    ).filter(
        Aerator.user_id == user_id
    ).first()


    # ถ้ายังไม่มี Aerator ของ User นี้
    # ให้สร้างค่าเริ่มต้น
    if not aerator:

        aerator = Aerator(
            user_id=user_id,
            mode="AUTO",
            speed=50
        )

        db.add(aerator)

        db.commit()

        db.refresh(aerator)


    return {
        "id": aerator.id,

        "user_id": aerator.user_id,

        "mode": aerator.mode,

        "speed": aerator.speed,

        "updated_at": str(
            aerator.updated_at
        )
    }


# =========================
# Update Aerator
# =========================

@router.put("/")
def update_aerator(
    user_id: int,
    data: AeratorRequest,
    db: Session = Depends(get_db)
):

    # ตรวจสอบ Mode
    if data.mode not in [
        "AUTO",
        "MANUAL"
    ]:

        raise HTTPException(
            status_code=400,
            detail="Mode must be AUTO or MANUAL"
        )


    # หา Aerator ของ User
    aerator = db.query(
        Aerator
    ).filter(
        Aerator.user_id == user_id
    ).first()


    # ถ้ายังไม่มี ให้สร้างใหม่
    if not aerator:

        aerator = Aerator(
            user_id=user_id,
            mode="AUTO",
            speed=50
        )

        db.add(aerator)


    # Update ข้อมูล
    aerator.mode = data.mode

    aerator.speed = data.speed

    aerator.updated_at = datetime.utcnow()


    db.commit()

    db.refresh(aerator)


    return {

        "message": "Aerator updated",

        "id": aerator.id,

        "user_id": aerator.user_id,

        "mode": aerator.mode,

        "speed": aerator.speed,

        "updated_at": str(
            aerator.updated_at
        )
    }