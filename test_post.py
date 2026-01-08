from app import app
from board_db import BoardDB

client = app.test_client()
# post sample data
resp = client.post('/', data={'text': 'テスト投稿', 'word': '単語A'}, follow_redirects=True)
print('POST status:', resp.status_code)
# verify last row
db = BoardDB()
rows = db.fetch_all()
print('latest row:', rows[0] if rows else None)
