"""Tests para verificar manejo de errores de base de datos."""

import sqlite3
import pytest
from fastapi.testclient import TestClient
from barbershop.app import app


client = TestClient(app)


class TestDatabaseErrors:
    """Tests para troubleshootear errores de base de datos."""

    def test_create_connection_readonly_db(self, tmp_path):
        """Test que simula una base de datos de solo lectura."""
        readonly_db = tmp_path / "readonly.db"
        readonly_db.touch()
        readonly_db.chmod(0o444)
        
        with pytest.raises((sqlite3.OperationalError, PermissionError)):
            conn = sqlite3.connect(str(readonly_db))
            conn.execute("CREATE TABLE test (id INT)")
            conn.commit()
            conn.close()

    def test_create_connection_memory_db(self):
        """Test usando base de datos en memoria (siempre funciona)."""
        conn = sqlite3.connect(":memory:")
        conn.execute("CREATE TABLE haircuts (id TEXT, name TEXT, price REAL, date TEXT)")
        conn.commit()
        
        cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        assert len(tables) == 1
        assert tables[0][0] == "haircuts"
        
        conn.close()

    def test_database_operations_on_memory_db(self):
        """Test completo de operaciones en base de datos en memoria."""
        conn = sqlite3.connect(":memory:")
        conn.execute("""
            CREATE TABLE haircuts (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                date TEXT DEFAULT CURRENT_DATE
            )
        """)
        conn.commit()
        
        conn.execute(
            "INSERT INTO haircuts (id, name, price, date) VALUES (?, ?, ?, ?)",
            ("test-1", "Test Cut", 25000.0, "2024-01-17")
        )
        conn.commit()
        
        cursor = conn.execute("SELECT * FROM haircuts")
        rows = cursor.fetchall()
        assert len(rows) == 1
        assert rows[0][1] == "Test Cut"
        
        conn.execute("DELETE FROM haircuts WHERE id = ?", ("test-1",))
        conn.commit()
        
        cursor = conn.execute("SELECT * FROM haircuts")
        rows = cursor.fetchall()
        assert len(rows) == 0
        
        conn.close()

    def test_database_constraint_violations(self):
        """Test de violaciones de constraints."""
        conn = sqlite3.connect(":memory:")
        conn.execute("""
            CREATE TABLE haircuts (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                price REAL NOT NULL
            )
        """)
        conn.commit()
        
        conn.execute("INSERT INTO haircuts VALUES (?, ?, ?)", ("1", "Cut 1", 100.0))
        conn.commit()
        
        try:
            conn.execute("INSERT INTO haircuts VALUES (?, ?, ?)", ("1", "Cut 2", 200.0))
            conn.commit()
            assert False, "Should have raised IntegrityError"
        except sqlite3.IntegrityError:
            pass
        
        try:
            conn.execute("INSERT INTO haircuts VALUES (?, ?, ?)", ("2", None, 100.0))
            conn.commit()
            assert False, "Should have raised IntegrityError"
        except sqlite3.IntegrityError:
            pass
        
        conn.close()

    def test_database_concurrent_operations(self):
        """Test de operaciones concurrentes simuladas."""
        conn = sqlite3.connect(":memory:")
        conn.execute("CREATE TABLE counters (id TEXT PRIMARY KEY, value INTEGER)")
        conn.execute("INSERT INTO counters VALUES ('count', 0)")
        conn.commit()
        
        for i in range(10):
            cursor = conn.execute("SELECT value FROM counters WHERE id = 'count'")
            current = cursor.fetchone()[0]
            conn.execute("UPDATE counters SET value = ? WHERE id = 'count'", (current + 1,))
            conn.commit()
        
        cursor = conn.execute("SELECT value FROM counters WHERE id = 'count'")
        assert cursor.fetchone()[0] == 10
        
        conn.close()

    def test_sql_injection_prevention(self):
        """Test de prevención de SQL injection."""
        conn = sqlite3.connect(":memory:")
        conn.execute("""
            CREATE TABLE haircuts (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                price REAL NOT NULL
            )
        """)
        conn.commit()
        
        user_input = "'; DROP TABLE haircuts; --"
        cursor = conn.execute("SELECT * FROM haircuts WHERE name = ?", (user_input,))
        assert cursor.fetchall() == []
        
        cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        assert len(tables) == 1
        assert tables[0][0] == "haircuts"
        
        conn.close()

    def test_rollback_on_error(self):
        """Test de rollback cuando hay errores."""
        conn = sqlite3.connect(":memory:")
        conn.execute("""
            CREATE TABLE haircuts (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                price REAL NOT NULL
            )
        """)
        conn.execute("INSERT INTO haircuts VALUES (?, ?, ?)", ("1", "Cut 1", 100.0))
        conn.commit()
        
        try:
            conn.execute("INSERT INTO haircuts VALUES (?, ?, ?)", ("1", "Cut 2", 200.0))
            conn.commit()
        except sqlite3.IntegrityError:
            conn.rollback()
        
        cursor = conn.execute("SELECT * FROM haircuts")
        rows = cursor.fetchall()
        assert len(rows) == 1
        assert rows[0][1] == "Cut 1"
        
        conn.close()

    def test_transaction_isolation(self):
        """Test de aislamiento de transacciones con una sola conexión."""
        conn = sqlite3.connect(":memory:")
        conn.execute("""
            CREATE TABLE haircuts (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL
            )
        """)
        conn.commit()
        
        conn.execute("INSERT INTO haircuts VALUES (?, ?)", ("1", "Cut 1"))
        conn.commit()
        
        cursor = conn.execute("SELECT * FROM haircuts")
        rows = cursor.fetchall()
        assert len(rows) == 1
        
        conn.execute("BEGIN TRANSACTION")
        cursor = conn.execute("SELECT * FROM haircuts")
        rows_in_transaction = cursor.fetchall()
        assert len(rows_in_transaction) == 1
        
        conn.execute("INSERT INTO haircuts VALUES (?, ?)", ("2", "Cut 2"))
        conn.commit()
        
        cursor = conn.execute("SELECT * FROM haircuts")
        rows_after = cursor.fetchall()
        assert len(rows_after) == 2
        
        conn.close()
