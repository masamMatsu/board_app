from flask import Flask, render_template, request, redirect, url_for
from board_db import BoardDB  # ← クラスを別ファイルに分けた
from markupsafe import Markup, escape
import re
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
db = BoardDB()
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
ALLOWED_EXT = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        text = request.form.get("text")
        word = request.form.get("word")
        # handle uploaded image
        image_file = request.files.get('image')
        image_filename = None
        if image_file and image_file.filename:
            fn = secure_filename(image_file.filename)
            ext = fn.rsplit('.', 1)[-1].lower() if '.' in fn else ''
            if ext in ALLOWED_EXT:
                # ensure unique filename
                base, _ = os.path.splitext(fn)
                counter = 0
                candidate = fn
                while os.path.exists(os.path.join(UPLOAD_DIR, candidate)):
                    counter += 1
                    candidate = f"{base}_{counter}.{ext}"
                image_file.save(os.path.join(UPLOAD_DIR, candidate))
                image_filename = candidate
        result = {
            "text": text,
            "word": word
        }
        db.save(text, word, image_filename)
        # POST/Redirect/GET: 投稿後はリダイレクトしてフォームをクリアする
        return redirect(url_for('index'))
    # 検索クエリ（GET パラメータ）を受け取る
    q = request.args.get('q')
    q_text = request.args.get('q_text')
    history = db.fetch_all(q, q_text)

    def _highlight(s, term):
        if not term or not s:
            return escape(s or '')
        pattern = re.compile(re.escape(term), re.IGNORECASE)
        parts = []
        last = 0
        for m in pattern.finditer(s):
            parts.append(escape(s[last:m.start()]))
            parts.append(Markup('<mark>') + escape(m.group(0)) + Markup('</mark>'))
            last = m.end()
        parts.append(escape(s[last:]))
        return Markup('').join(parts)

    display_history = []
    for row in history:
        # row: (id, created_at, text, word)
        hid = row[0]
        hcreated = row[1]
        htext = _highlight(row[2], q_text) if q_text else escape(row[2] or '')
        hword = _highlight(row[3], q) if q else escape(row[3] or '')
        himage = row[4] if len(row) > 4 else None
        display_history.append((hid, hcreated, htext, hword, himage))

    return render_template("index.html", result=result, history=display_history, q=q, q_text=q_text)

@app.route("/delete", methods=["POST"])
def delete_all():
    db.delete_all()
    return redirect(url_for("index"))

@app.route("/delete/<int:entry_id>", methods=["POST"])
def delete_entry(entry_id):
    db.delete_by_id(entry_id)
    return redirect(url_for("index"))


@app.route('/edit/<int:entry_id>', methods=['GET', 'POST'])
def edit_entry(entry_id):
    if request.method == 'POST':
        text = request.form.get('text')
        word = request.form.get('word')
        db.update(entry_id, text, word)
        return redirect(url_for('index'))
    # GET
    row = db.fetch_by_id(entry_id)
    if not row:
        return redirect(url_for('index'))
    # row: (id, created_at, text, word)
    return render_template('edit.html', row=row)

if __name__ == "__main__":
    app.run(debug=True)
#    app.run(host="0.0.0.0", port=5000)
