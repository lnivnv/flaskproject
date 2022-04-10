import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Answers(SqlAlchemyBase):
    __tablename__ = 'Answers'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    is_correct = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    question_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Questions.id"))
    question = orm.relation('Questions')
