from typing import Union

from pydantic import BaseModel


class ApartmentBase(BaseModel):
	name: str
	address: str
	city: str
	state: str
	floor_num: int
	unit_num: int
	manager_id: Union[int, None] = None


class ApartmentCreate(ApartmentBase):
	pass


class Apartment(ApartmentBase):
	id: int

	class Config:
		orm_mode = True


class UserBase(BaseModel):
	phone_num: int
	email: str
	name: str
	home_num: str
	role: int


class UserCreate(UserBase):
	password: str


class User(UserBase):
	id: int
	apartment_id: Union[int, None] = None

	class Config:
		orm_mode = True


class UserUpdate(BaseModel):
	apartment_id: int

	class Config:
		orm_mode = True


class RepairmanBase(BaseModel):
	name: str
	email: str
	phone_num: int
	email: str
	job: str
	state: str
	city: str


class RepairmanCreate(RepairmanBase):
	password: str


class Repairman(RepairmanBase):
	id: int

	class Config:
		orm_mode = True
