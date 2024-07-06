from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database_setup import Base, Restaurant, MenuItem

engine = create_engine("sqlite:///restaurantmenu.db")
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# restaurants = session.query(Restaurant).all()
# for restaurant in restaurants:
# #print(f"Menu Item ID: {restaurant.id}, Name: {restaurant.name}, Course: {restaurant.course}, Description: {restaurant.description}, Price: {restaurant.price}, Restaurant ID: {restaurant.restaurant_id}, Ralationship{restaurant.restaurant}")
#     print(f"{restaurant.id} {restaurant.name}")
Results = session.query(Restaurant).all()
for result in Results:
    print(f"{result.id} {result.name}")

menu_items = session.query(MenuItem).all()
for item in menu_items:
    print(f"{item.id} {item.name} {item.course} {item.description} {item.price}")
