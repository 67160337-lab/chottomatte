from pydantic import BaseModel, Field


# =========================
# Authentication
# =========================

class RegisterRequest(BaseModel):

    username: str

    email: str

    password: str


class LoginRequest(BaseModel):

    username: str

    password: str


class ChangePasswordRequest(BaseModel):

    old_password: str

    new_password: str


# =========================
# Water Quality
# =========================

class WaterQualityRequest(BaseModel):

    do: float

    temperature: float

    flow_rate: float

    cod: float

    status: str = "NORMAL"


# =========================
# Aerator
# =========================

class AeratorRequest(BaseModel):

    mode: str = Field(
        default="AUTO"
    )

    speed: float = Field(
        default=50,
        ge=0,
        le=100
    )


# =========================
# AI
# =========================

class AIPredictRequest(BaseModel):

    influent_cod: float

    flow_rate: float

    water_temp: float

    current_do: float