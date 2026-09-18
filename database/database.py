import sqlite3
from pathlib import Path

DATABASE_PATH = Path("data/healthcare.db")


def get_connection():
    DATABASE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    return sqlite3.connect(DATABASE_PATH)


def init_database():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


def save_chat(question, answer):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO chat_history (question, answer)
        VALUES (?, ?)
    """, (question, answer))

    connection.commit()
    connection.close()


def get_chat_history():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, question, answer, created_at
        FROM chat_history
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    connection.close()

    return rows


def delete_chat_history():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("DELETE FROM chat_history")

    connection.commit()
    connection.close()