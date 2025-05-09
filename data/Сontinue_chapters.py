import sqlalchemy
from flask_login import UserMixin
from data.db_session import SqlAlchemyBase


class Сontinue_chapters(SqlAlchemyBase, UserMixin):
    __tablename__ = 'continue_chapters'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)