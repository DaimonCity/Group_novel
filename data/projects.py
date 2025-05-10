from flask_login import UserMixin
from datetime import datetime
from data.db_session import SqlAlchemyBase
from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, Text


class Project(SqlAlchemyBase, UserMixin):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey("users.id"))
    state = Column(Integer, default=0)  # 0-Private 1-Shown 2-Shown + Edit
    votes = Column(Integer, default=0)
    date = Column(DateTime, default=datetime.utcnow)
    title = Column(Text, nullable=False)
    chapter_id = Column(Text, ForeignKey("chapters.id"))
