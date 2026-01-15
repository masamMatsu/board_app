import sqlite3
from datetime import datetime

class BoardDB:
    def __init__(self, db_path="board.db"):
        self.db_path = db_path
        # テーブルが存在しない場合に作成する（flask run 時に init_db.py が実行されないため）
        conn = self._connect()
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT,
                text TEXT
            )
        """)
        conn.commit()
        # カラム 'word' が無ければ追加する（安全なマイグレーション）
        c.execute("PRAGMA table_info(history)")
        cols = [row[1] for row in c.fetchall()]
        if 'word' not in cols:
            c.execute("ALTER TABLE history ADD COLUMN word TEXT")
            conn.commit()
        # カラム 'image' が無ければ追加する（画像ファイル名を保持）
        if 'image' not in cols:
            c.execute("ALTER TABLE history ADD COLUMN image TEXT")
            conn.commit()
        conn.close()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def save(self, text, word=None, image=None):
        conn = self._connect()
        c = conn.cursor()
        c.execute("""
            INSERT INTO history (created_at, text, word, image)
            VALUES (?, ?, ?, ?)
        """, (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), text, word, image))
        conn.commit()
        conn.close()

    def fetch_all(self, q=None, q_text=None):
        conn = self._connect()
        c = conn.cursor()
        sql = "SELECT id, created_at, text, word, image FROM history"
        conds = []
        params = []
        if q:
            conds.append("word LIKE ?")
            params.append('%' + q + '%')
        if q_text:
            conds.append("text LIKE ?")
            params.append('%' + q_text + '%')
        if conds:
            sql += " WHERE " + " AND ".join(conds)
        sql += " ORDER BY id DESC"
        c.execute(sql, params)
        rows = c.fetchall()
        conn.close()
        return rows

    def delete_all(self):
        conn = self._connect()
        c = conn.cursor()
        c.execute("DELETE FROM history")
        conn.commit()
        conn.close()

    def delete_by_id(self, entry_id):
        conn = self._connect()
        c = conn.cursor()
        c.execute("DELETE FROM history WHERE id = ?", (entry_id,))
        conn.commit()
        conn.close()

    def fetch_by_id(self, entry_id):
        conn = self._connect()
        c = conn.cursor()
        c.execute("SELECT id, created_at, text, word, image FROM history WHERE id = ?", (entry_id,))
        row = c.fetchone()
        conn.close()
        return row

    def update(self, entry_id, text, word=None, image=None):
        conn = self._connect()
        c = conn.cursor()
        # update image only if provided (allow clearing with empty string)
        if image is not None:
            c.execute("UPDATE history SET text = ?, word = ?, image = ? WHERE id = ?", (text, word, image, entry_id))
        else:
            c.execute("UPDATE history SET text = ?, word = ? WHERE id = ?", (text, word, entry_id))
        conn.commit()
        conn.close()