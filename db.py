# db.py
import os
import sqlite3
import psycopg2
import mysql.connector

DB_ENGINE = os.getenv("DB_ENGINE", "sqlite").lower()  # sqlite | mysql | postgres
DB_NAME   = os.getenv("DB_NAME", "feedback.db")
DB_HOST   = os.getenv("DB_HOST", "localhost")
DB_USER   = os.getenv("DB_USER", "user")
DB_PASS   = os.getenv("DB_PASS", "password")
DB_PORT   = os.getenv("DB_PORT", "")

def _sqlite():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn

def _postgres():
    port = int(DB_PORT) if DB_PORT else 5432
    return psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=port
    )

def _mysql():
    port = int(DB_PORT) if DB_PORT else 3306
    return mysql.connector.connect(
        database=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=port
    )

def get_db():
    if DB_ENGINE == "postgres":
        return _postgres()
    if DB_ENGINE == "mysql":
        return _mysql()
    return _sqlite()

def init_db():
    conn = get_db()
    cur = conn.cursor()
    create_sql = """
    CREATE TABLE IF NOT EXISTS feedback (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      text TEXT NOT NULL,
      sentiment VARCHAR(16) NOT NULL,
      score REAL NOT NULL,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    if DB_ENGINE in ("mysql", "postgres"):
        # Normalize DDL for other engines
        create_sql = create_sql.replace("INTEGER PRIMARY KEY AUTOINCREMENT", "SERIAL PRIMARY KEY")
        if DB_ENGINE == "mysql":
            create_sql = create_sql.replace("SERIAL", "INT AUTO_INCREMENT")

    cur.execute(create_sql)
    conn.commit()
    cur.close()
    conn.close()

def insert_feedback(conn, text, sentiment, score):
    cur = conn.cursor()
    if DB_ENGINE == "sqlite":
        cur.execute("INSERT INTO feedback (text, sentiment, score) VALUES (?, ?, ?)",
                    (text, sentiment, score))
    else:
        cur.execute("INSERT INTO feedback (text, sentiment, score) VALUES (%s, %s, %s)",
                    (text, sentiment, score))
    conn.commit()
    cur.close()
    conn.close()

def get_stats(conn):
    cur = conn.cursor()
    # Count by sentiment
    if DB_ENGINE == "sqlite":
        cur.execute("SELECT sentiment, COUNT(*) FROM feedback GROUP BY sentiment")
    else:
        cur.execute("SELECT sentiment, COUNT(*) FROM feedback GROUP BY sentiment")
    rows = cur.fetchall()
    counts = {r[0]: int(r[1]) for r in rows}
    # Total
    if DB_ENGINE == "sqlite":
        cur.execute("SELECT COUNT(*) FROM feedback")
    else:
        cur.execute("SELECT COUNT(*) FROM feedback")
    total = int(cur.fetchone()[0])
    cur.close()
    conn.close()
    return {"total": total, "counts": counts}
