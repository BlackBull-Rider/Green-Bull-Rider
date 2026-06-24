import hashlib
import jwt

from datetime import datetime, timedelta

from backend.user_database.connection import get_user_connection

SECRET_KEY = "GREEN_BULL_RIDER_SECRET"


def hash_password(password):

    return hashlib.sha256(
        password.encode()
    ).hexdigest()


def create_token(user_id, role):

    payload = {
        "user_id": user_id,
        "role": role,
        "exp": datetime.utcnow() + timedelta(days=7)
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm="HS256"
    )


def decode_token(token):

    try:

        return jwt.decode(
            token,
            SECRET_KEY,
            algorithms=["HS256"]
        )

    except:

        return None


def register_user(
    name,
    email,
    mobile,
    password
):

    conn = get_user_connection()

    existing = conn.execute(
        """
        SELECT id
        FROM users
        WHERE email = ?
        """,
        (email,)
    ).fetchone()

    if existing:

        conn.close()

        return {
            "success": False,
            "message": "Email Already Exists"
        }

    conn.execute(
        """
        INSERT INTO users
        (
            name,
            email,
            mobile,
            password_hash
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            name,
            email,
            mobile,
            hash_password(password)
        )
    )

    conn.commit()
    conn.close()

    return {
        "success": True,
        "message": "Registration Submitted",
        "status": "pending"
    }


def login_user(email, password):

    conn = get_user_connection()

    user = conn.execute(
        """
        SELECT *
        FROM users
        WHERE email = ?
        """,
        (email,)
    ).fetchone()

    conn.close()

    if not user:

        return {
            "success": False,
            "message": "User Not Found"
        }

    if user[6] != "approved":

        return {
            "success": False,
            "message": "Account Pending Approval"
        }

    if user[4] != hash_password(password):

        return {
            "success": False,
            "message": "Wrong Password"
        }

    token = create_token(
        user[0],
        user[5]
    )

    return {
        "success": True,
        "token": token,
        "role": user[5],
        "user_id": user[0],
        "name": user[1]
    }
