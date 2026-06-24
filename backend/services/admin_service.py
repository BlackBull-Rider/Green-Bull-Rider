from backend.user_database.connection import get_user_connection


def get_pending_users():

    conn = get_user_connection()

    rows = conn.execute(
        """
        SELECT
            id,
            name,
            email,
            mobile,
            role,
            status
        FROM users
        WHERE status='pending'
        """
    ).fetchall()

    conn.close()

    return {
        "count": len(rows),
        "users": [
            dict(row)
            for row in rows
        ]
    }


def approve_user(user_id):

    conn = get_user_connection()

    conn.execute(
        """
        UPDATE users
        SET status='approved'
        WHERE id=?
        """,
        (user_id,)
    )

    conn.commit()
    conn.close()

    return {"message": "User Approved"}


def reject_user(user_id):

    conn = get_user_connection()

    conn.execute(
        """
        UPDATE users
        SET status='rejected'
        WHERE id=?
        """,
        (user_id,)
    )

    conn.commit()
    conn.close()

    return {"message": "User Rejected"}


def block_user(user_id):

    conn = get_user_connection()

    conn.execute(
        """
        UPDATE users
        SET status='blocked'
        WHERE id=?
        """,
        (user_id,)
    )

    conn.commit()
    conn.close()

    return {"message": "User Blocked"}


def get_all_users():

    conn = get_user_connection()

    rows = conn.execute(
        """
        SELECT
            id,
            name,
            email,
            mobile,
            role,
            status
        FROM users
        ORDER BY id DESC
        """
    ).fetchall()

    conn.close()

    return {
        "count": len(rows),
        "users": [
            dict(row)
            for row in rows
        ]
    }
