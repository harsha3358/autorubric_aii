import sqlite3

conn = sqlite3.connect("data.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS results (
id TEXT, prompt TEXT, answer TEXT, score REAL, feedback TEXT
)
""")

conn.commit()