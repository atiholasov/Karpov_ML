from ..base_model import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class GeolocationModel(Base):
    __tablename__ = 'geolocation'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
