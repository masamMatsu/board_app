from app import app, UPLOAD_DIR
import io

client = app.test_client()
# create a small in-memory file
data = {
    'text': 'upload test',
    'word': 'アップロード',
    'image': (io.BytesIO(b'testimagecontent'), 'test.png')
}
resp = client.post('/', data=data, content_type='multipart/form-data', follow_redirects=True)
print('POST status:', resp.status_code)
# list files in upload dir
import os
print('uploads:', os.listdir(UPLOAD_DIR))
