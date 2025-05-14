from flask_login import UserMixin
from datetime import datetime
from data.db_session import SqlAlchemyBase
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Text, ARRAY


class Chapter(SqlAlchemyBase, UserMixin):
    __tablename__ = 'chapters'

    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey("users.id"))
    state = Column(Integer, default=0)  # 0-первая глава 1-продолжениеб 2-концовка
    votes = Column(Integer, default=0)
    date = Column(DateTime, default=datetime.utcnow)
    content = Column(Text, nullable=False)
    title = Column(Text, nullable=False)
    next = Column(ARRAY(Integer), nullable=True, default=[])

