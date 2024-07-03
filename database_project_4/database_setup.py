import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()

engine = create_engine('sqlite:///restaurantmenu.db')

class Restaurant(Base):
    __tablename__ = 'restaurant'
    name = Column(String(250), nullable=False)
    id = Column(Integer, primary_key = True)

    def __repr__(self):
        return f"{self.id} {self.name}"

class MenuItem(Base):
    __tablename__ = 'menu_item'
    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key = True)
    course = Column(String(250))
    description = Column(String(250))
    price = Column(String(8))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)

    def __repr__(self):
        return f"<MenuItem(name={self.name}, id={self.id}, course={self.course}, description={self.description}, price={self.price}, restaurant_id={self.restaurant_id})>"

Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()