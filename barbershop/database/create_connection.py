import sqlite3

import loguru

logger = loguru.logger


def create_connection(db_file):
    """Create a database connection to the SQLite database specified by db_file."""
    conn = None
    try:
        conn = sqlite3.connect(db_file, check_same_thread=False)

        logger.info(f"Connection to {db_file} established.")
    except sqlite3.Error as e:
        logger.error(f"Error connecting to database: {e}")
    return conn
