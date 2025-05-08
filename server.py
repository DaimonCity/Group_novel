from flask import Flask, render_template, request, redirect, url_for, render_template_string
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from bs4 import BeautifulSoup
from flask_login import LoginManager, login_user, login_required, logout_user
from data.users import User
from forms.user import RegisterForm
from forms.login import LoginForm

from data import db_session
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///novel.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

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

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)

@app.route('/')
def index():
    chapters = Chapter.query.order_by(Chapter.date.desc()).all()
    return render_template('index.html', chapters=chapters)


@app.route('/edit')
def editor():
    return render_template('docs.html')


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


@app.route('/publish_chapter', methods=['POST'])
def publish_chapter():
    raw_content = request.form['content']
    author = request.form['author']

    # Очистка HTML (опционально)
    clean_content = BeautifulSoup(raw_content, "html.parser").get_text()
    print(clean_content)
    if clean_content and author:
        new_chapter = Chapter(content=clean_content, author=author)
        db.session.add(new_chapter)
        db.session.commit()
        # Очищаем localStorage после успешной отправки
        return redirect(url_for('editor'))

    return "Ошибка: текст или автор не указаны", 400

@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == '__main__':
    db_session.global_init("db/blogs.db")
    app.run(debug=True)
