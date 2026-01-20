import sqlite3

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


def create_connection(db_file):
    """Create a database connection to the SQLite database specified by db_file."""
    conn = None
    try:
        conn = sqlite3.connect(db_file, check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS haircuts (
                id TEXT PRIMARY KEY,
                client_name TEXT NOT NULL,
                service_name TEXT NOT NULL,
                price REAL NOT NULL,
                date TEXT DEFAULT CURRENT_DATE,
                time TEXT,
                count INTEGER DEFAULT 0
            )
        """)
        cursor.execute("PRAGMA table_info(haircuts)")
        columns = [col[1] for col in cursor.fetchall()]
        
        # Migración para bases de datos antiguas
        if "name" in columns and "client_name" not in columns:
            # Renombrar columna name a service_name y agregar client_name
            cursor.execute("ALTER TABLE haircuts RENAME COLUMN name TO service_name")
            cursor.execute("ALTER TABLE haircuts ADD COLUMN client_name TEXT DEFAULT 'Cliente'")
        
        if "date" not in columns:
            cursor.execute("ALTER TABLE haircuts ADD COLUMN date TEXT DEFAULT CURRENT_DATE")
            
        if "time" not in columns:
            cursor.execute("ALTER TABLE haircuts ADD COLUMN time TEXT")

        if "count" not in columns:
            cursor.execute("ALTER TABLE haircuts ADD COLUMN count INTEGER DEFAULT 0")
        
        # Create service_prices table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS service_prices (
                id TEXT PRIMARY KEY,
                service_name TEXT UNIQUE NOT NULL,
                base_price INTEGER NOT NULL
            )
        """)
        
        # Populate default service prices if table is empty
        cursor.execute("SELECT COUNT(*) FROM service_prices")
        if cursor.fetchone()[0] == 0:
            from uuid import uuid4
            for service_name, base_price in DEFAULT_SERVICE_PRICES:
                cursor.execute(
                    "INSERT INTO service_prices (id, service_name, base_price) VALUES (?, ?, ?)",
                    (str(uuid4()), service_name, base_price)
                )
        
        conn.commit()
        logger.info(f"Connection to {db_file} established.")
    except sqlite3.Error as e:
        logger.error(f"Error connecting to database: {e}")
    return conn
