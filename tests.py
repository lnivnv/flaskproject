import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Tests(SqlAlchemyBase):
    __tablename__ = 'Tests'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    news = orm.relation("questions", back_populates='test')