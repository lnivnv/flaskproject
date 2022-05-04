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

is_login_in_private_office = False
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
result_test = 0
title_test = ''
username = ''


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
@app.route('/home')
def index():
    return render_template('home.html')


@app.route('/private office')
def private_office():
    if is_login_in_private_office:
        con = sqlite3.connect("users.db")
        cur = con.cursor()
        result_private_office = cur.execute("""SELECT * FROM users WHERE username = ?""", [username, ])
        for elem in result_private_office:
            param = {}
            param['username'] = elem[3]
            param['name'] = elem[1]
            param['email'] = elem[2]
            param['picture'] = elem[5]
            return render_template('private office.html', **param)
    else:
        return f'<h1>Вам надо зарегистрироваться или авторизоваться!</h1>'


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/result')
def result():
    return render_template('result.html', title=title_test, result=result_test)


@app.route('/tests')
def tests():
    return render_template('tests.html', tests=Tests)


@app.route('/test/<title>', methods=["POST", "GET"])
def test(title):
    if request.method == 'GET':
        global title_test
        title_test = title
        return render_template('test.html', title=title, tests=Tests, Question=Question, answer=Answer)
    elif request.method == 'POST':
        users_ans, users_answers = [], []
        for answers in Answer:
            is_clicked = request.form.get(str(answers["question_id"]))
            if is_clicked == answers["title"]:
                users_ans.append(is_clicked)
                users_answers.append(answers["is_correct"])
        global result_test
        result_test = users_answers.count(True)
        return redirect('/result')


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
        global username
        username = request.form['username']
        password_candidate = request.form['password']
        con = sqlite3.connect("users.db")
        cur = con.cursor()
        result_login = cur.execute("""SELECT * FROM users WHERE username = ?""", [username, ])
        if result_login:
            data = cur.fetchone()
            password = data[4]
            if sha256_crypt.verify(password_candidate, password):
                global is_login_in_private_office
                is_login_in_private_office = True
                session['logged_in'] = True
                session['username'] = username
                flash('You are now logged in', 'success')
                return redirect('/home')
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
    global is_login_in_private_office
    is_login_in_private_office = False
    session.clear()
    flash('You are now logged out', 'success')
    return redirect('/home')


if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(port=5000, host='127.0.0.1')
