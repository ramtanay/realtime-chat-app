import sqlite3

from utils.config import DATABASE_NAME


def create_tables():

    with sqlite3.connect(DATABASE_NAME) as conn:

        cursor = conn.cursor()

        print("Successfully connected to DB")

        cursor.execute(
            "PRAGMA foreign_keys = ON"
        )

        # =========================
        # USERS TABLE
        # =========================
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                username TEXT UNIQUE NOT NULL,

                password TEXT NOT NULL
            )
        """)

        # =========================
        # MESSAGES TABLE
        # =========================
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                user_id INTEGER NOT NULL,

                username TEXT NOT NULL,

                room TEXT NOT NULL,

                message TEXT NOT NULL,

                timestamp DATETIME
                DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (user_id)
                REFERENCES users(id)
            )
        """)

    print("Database Tables Created Successfully")