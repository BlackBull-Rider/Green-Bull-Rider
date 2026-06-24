import sqlite3

DB_PATH = "/data/data/com.termux/files/home/Green-Bull-Rider/users.db"


def get_user_connection():

    conn = sqlite3.connect(DB_PATH)

    conn.row_factory = sqlite3.Row

    return conn
