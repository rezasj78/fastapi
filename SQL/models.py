from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .databases import Base


# 1 is manager,  0 is normal resident
class User(Base):
	__tablename__ = 'user'

	id = Column(Integer, primary_key=True, index=True)
	name = Column(String)
	hashed_password = Column(String)
	email = Column(String, unique=True, index=True)
	home_num = Column(String, unique=True, index=True)
	phone_num = Column(Integer, unique=True, index=True)
	role = Column(Integer, default=1)
	apartment_id = Column(Integer, ForeignKey('apartment.id'), default=None)


class Repairman(Base):
	__tablename__ = 'repairman'

	id = Column(Integer, primary_key=True, index=True)
	name = Column(String, index=True)
	hashed_password = Column(String)
	phone_num = Column(Integer, unique=True, index=True)
	email = Column(String, unique=True, index=True)
	job = Column(String, index=True)
	state = Column(String, index=True)
	city = Column(String, index=True)


class Apartment(Base):
	__tablename__ = 'apartment'

	id = Column(Integer, primary_key=True, index=True)
	name = Column(String, index=True)
	state = Column(String)
	city = Column(String)
	address = Column(String)
	floor_num = Column(Integer)
	unit_num = Column(Integer)
	manager_id = Column(Integer, ForeignKey('user.id'), default=None)


class ApartmentAndRepairmen(Base):
	__tablename__ = "apartment_and_Repairmen"

	id = Column(Integer, primary_key=True, index=True)
	repairman_id = Column(Integer, ForeignKey('repairman.id'), default=None)
	apartment_id = Column(Integer, ForeignKey('apartment.id'), default=None)
