import sqlalchemy
from flask_login import UserMixin
from  datetime import datetime
from data.db_session import SqlAlchemyBase


class Chapter(SqlAlchemyBase, UserMixin):
    __tablename__ = 'chapters'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    content = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    author = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    votes = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.utcnow)
    state = sqlalchemy.Column(sqlalchemy.Integer, default=0) # 0-первая глава 1-продолжениеб 2-концовка