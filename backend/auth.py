from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


# =========================
# Hash Password
# =========================

def hash_password(password: str):

    # bcrypt รองรับ password สูงสุด 72 bytes
    password = password[:72]

    return pwd_context.hash(password)


# =========================
# Verify Password
# =========================

def verify_password(
    plain_password: str,
    hashed_password: str
):

    # bcrypt รองรับ password สูงสุด 72 bytes
    plain_password = plain_password[:72]

    return pwd_context.verify(
        plain_password,
        hashed_password
    )