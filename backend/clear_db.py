from utils.config import DATABASE_NAME
import sqlite3

def clear_database():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    # Drop the messages table if it exists
    cursor.execute("DROP TABLE IF EXISTS messages")
    
    # Create a new messages table
    cursor.execute("""
        CREATE TABLE messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.execute("DROP TABLE IF EXISTS users")  # Clear all existing users
    
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS users(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                username TEXT UNIQUE NOT NULL,

                password TEXT NOT NULL
            )
        """)

    conn.commit()
    conn.close()
    print("Database cleared and reset.")

if __name__ == "__main__":
    clear_database()