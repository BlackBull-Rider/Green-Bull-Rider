from backend.user_database.connection import (
    get_user_connection
)


def create_tables():

    conn = get_user_connection()

    conn.execute("""
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
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS portfolios (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER,

        symbol TEXT,

        qty REAL,

        avg_price REAL,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS transactions (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER,

        symbol TEXT,

        action TEXT,

        qty REAL,

        price REAL,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS watchlists (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER,

        symbol TEXT
    )
    """)

    conn.commit()
    conn.close()

    print("Users DB Ready")


if __name__ == "__main__":
    create_tables()
