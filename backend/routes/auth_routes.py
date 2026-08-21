from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User
from ..schemas import (
    RegisterRequest,
    LoginRequest,
    ChangePasswordRequest
)
from ..auth import (
    hash_password,
    verify_password
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# =========================
# Register
# =========================

@router.post("/register")
def register(
    data: RegisterRequest,
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.username == data.username
    ).first()

    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )


    existing_email = db.query(User).filter(
        User.email == data.email
    ).first()

    if existing_email:

        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )


    user = User(
        username=data.username,
        email=data.email,
        password_hash=hash_password(
            data.password
        )
    )

    db.add(user)

    db.commit()

    db.refresh(user)


    return {
        "message": "Register successful",
        "user_id": user.id,
        "username": user.username
    }


# =========================
# Login
# =========================

@router.post("/login")
def login(
    data: LoginRequest,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.username == data.username
    ).first()


    if not user:

        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )


    if not verify_password(
        data.password,
        user.password_hash
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )


    return {
        "message": "Login successful",
        "user_id": user.id,
        "username": user.username
    }


# =========================
# Logout
# =========================

@router.post("/logout")
def logout():

    return {
        "message": "Logout successful"
    }


# =========================
# Change Password
# =========================

@router.post("/change-password")
def change_password(
    user_id: int,
    data: ChangePasswordRequest,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.id == user_id
    ).first()


    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )


    if not verify_password(
        data.old_password,
        user.password_hash
    ):

        raise HTTPException(
            status_code=400,
            detail="Old password is incorrect"
        )


    user.password_hash = hash_password(
        data.new_password
    )

    db.commit()


    return {
        "message": "Password changed successfully"
    }


# =========================
# Get Users
# =========================

@router.get("/users")
def get_users(
    db: Session = Depends(get_db)
):

    users = db.query(User).all()


    return [
        {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }

        for user in users
    ]


# =========================
# Get User
# =========================

@router.get("/users/{user_id}")
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.id == user_id
    ).first()


    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )


    return {
        "id": user.id,
        "username": user.username,
        "email": user.email
    }


# =========================
# Delete User
# =========================

@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.id == user_id
    ).first()


    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )


    db.delete(user)

    db.commit()


    return {
        "message": "User deleted successfully"
    }