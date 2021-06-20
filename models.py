from sqlalchemy import Column,Integer,String, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from db import Base, engine

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)    
    phone_number = Column(String)    
    subscribe = Column(Boolean)

    def __repr__(self):
        return f'User id: {self.id}, name: {self.name}'

class Car(Base):
    __tablename__ = 'cars'

    id = Column(Integer, primary_key=True)
    driver_id = Column(Integer, ForeignKey(User.id), index=True, nullable=False)
    user = relationship("User", backref="cars")
    model = Column(String)
    year_of_issue = Column(String)

    def __repr__(self):
        return f'Car id: {self.id}'

class Trip(Base):
    __tablename__ = 'trip'

    id = Column(Integer, primary_key=True)
    car_id = Column(Integer, ForeignKey(Car.id), index=True, nullable=False)
    car = relationship("Car", backref="trips")
    route = Column(String)
    date = Column(Date)

    def __repr__(self):
        return f'Trip id: {self.id}'

class User_trip(Base):
    __tablename__ = 'trip_user'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id), index=True, nullable=False)
    user = relationship("User", backref="user_trips")
    trip_id = Column(Integer, ForeignKey(Trip.id), index=True, nullable=False)
    trip = relationship("Trip", backref="user_trips")

    def __repr__(self):
        return f'Trip_user id: {self.id}'


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)

