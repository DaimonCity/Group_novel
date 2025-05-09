# from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, Text
# from flask_login import UserMixin
# from  datetime import datetime
# from data.db_session import SqlAlchemyBase
#
#
# class InfoChapter(SqlAlchemyBase, UserMixin):
#     __tablename__ = 'info_chapters'
#
#     id = Column(Integer, primary_key=True, ForeignKey=ForeignKey('chapters.id'))
#     author_id = Column(String, nullable=False, ForeignKey=ForeignKey('users.id'))
#     state = Column(Integer, default=0, ForeignKey=ForeignKey('state.id')) # 0-первая глава 1-продолжениеб 2-концовка
#     votes = Column(Integer, default=0, ForeignKey=ForeignKey('votes.id'))
#     date = Column(DateTime, default=datetime.utcnow, ForeignKey=ForeignKey('date.id'))
#
#     content = Column(Text, nullable=False)
#     # next = Column(Text, nullable=False)