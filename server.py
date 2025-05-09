import flask_login
import sqlalchemy
from flask import Flask, render_template, request, redirect, url_for
from bs4 import BeautifulSoup
from flask_login import login_user, login_required, logout_user, UserMixin, LoginManager
from forms.user import RegisterForm
from forms.login import LoginForm
from data import db_session
from data.users import User
from data.chapters import Chapter
from data.Сontinue_chapters import Сontinue_chapters

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
def index():
    db_sess = db_session.create_session()
    chapters = [char for char in db_sess.query(Chapter).all() if char.state == 0]
    return render_template('index.html', chapters=chapters)


@app.route('/edit')
def editor():
    return render_template('docs2.html')


@app.route('/continue_chapter/<int:chapter_id>')
def continue_chapter(chapter_id):
    db_sess = db_session.create_session()
    chapter = db_sess.query(Chapter).get(chapter_id)
    print(db_sess.query(Сontinue_chapters).get().all())
    add_chapter()
    chapter.continues_id.append()

    db_sess.commit()
    return redirect(url_for('index'))


@app.route('/add_chapter', methods=['POST'])
def add_chapter():
    db_sess = db_session.create_session()
    content = request.form['content']
    author_id = flask_login.current_user.id

    if content and author_id:
        new_chapter = Chapter(content=content, author_id=author_id)
        db_sess.add(new_chapter)
        db_sess.query(Сontinue_chapters).add_column(sqlalchemy.Column(sqlalchemy.Integer))
        db_sess.commit()

    return redirect(url_for('index'))


@app.route('/vote/<int:chapter_id>')
def vote(chapter_id):
    db_sess = db_session.create_session()
    chapter = db_sess.query(Chapter).get(chapter_id)
    chapter.votes += 1
    db_sess.commit()
    return redirect(url_for('index'))


@app.route('/publish_chapter', methods=['POST'])
def publish_chapter():
    raw_content = request.form['content']
    author = request.form['author']


    # Очистка HTML (опционально)
    clean_content = BeautifulSoup(raw_content, "html.parser").get_text()
    if clean_content and author:
        db_sess = db_session.create_session()
        new_chapter = Chapter(content=clean_content, author=author)
        db_sess.add(new_chapter)
        db_sess.commit()
        # Очищаем localStorage после успешной отправки
        return redirect(url_for('editor'))
    return "Ошибка: текст или автор не указаны", 400


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html',
                                   title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html',
                                   title='Регистрация',
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
    return render_template('login.html',
                           title='Авторизация',
                           form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == '__main__':
    print(id)
    db_session.global_init("db/main.db")
    app.run(debug=True)
