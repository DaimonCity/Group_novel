import flask_login
from flask import Flask, render_template, request, redirect, url_for
from flask_login import login_user, login_required, logout_user, LoginManager
from forms.user import RegisterForm
from forms.login import LoginForm
from data import db_session, chapters
from data.users import User
from data.chapters import Chapter
from data.projects import Project

# from data.Сontinue_chapters import Сontinue_chapters

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
    return render_template('index.html', chapters=chapters, title='Лента')

@app.route('/edit/<int:chapter_id>')
def edit(chapter_id):
    db_sess = db_session.create_session()
    chapter = db_sess.query(Chapter).get(chapter_id)
    return render_template('docs.html', chapter=chapter)


@app.route('/continue_chapter/<int:chapter_id>')
def continue_chapter(chapter_id):
    db_sess = db_session.create_session()
    chapter = db_sess.query(Chapter).get(chapter_id)
    add_chapter()
    chapter.continues_id.append()

    db_sess.commit()
    return render_template('index')


@app.route('/add_chapter/<int:chapter_id>', methods=['POST'])
def add_chapter(chapter_id):
    db_sess = db_session.create_session()
    content = request.form['content']
    print(content)
    author_id = flask_login.current_user.id

    if content and author_id:
        print(content)
        db_sess.query(Chapter).get(chapter_id).content = content
        db_sess.commit()

    return redirect(url_for('personal', user_id=author_id))


@app.route('/vote/<int:chapter_id>')
def vote(chapter_id):
    db_sess = db_session.create_session()
    chapter = db_sess.query(Chapter).get(chapter_id)
    chapter.votes += 1
    db_sess.commit()
    return redirect(url_for('index'))


@app.route('/publish_chapter', methods=['POST'])
def publish_chapter():
    content = request.form['content']
    name = request.form['name']
    author_id = flask_login.current_user.id

    if content and author_id:
        db_sess = db_session.create_session()
        new_chapter = Chapter(content=content, author_id=author_id, title=name)
        db_sess.add(new_chapter)
        db_sess.commit()
        # Очищаем localStorage после успешной отправки
        return redirect(url_for('edit'))
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


@app.route('/profile/<int:id>')
@login_required
def profile(id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(id)
    return render_template('profile.html', user=user, title=f"{user.name}'s Profile")


@app.route('/redact')
@login_required
def redact():
    # db_sess = db_session.create_session()
    # user = db_sess.query(User).get(id)
    form = RegisterForm()
    return render_template('redact.html', title=f"redact rofile", form=form)


@app.route('/save_redact/<string:name><string:about>')
@login_required
def save_redact(name, about):
    db_sess = db_session.create_session()
    # user_id = flask_login.current_user.id
    print(name, about, '!!!!!!')
    # if name:
    #     db_sess.query(`User`).get(user_id).update({'name': name})
    # if about:
    #     db_sess.query(User).get(user_id).update({'about': about})
    db_sess.commit()
    # return redirect(url_for('profile', id=user_id))


@app.route('/read/<int:chapter_id>')
def read(chapter_id):
    db_sess = db_session.create_session()
    chapter = db_sess.query(Chapter).get(chapter_id)
    return render_template('read_chapter.html', title=chapter.title, chapter=chapter)


@app.route('/personal/<int:user_id>')
@login_required
def personal(user_id):
    db_sess = db_session.create_session()
    projects = [proj for proj in db_sess.query(Project).filter(Project.author_id == user_id)]
    projects = [projects[i:i + 3] for i in range(0, len(projects), 3)]
    print(projects)
    if len(projects) == 0:
        return render_template('personal.html', user_id=user_id, projects=0)
    return render_template('personal.html', user_id=user_id, projects=projects)
    # except Exception as e:
    #     return render_template('personal.html', user=user, projects=0)


@app.route("/make_project", methods=['POST'])
@login_required
def make_project():
    curent_user_id = flask_login.current_user.id
    db_sess = db_session.create_session()
    title = request.form['title']
    if title:
        new_chapter = Chapter(author_id=curent_user_id, title=title, content='')
        db_sess.add(new_chapter)
        db_sess.commit()
        new_project = Project(author_id=curent_user_id, title=title, chapter_id=new_chapter.id)
        db_sess.add(new_project)
        db_sess.commit()
        return redirect(url_for('personal', user_id=curent_user_id))
    return redirect('/')

# @app.route("/open_table/<int:chapter_id>", methods=['POST'])
# @login_required
# def open_table(chapter_id):
#     tree = chapter_tree(chapter_id)
#     return redirect('/table', tree=tree)
#
# def chapter_tree(chapter_id):
#     tree = dict()
#     db_sess = db_session.create_session()
#     chapter = db_sess.query(Chapter).get(chapter_id)
#     if chapter.next:
#         for i in chapter.next:
#             if tree[chapter_id]:
#                 tree[chapter_id].append(chapter_tree(i))
#             else:
#                 tree[chapter_id] = [chapter_tree(i)]
#     return tree


if __name__ == '__main__':
    db_session.global_init("db/main.db")
    app.run(debug=True)
