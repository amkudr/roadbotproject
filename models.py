from sqlalchemy import Column,Integer,String, Date, ForeignKey, Boolean

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
    user_id = Column(Integer, ForeignKey(User.id), index=True, nullable=False)
    model = Column(String)
    year_of_issue = Column(String)

    def __repr__(self):
        return f'Car id: {self.id}'

class Trip(Base):
    __tablename__ = 'trip'

    id = Column(Integer, primary_key=True)
    car_id = Column(Integer, ForeignKey(Car.id), index=True, nullable=False)
    route = Column(String)
    date = Column(Date)

    def __repr__(self):
        return f'Trip id: {self.id}'

class Trip_user(Base):
    __tablename__ = 'trip_user'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id), index=True, nullable=False)
    car_id = Column(Integer, ForeignKey(Car.id), index=True, nullable=False)

    def __repr__(self):
        return f'Trip_user id: {self.id}'