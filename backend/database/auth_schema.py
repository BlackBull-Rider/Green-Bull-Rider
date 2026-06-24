from backend.database.connection import get_connection


def create_user_table():

    conn = get_connection()

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            email TEXT UNIQUE NOT NULL,

            mobile TEXT,

            password_hash TEXT NOT NULL,

            role TEXT DEFAULT 'user',

            status TEXT DEFAULT 'pending',

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_user_table()
