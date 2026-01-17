import sqlite3

import loguru

logger = loguru.logger


def create_connection(db_file):
    """Create a database connection to the SQLite database specified by db_file."""
    conn = None
    try:
        conn = sqlite3.connect(db_file, check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS haircuts (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                date TEXT DEFAULT CURRENT_DATE
            )
        """)
        cursor.execute("PRAGMA table_info(haircuts)")
        columns = [col[1] for col in cursor.fetchall()]
        if "date" not in columns:
            cursor.execute("ALTER TABLE haircuts ADD COLUMN date TEXT DEFAULT CURRENT_DATE")
        conn.commit()
        logger.info(f"Connection to {db_file} established.")
    except sqlite3.Error as e:
        logger.error(f"Error connecting to database: {e}")
    return conn
