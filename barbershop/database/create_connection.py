import psycopg2
from psycopg2.extras import RealDictCursor

from dotenv import load_dotenv
import os

load_dotenv()

import loguru

logger = loguru.logger

DEFAULT_SERVICE_PRICES = [
    ("Degradado", 9000),
    ("Corte", 7000),
    ("Barba", 3000),
    ("Corte+Barba", 10000),
    ("Claritos", 5000),
    ("Otros", 8000),
]


def create_connection(db_url=None):
    """Create a database connection to PostgreSQL."""
    conn = None
    try:
        import os
        if db_url is None:
            db_url = os.environ.get("DATABASE_URL")
        
        conn = psycopg2.connect(db_url, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS haircuts (
                id TEXT PRIMARY KEY,
                client_name TEXT NOT NULL,
                service_name TEXT NOT NULL,
                price REAL NOT NULL,
                date TEXT DEFAULT CURRENT_DATE,
                time TEXT,
                count INTEGER DEFAULT 0,
                tip REAL DEFAULT 0
            )
        """)
        
        cursor.execute("""
            SELECT column_name FROM information_schema.columns 
            WHERE table_name = 'haircuts'
        """)
        columns = [row["column_name"] for row in cursor.fetchall()]
        
        if "name" in columns and "client_name" not in columns:
            cursor.execute("ALTER TABLE haircuts RENAME COLUMN name TO service_name")
            cursor.execute("ALTER TABLE haircuts ADD COLUMN client_name TEXT DEFAULT 'Cliente'")
        
        if "date" not in columns:
            cursor.execute("ALTER TABLE haircuts ADD COLUMN date TEXT DEFAULT CURRENT_DATE")
            
        if "time" not in columns:
            cursor.execute("ALTER TABLE haircuts ADD COLUMN time TEXT")

        if "count" not in columns:
            cursor.execute("ALTER TABLE haircuts ADD COLUMN count INTEGER DEFAULT 0")
        
        if "tip" not in columns:
            cursor.execute("ALTER TABLE haircuts ADD COLUMN tip REAL DEFAULT 0")
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS service_prices (
                id TEXT PRIMARY KEY,
                service_name TEXT UNIQUE NOT NULL,
                base_price INTEGER NOT NULL
            )
        """)
        
        cursor.execute("SELECT COUNT(*) FROM service_prices")
        result = cursor.fetchone()
        if result is None or result["count"] == 0:
            from uuid import uuid4
            for service_name, base_price in DEFAULT_SERVICE_PRICES:
                cursor.execute(
                    "INSERT INTO service_prices (id, service_name, base_price) VALUES (%s, %s, %s)",
                    (str(uuid4()), service_name, base_price)
                )
        
        conn.commit()
        logger.info("Connection to PostgreSQL established.")
        return conn
    except psycopg2.Error as e:
        logger.error(f"Error connecting to database: {e}")
        return None
    except Exception as e:
        import traceback
        logger.error(f"Unexpected error: {e}\n{traceback.format_exc()}")
        return None
