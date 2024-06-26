#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel
from models.city import City
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import models

Base = declarative_base()

class State(BaseModel, Base):
    """ State class """
    __tablename__ = "state"
    name = Column(String(128), nullable=False)
    if models.storage_type == 'db':
        cities = relationship('City', backref='state', cascade='all, delete, delete-orphan')
    else:
        @property
        def cities(self):
            """Getter attribute to return the list of City instances with state_id equals to the current State.id"""
            city_list = []
            for city in models.storage.all(City).values():
                if city.state_id == self.id:
                    city_list.append(city)
            return city_list
