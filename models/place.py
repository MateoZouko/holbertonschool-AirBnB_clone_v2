#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from os import getenv
from sqlalchemy.orm import relationship

place_amenity = Table('place_amenity', Base.metadata,
                              Column('place_id', String(60),
                                     ForeignKey('places.id'),
                                     primary_key=True, nullable=False),
                              Column('amenity_id', String(60),
                                     ForeignKey('amenities.id'),
                                     primary_key=True, nullable=False))

class Place(BaseModel):
    """ A place to stay """

    __tablename__ = 'places'

    if getenv("HBNB_TYPE_STORAGE") == "db":
        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        amenity_ids = []
        reviews = relationship("Review", backref="place", cascade="all, delete-orphan")
        amenities = relationship("Amenity", secondary=place_amenity, viewonly=False)
    else:
        @property
        def reviews(self):
            """Getter attribute reviews that returns the list of Review instances
            with place_id equals to the current Place.id"""
            review_list = []
            for review in models.storage.all(Review).values():
                if review.place_id == self.id:
                    review_list.append(review)
            return review_list

        @property
        def amenities(self):
            """Getter attribute amenities that returns the list of Amenity instances
            with amenity_id equals to the current Place.id"""
            amenity_list = []
            for amenity_id in self.amenity_ids:
                amenity = models.storage.get(Amenity, amenity_id)
                if amenity:
                    amenity_list.append(amenity)
            return amenity_list

        @amenities.setter
        def amenities(self, amenity):
            """Setter attribute amenities that handles append method
            for adding an Amenity.id to the attribute amenity_ids"""
            if isinstance(amenity, Amenity):
                self.amenity_ids.append(amenity.id)