from sqlalchemy import Column,Integer,String, Date, ForeignKey, Boolean

from db import Base, engine

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)    
    phone_number = Column(String)    
    subscribe = Column(Boolean)

    def __repr__(self):
        return f'Company id: {self.id}, name: {self.name}'

class Cars(Base):
    __tablename__ = 'cars'

    id = Column(Integer, primary_key=True)
    id_user = Column(Integer, ForeignKey(Users.id), index=True, nullable=False)
    model = Column(String)
    year_of_issue = Column(String)

    def __repr__(self):
        return f'Company id: {self.id}, name: {self.name}'

class Trip(Base):
    __tablename__ = 'trip'

    id = Column(Integer, primary_key=True)
    id_car = Column(Integer, ForeignKey(Cars.id), index=True, nullable=False)
    route = Column(String)
    date = Column(Date)

    def __repr__(self):
        return f'Company id: {self.id}, name: {self.name}'

class Trip_user(Base):
    __tablename__ = 'trip_user'

    id = Column(Integer, primary_key=True)
    id_user = Column(Integer, ForeignKey(Users.id), index=True, nullable=False)
    id_car = Column(Integer, ForeignKey(Cars.id), index=True, nullable=False)

    def __repr__(self):
        return f'Company id: {self.id}, name: {self.name}'