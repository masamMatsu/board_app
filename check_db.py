from board_db import BoardDB
BoardDB()
import sqlite3
conn = sqlite3.connect('board.db')
c = conn.cursor()
c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='history'")
print('table:', c.fetchone())
c.execute("PRAGMA table_info(history)")
cols = c.fetchall()
print('columns:')
for col in cols:
	print(col)
conn.close()
