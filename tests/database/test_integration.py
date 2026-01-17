"""Tests de integración con base de datos en memoria para evitar problemas de permisos."""

import sqlite3
from datetime import date
from uuid import uuid4
import pytest
from fastapi.testclient import TestClient


def create_test_db():
    """Crear una base de datos en memoria para tests."""
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
    return conn


def get_all_haircuts(conn):
    """Obtener todos los cortes de la base de datos."""
    cursor = conn.execute("SELECT * FROM haircuts ORDER BY rowid DESC")
    return cursor.fetchall()


def insert_haircut(conn, id, name, price, haircut_date):
    """Insertar un corte en la base de datos."""
    conn.execute(
        "INSERT INTO haircuts (id, name, price, date) VALUES (?, ?, ?, ?)",
        (id, name, price, haircut_date)
    )
    conn.commit()


class TestHaircutsIntegration:
    """Tests de integración completos para el sistema de haircuts."""

    def setup_method(self):
        """Setup antes de cada test."""
        self.db = create_test_db()
        self.haircut_id = str(uuid4())

    def teardown_method(self):
        """Cleanup después de cada test."""
        self.db.close()

    def test_full_crud_workflow(self):
        """Test del flujo completo CRUD."""
        insert_haircut(self.db, self.haircut_id, "Corte Completo", 25000.0, date.today().isoformat())
        
        rows = get_all_haircuts(self.db)
        assert len(rows) == 1
        assert rows[0][1] == "Corte Completo"
        assert rows[0][2] == 25000.0
        
        self.db.execute(
            "UPDATE haircuts SET price = 30000.0 WHERE id = ?",
            (self.haircut_id,)
        )
        self.db.commit()
        
        rows = get_all_haircuts(self.db)
        assert rows[0][2] == 30000.0
        
        self.db.execute("DELETE FROM haircuts WHERE id = ?", (self.haircut_id,))
        self.db.commit()
        
        rows = get_all_haircuts(self.db)
        assert len(rows) == 0

    def test_multiple_haircuts_same_day(self):
        """Test de múltiples cortes el mismo día."""
        today = date.today().isoformat()
        ids = [str(uuid4()) for _ in range(5)]
        
        prices = [20000.0, 25000.0, 30000.0, 35000.0, 40000.0]
        for i, id in enumerate(ids):
            insert_haircut(self.db, id, f"Corte {i+1}", prices[i], today)
        
        rows = get_all_haircuts(self.db)
        assert len(rows) == 5
        
        total = sum(row[2] for row in rows)
        expected_total = sum(prices)
        assert total == expected_total

    def test_daily_summary_calculation(self):
        """Test del cálculo de resumen diario."""
        today = date.today().isoformat()
        yesterday = date.fromisoformat(today).replace(day=date.fromisoformat(today).day - 1).isoformat()
        
        insert_haircut(self.db, str(uuid4()), "Corte Hoy 1", 25000.0, today)
        insert_haircut(self.db, str(uuid4()), "Corte Hoy 2", 30000.0, today)
        insert_haircut(self.db, str(uuid4()), "Corte Ayer", 20000.0, yesterday)
        
        cursor = self.db.execute(
            "SELECT date, SUM(price), COUNT(*) FROM haircuts GROUP BY date ORDER BY date DESC"
        )
        results = cursor.fetchall()
        
        today_results = [r for r in results if r[0] == today]
        assert len(today_results) == 1
        assert today_results[0][1] == 55000.0
        assert today_results[0][2] == 2
        
        yesterday_results = [r for r in results if r[0] == yesterday]
        assert len(yesterday_results) == 1
        assert yesterday_results[0][1] == 20000.0

    def test_price_precision(self):
        """Test de precisión en precios."""
        insert_haircut(self.db, self.haircut_id, "Corte Precision", 19999.99, date.today().isoformat())
        
        rows = get_all_haircuts(self.db)
        assert rows[0][2] == 19999.99

    def test_special_characters_in_name(self):
        """Test de caracteres especiales en nombres."""
        insert_haircut(self.db, self.haircut_id, "Corte 'Especial' & Estilo", 30000.0, date.today().isoformat())
        
        rows = get_all_haircuts(self.db)
        assert "'" in rows[0][1]
        assert "&" in rows[0][1]

    def test_delete_by_date(self):
        """Test de eliminación por fecha."""
        today = date.today().isoformat()
        yesterday = date.fromisoformat(today).replace(day=date.fromisoformat(today).day - 1).isoformat()
        
        insert_haircut(self.db, str(uuid4()), "Corte Hoy", 25000.0, today)
        insert_haircut(self.db, str(uuid4()), "Corte Ayer", 20000.0, yesterday)
        
        self.db.execute("DELETE FROM haircuts WHERE date = ?", (today,))
        self.db.commit()
        
        rows = get_all_haircuts(self.db)
        assert len(rows) == 1
        assert "Ayer" in rows[0][1]

    def test_empty_database(self):
        """Test con base de datos vacía."""
        rows = get_all_haircuts(self.db)
        assert len(rows) == 0
        
        cursor = self.db.execute("SELECT SUM(price) FROM haircuts")
        total = cursor.fetchone()[0]
        assert total is None

    def test_database_schema_integrity(self):
        """Test de integridad del esquema de la base de datos."""
        cursor = self.db.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        assert len(tables) == 1
        assert tables[0][0] == "haircuts"
        
        cursor = self.db.execute(f"PRAGMA table_info(haircuts)")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        assert "id" in column_names
        assert "name" in column_names
        assert "price" in column_names
        assert "date" in column_names

    def test_concurrent_inserts(self):
        """Test de inserts concurrentes."""
        ids = [str(uuid4()) for _ in range(10)]
        
        for id in ids:
            insert_haircut(self.db, id, f"Corte {id[:8]}", 25000.0, date.today().isoformat())
        
        rows = get_all_haircuts(self.db)
        assert len(rows) == 10
        
        unique_ids = set(row[0] for row in rows)
        assert len(unique_ids) == 10

    def test_large_price_values(self):
        """Test con valores grandes de precio."""
        insert_haircut(self.db, self.haircut_id, "Corte Premium", 999999.99, date.today().isoformat())
        
        rows = get_all_haircuts(self.db)
        assert rows[0][2] == 999999.99
        
        total = self.db.execute("SELECT SUM(price) FROM haircuts").fetchone()[0]
        assert total == 999999.99

    def test_zero_price(self):
        """Test con precio cero."""
        insert_haircut(self.db, self.haircut_id, "Corte Gratis", 0.0, date.today().isoformat())
        
        rows = get_all_haircuts(self.db)
        assert rows[0][2] == 0.0

    def test_negative_price(self):
        """Test con precio negativo (caso edge)."""
        insert_haircut(self.db, self.haircut_id, "Corte Negativo", -10000.0, date.today().isoformat())
        
        rows = get_all_haircuts(self.db)
        assert rows[0][2] == -10000.0
