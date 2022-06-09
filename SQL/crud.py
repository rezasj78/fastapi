from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
	return db.query(models.User).filter(models.User.id == user_id).first()


def get_users(db: Session):
	return db.query(models.User).limit(100).all()


def get_user_pass(db: Session, phone_num: int):
	return db.query(models.User).filter(models.User.phone_num == phone_num).first()


def get_user_by_phone(db: Session, phone_num: int):
	return db.query(models.User).filter(models.User.phone_num == phone_num).first()


def get_apartment(db: Session, apartment_id: int):
	return db.query(models.Apartment).filter(models.Apartment.id == apartment_id).first()


def get_apartment_manager(db: Session, manager_id: int):
	return db.query(models.Apartment).filter(models.Apartment.manager_id == manager_id).first()


def create_user(db: Session, user: schemas.UserCreate):
	supposedly_hashed_password = user.password + "think its hashed"
	db_user = models.User(phone_num=user.phone_num, hashed_password=supposedly_hashed_password, home_num=user.home_num,
						  name=user.name, email=user.email)
	db.add(db_user)
	db.commit()
	db.refresh(db_user)
	return db_user
