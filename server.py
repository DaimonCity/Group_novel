from flask import Flask, render_template, request, redirect, url_for, render_template_string
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///novel.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Модель для главы
class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(50), nullable=False)
    votes = db.Column(db.Integer, default=0)
    date = db.Column(db.DateTime, default=datetime.utcnow)

# Создаем базу данных
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    chapters = Chapter.query.order_by(Chapter.date.desc()).all()
    return render_template_string(open('index.html', 'r', encoding='utf-8').read(), chapters=chapters)

@app.route('/add_chapter', methods=['POST'])
def add_chapter():
    content = request.form['content']
    author = request.form['author']
    
    if content and author:
        new_chapter = Chapter(content=content, author=author)
        db.session.add(new_chapter)
        db.session.commit()
    
    return redirect(url_for('index'))

@app.route('/vote/<int:chapter_id>')
def vote(chapter_id):
    chapter = Chapter.query.get(chapter_id)
    chapter.votes += 1
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)