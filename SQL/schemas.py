from typing import Union

from pydantic import BaseModel


class ApartmentBase(BaseModel):
	name: str
	address: str
	city: str
	state: str
	floor_num: int
	unit_num: int
	manager_id: int


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
