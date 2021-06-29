from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Table

from db import Base, engine


user_trips = Table(
    'user_trips', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('trip_id', Integer, ForeignKey('trips.id'))
)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, unique=True, primary_key=True)
    name = Column(String)
    nickname = Column(String)
    phone_number = Column(String)
    subscribe = Column(Boolean)
    trips = relationship("Trip", secondary=user_trips, back_populates="passengers")  # Many to many with Trip
    cars = relationship("Car", backref="driver")  # One to many with Car

    def __repr__(self):
        return f'User id: {self.id}, name: {self.name}'


class Car(Base):
    __tablename__ = 'cars'

    id = Column(Integer, index=True, unique=True, primary_key=True)
    driver_id = Column(Integer, ForeignKey(User.id))    
    model = Column(String)
    year = Column(String)
    trip = relationship("Trip", back_populates="car", uselist=False)  # One to one with Trip.car

    def __repr__(self):
        return f'Car id: {self.id}'


class Trip(Base):
    __tablename__ = 'trips'

    id = Column(Integer, primary_key=True)
    car_id = Column(Integer, ForeignKey(Car.id))    
    route = Column(String)
    date = Column(Date)
    car = relationship("Car", back_populates="trip", uselist=False)  # One to one with Car.trip
    passengers = relationship("User", secondary=user_trips, back_populates="trips")  # Many to many with User

    def __repr__(self):
        return f'Trip id: {self.id}'


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
