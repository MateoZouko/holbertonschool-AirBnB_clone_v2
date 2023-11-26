#!/usr/bin/python3
"""State Module for HBNB project"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

class State(BaseModel, Base):
    """State class"""

    __tablename__ = 'states'

    name = Column(String(128), nullable=False)
    cities = relationship("City", backref="state", cascade="all, delete-orphan")

    @property
    def cities(self):
        """Getter attribute to return a list of City instances with state_id equals to the current State.id"""
        from models import storage
        cities_list = []
        for key, value in storage.all(City).items():
            if value.state_id == self.id:
                cities_list.append(value)
        return cities_list