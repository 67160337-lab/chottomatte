from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    Boolean,
    ForeignKey
)

from datetime import datetime

from .database import Base


# =========================
# User
# =========================

class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    username = Column(
        String(100),
        unique=True,
        nullable=False,
        index=True
    )

    email = Column(
        String(150),
        unique=True,
        nullable=False
    )

    password_hash = Column(
        String(255),
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


# =========================
# Water Quality
# =========================

class WaterQuality(Base):

    __tablename__ = "water_quality"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # เจ้าของข้อมูล
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    do = Column(
        Float,
        nullable=False
    )

    temperature = Column(
        Float,
        nullable=True
    )

    flow_rate = Column(
        Float,
        nullable=True
    )

    cod = Column(
        Float,
        nullable=True
    )

    status = Column(
        String(50),
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


# =========================
# AI Prediction
# =========================

class AIPrediction(Base):

    __tablename__ = "ai_predictions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # เจ้าของข้อมูล
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    influent_cod = Column(
        Float
    )

    flow_rate = Column(
        Float
    )

    water_temp = Column(
        Float
    )

    current_do = Column(
        Float
    )

    predicted_speed = Column(
        Float
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


# =========================
# Aerator
# =========================

class Aerator(Base):

    __tablename__ = "aerator"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # เจ้าของ Aerator
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        unique=True,
        index=True
    )

    mode = Column(
        String(20),
        default="AUTO"
    )

    speed = Column(
        Float,
        default=50
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow
    )


# =========================
# Alert
# =========================

class Alert(Base):

    __tablename__ = "alerts"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # เจ้าของ Alert
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    message = Column(
        String(500)
    )

    do_value = Column(
        Float,
        nullable=True
    )

    is_read = Column(
        Boolean,
        default=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )