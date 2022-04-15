import sqlalchemy
from sqlalchemy import orm
from db_session import SqlAlchemyBase


class Questions(SqlAlchemyBase):
    __tablename__ = 'Questions'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    picture = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    test_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Tests.id"))
    test = orm.relation('Tests')
    answers = orm.relation("Answers", back_populates='question')
