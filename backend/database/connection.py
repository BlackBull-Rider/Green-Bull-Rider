import sqlite3

DB_PATH = "/data/data/com.termux/files/home/Green-Bull-Data-Engine/database/market.db"

def get_connection():
    return sqlite3.connect(DB_PATH)
