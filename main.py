from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/')
@app.route('/base')
def base():
    return render_template("base.html", title='Mars?')


@app.route('/home')
def index():
    return render_template('homepage.html')


if __name__ == '__main__':
    app.run(port=5000, host='127.0.0.1')