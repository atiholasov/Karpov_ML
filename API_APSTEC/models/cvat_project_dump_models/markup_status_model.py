from ..base_model import Base
from sqlalchemy import Column, Integer, String


class MarkupStatusModel(Base):
    __tablename__ = 'markup_status'
    id = Column(Integer, primary_key = True)
    name = Column(String)