from app import _highlight  # noqa: F401
from app import db

# build a sample display using current DB and highlight for manual check
rows = db.fetch_all('XDR')
if not rows:
    print('no rows')
else:
    for r in rows:
        print('raw word:', r[3])
        print('highlighted:', _highlight(r[3], 'XDR'))
        print('---')
