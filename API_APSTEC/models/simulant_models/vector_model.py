from ..base_model import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class VectorModel(Base):
    __tablename__ = 'vector'
    id = Column(Integer, primary_key = True)
    name = Column(String, unique=True)