import sqlite3

from barbershop.database.create_connection import create_connection


def test_create_connection_success(tmp_path):
    db_path = tmp_path / "test.db"
    conn = create_connection(str(db_path))
    assert conn is not None
    conn.close()


def test_create_connection_failure(monkeypatch):
    def fake_connect(*args, **kwargs):
        raise sqlite3.Error("fail")

    monkeypatch.setattr(sqlite3, "connect", fake_connect)
    conn = create_connection("invalid_path")
    assert conn is None
