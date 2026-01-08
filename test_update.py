from board_db import BoardDB

db = BoardDB()
rows = db.fetch_all()
print('before:', rows[0] if rows else 'no rows')
if rows:
    eid = rows[0][0]
    db.update(eid, '更新テスト', '更新単語')
    print('after:', db.fetch_by_id(eid))
else:
    print('no rows to update')
