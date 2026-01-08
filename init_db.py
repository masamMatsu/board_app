import sqlite3

conn = sqlite3.connect("board.db")
c = conn.cursor()

# テーブル作成
c.execute("""
CREATE TABLE IF NOT EXISTS history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TEXT,
    text TEXT
)
""")

conn.commit()
conn.close()