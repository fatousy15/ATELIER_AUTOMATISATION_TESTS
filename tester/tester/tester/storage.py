import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "runs.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            api TEXT,
            passed INTEGER,
            failed INTEGER,
            total INTEGER,
            error_rate REAL,
            latency_avg REAL,
            latency_p95 REAL,
            tests_json TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_run(run):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO runs 
        (timestamp, api, passed, failed, total, error_rate, latency_avg, latency_p95, tests_json)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        run["timestamp"],
        run["api"],
        run["summary"]["passed"],
        run["summary"]["failed"],
        run["summary"]["total"],
        run["summary"]["error_rate"],
        run["summary"]["latency_ms_avg"],
        run["summary"]["latency_ms_p95"],
        json.dumps(run["tests"])
    ))
    conn.commit()
    conn.close()

def list_runs(limit=20):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        SELECT timestamp, api, passed, failed, total, 
               error_rate, latency_avg, latency_p95, tests_json
        FROM runs ORDER BY id DESC LIMIT ?
    ''', (limit,))
    rows = c.fetchall()
    conn.close()
    result = []
    for row in rows:
        result.append({
            "timestamp": row[0],
            "api": row[1],
            "summary": {
                "passed": row[2],
                "failed": row[3],
                "total": row[4],
                "error_rate": row[5],
                "latency_ms_avg": row[6],
                "latency_ms_p95": row[7]
            },
            "tests": json.loads(row[8])
        })
    return result
