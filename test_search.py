from board_db import BoardDB

db = BoardDB()
print('All rows:')
for r in db.fetch_all():
    print(r)
print('\nSearch by 用語 (Python):')
for r in db.fetch_all('Python'):
    print(r)
print('\nSearch by 説明 (更新テスト):')
for r in db.fetch_all(None, '更新テスト'):
    print(r)
