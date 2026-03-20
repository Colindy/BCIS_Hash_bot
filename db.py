import sqlite3
import time

conn = sqlite3.connect("hash_jobs.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS jobs(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT,
    hash TEXT,
    status TEXT,
    submitted INTEGER
)
""")

conn.commit()

def add_job(user_id, hash_value):
    cursor.execute(
        "INSERT INTO jobs (user_id, hash, status, submitted) VALUES (?, ?, ?, ?)",
        (user_id, hash_value, "queued", int(time.time()))
    )
    conn.commit()

def last_job_time(user_id):
    cursor.execute(
        "SELECT submitted FROM jobs WHERE user_id=? ORDER BY submitted DESC LIMIT 1",
        (user_id,)
    )
    row = cursor.fetchone()
    return row[0] if row else None