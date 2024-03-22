from database import Base, SessionLocal
from sqlalchemy import Column, Integer, String, desc, func, TIMESTAMP, ForeignKey


class Post(Base):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True)
    text = Column(String)
    topic = Column(String)


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    gender = Column(Integer)
    age = Column(Integer)
    country = Column(String)
    city = Column(String)
    exp_group = Column(Integer)
    os = Column(String)
    source = Column(String)


class Feed(Base):
    __tablename__ = "feed_action"
    action = Column(String, primary_key=True)
    post_id = Column(
        Integer, ForeignKey('post.id'))
    time = Column(TIMESTAMP)
    user_id = Column(
        Integer, ForeignKey("user.id"))


"""
if __name__ == "__main__":
    session = SessionLocal()
    out = (session.query(User.country, User.os, func.count(User.id))
           .filter(User.exp_group == 3)
           .group_by(User.country, User.os)
           .order_by(desc(func.count(User.id)))
           .having(func.count(User.id) > 100)
           .all())

    answer = []
    for elem in out:
        answer.append(elem)

    print(answer)
"""
