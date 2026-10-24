import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent.parent.parent / "reservas.db"
SCHEMA_PATH = Path(__file__).parent / "schema.sql"


def get_connection():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        schema = f.read()
    conn.executescript(schema)
    conn.commit()
    conn.close()
