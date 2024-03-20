from sqlalchemy import Column, Integer, String, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# NOTE be careful when sharing
# SQLALCHEMY_DATABASE_URL = "postgresql://username:password@localhost/database"
SQLALCHEMY_DATABASE_URL = "postgresql://robot-startml-ro:pheiph0hahj1Vaif@postgres.lab.karpov.courses:6432/startml"

# создаём engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)
# настройка класса Session c требуемыми настройками
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    age = Column(Integer)
    sex = Column(Boolean)


if __name__ == "__main__":
    Base.metadata.create_all(engine)
