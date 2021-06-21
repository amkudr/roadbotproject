from sqlalchemy import Column,Integer,String, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Table

from db import Base, engine


# user_trips = UserTrip('user_trip',
#         Column('user_id', Integer, ForeignKey('users.id')),
#         Column('trip_id', Integer, ForeignKey('trips.id'))
# )

user_trips = Table('user_trips', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('trip_id', Integer, ForeignKey('trips.id'))
)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)    
    phone_number = Column(String)    
    subscribe = Column(Boolean)
    trips = relationship("Trip", secondary = user_trips) #Many to many with Trip
    car = relationship("Car", backref="driver") #One to many with Car

    def __repr__(self):
        return f'User id: {self.id}, name: {self.name}'

class Car(Base):
    __tablename__ = 'cars'

    id = Column(Integer, primary_key=True)
    driver = Column(Integer, ForeignKey(User.id), index=True, nullable=False)    
    model = Column(String)
    year_of_issue = Column(String)
    trip = relationship("Trip", back_populates="car", uselist=False) #One to one with Trip.car

    def __repr__(self):
        return f'Car id: {self.id}'

class Trip(Base):
    __tablename__ = 'trips'

    id = Column(Integer, primary_key=True)
    car_id = Column(Integer, ForeignKey(Car.id), index=True, nullable=False)    
    route = Column(String)
    date = Column(Date)
    car = relationship("Car", back_populates="trip", uselist=False) #One to one with Car.trip
    passengers = relationship("User", secondary = user_trips) #Many to many with User

    def __repr__(self):
        return f'Trip id: {self.id}'

# class UserTrip(Base):
#     __tablename__ = 'user_trip'

#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer, ForeignKey(User.id), index=True, nullable=False)    
#     trip_id = Column(Integer, ForeignKey(Trip.id), index=True, nullable=False)

#     def __repr__(self):
#         return f'Trip_user id: {self.id}'


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)

