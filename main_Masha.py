from flask import Flask
import db_session
from tests import Tests
from questions import Questions
from answers import Answers
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def test():
    db_session.global_init("tests.db")
    with open('tests.csv', encoding="utf8") as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='"')
        for index, row in enumerate(reader):
            tests = Tests()
            tests.title = row[0]
            db_sess = db_session.create_session()
            db_sess.add(tests)
            db_sess.commit()
    csvfile.close()
    tests = Tests()


def question():
    db_session.global_init("tests.db")
    with open('questions.csv', encoding="utf8") as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='"')
        for index, row in enumerate(reader):
            questions = Questions()
            if index < 5:
                questions.test_id = 1
                questions.picture = row[1]
            elif index < 17:
                questions.test_id = 2
            else:
                questions.test_id = 3
            questions.title = row[0]
            db_sess = db_session.create_session()
            db_sess.add(questions)
            db_sess.commit()
    csvfile.close()


def answer():
    db_session.global_init("tests.db")
    with open('answers.csv', encoding="utf8") as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='"')
        period = 0
        questionid = 1
        for index, row in enumerate(reader):
            if period == 4:
                period = 0
                questionid += 1
            if period < 4:
                db_sess = db_session.create_session()
                if row[1] == 'False':
                    answers = Answers(title=row[0], is_correct=False, question_id=questionid)
                    db_sess.add(answers)
                    db_sess.commit()
                else:
                    answers = Answers(title=row[0], is_correct=True, question_id=questionid)
                    db_sess.add(answers)
                    db_sess.commit()
                period += 1
    csvfile.close()


def tests_tests():
    tests = []
    info = {}
    db_sess = db_session.create_session()
    s = 0
    for test_in in db_sess.query(Tests).all():
        info['id'] = test_in.id
        info['title'] = test_in.title
        tests.append(info)
        info = {}
    return tests[0:3]


def tests_questions():
    questions = []
    info = {}
    db_sess = db_session.create_session()
    for test_in in db_sess.query(Questions).all():
        info['id'] = test_in.id
        info['title'] = test_in.title
        info['test_id'] = test_in.test_id
        info['picture'] = test_in.picture
        questions.append(info)
        info = {}
    return questions[0:23]


def tests_answers():
    answers = []
    info = {}
    db_sess = db_session.create_session()
    for test_in in db_sess.query(Answers).all():
        info['id'] = test_in.id
        info['title'] = test_in.title
        info['question_id'] = test_in.question_id
        info['is_correct'] = test_in.is_correct
        answers.append(info)
        info = {}
    return answers[0:95]


test()
question()
answer()
tests_questions()
tests_answers()
