from flask import Flask, render_template, flash, redirect, url_for, session, request
from main_Masha import tests_tests, tests_questions, tests_answers
import sqlite3
import os
from wtforms import Form, StringField, PasswordField, validators, EmailField
import email_validator
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired, Email
from passlib.hash import sha256_crypt
from functools import wraps

app = Flask(__name__)

Tests = tests_tests()
Question = tests_questions()
Answer = tests_answers()
UPLOAD_FOLDER = 'static/img/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'myflaskapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
@app.route('/home')
def index():
    return render_template('home.html')


@app.route('/private office')
def private_office():
    return render_template('private office.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/result')
def result():
    return render_template('result.html', tests=Tests, Question=Question, answer=Answer)


@app.route('/tests')
def tests():
    return render_template('tests.html', tests=Tests)


@app.route('/test/<title>', methods=["POST", "GET"])
def test(title):
    if request.method == 'GET':
        return render_template('test.html', title=title, tests=Tests, Question=Question, answer=Answer)
    elif request.method == 'POST':
        k, users_ans, users_answers = [], [], []
        for q in Answer:
            h = request.form.get(str(q["question_id"]))
            if h == q["title"]:
                users_ans.append(h)
                users_answers.append(q["is_correct"])
        print(users_answers)
        print(users_answers.count(True))
        return f'Your result in test "{title}" - {users_answers.count(True)} right answers!'


class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = EmailField("Email", validators=[InputRequired("Please enter your email address."),
                                            Email("Please enter your email address.")])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.hash(str(form.password.data))
        picture = request.files['file']
        # picture = picture.filename
        # picture = str(picture)
        # picture = picture[picture.index(':') + 3:]
        # picture = picture[:picture.index("'")]
        if picture.filename != '' and allowed_file(picture.filename):
            con = sqlite3.connect("users.db")
            cur = con.cursor()
            try:
                cur.execute("""INSERT INTO users(name, email, username, password, picture) VALUES(?, ?, ?, ?, ?)""",
                            (name, email, username, password, picture.filename))
                con.commit()
                con.close()
                picture.save(os.path.join(app.config['UPLOAD_FOLDER'], picture.filename))
                return redirect(url_for('login'))
            except Exception as e:
                error = 'Неправильно введены данные'
                return render_template('register.html', form=form, error=error)
        else:
            error = 'Добавьте изображение'
            return render_template('register.html', form=form, error=error)
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password_candidate = request.form['password']
        con = sqlite3.connect("users.db")
        cur = con.cursor()
        result = cur.execute("""SELECT * FROM users WHERE username = ?""", [username, ])
        if result:
            data = cur.fetchone()
            password = data[4]
            if sha256_crypt.verify(password_candidate, password):
                session['logged_in'] = True
                session['username'] = username
                flash('You are now logged in', 'success')
                return redirect('/private office')
            else:
                error = 'Invalid login or password'
                return render_template('login.html', error=error)
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)
    return render_template('login.html')


def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('home'))

    return wrap


@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect('/home')


if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(port=8080, host='127.0.0.1')
