from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
	return db.query(models.User).filter(models.User.id == user_id).first()


def get_users(db: Session):
	return db.query(models.User).limit(100).all()


def get_user_by_phone(db: Session, phone_num: int):
	return db.query(models.User).filter(models.User.phone_num == phone_num).first()


def get_apartment(db: Session, apartment_id: int):
	return db.query(models.Apartment).filter(models.Apartment.id == apartment_id).first()


def get_apartment_by_manager(db: Session, manager_id: int):
	return db.query(models.Apartment).filter(models.Apartment.manager_id == manager_id).first()


def get_apartments_for_repairman(db: Session, repairman_id: int):
	return db.query(models.ApartmentAndRepairmen).filter(
		models.ApartmentAndRepairmen.repairman_id == repairman_id).all()


def update_user_apartment(db: Session, phone_num, user: schemas.UserUpdate):
	db_user = get_user_by_phone(db, phone_num=phone_num)
	if db_user is None:
		return None
	user_data = user.dict()
	for key, value in user_data.items():
		setattr(db_user, key, value)
	db.add(db_user)
	db.commit()
	return db_user


def create_user(db: Session, user: schemas.UserCreate):
	supposedly_hashed_password = user.password + "think its hashed"
	db_user = models.User(phone_num=user.phone_num, hashed_password=supposedly_hashed_password, home_num=user.home_num,
						  name=user.name, email=user.email)
	db.add(db_user)
	db.commit()
	db.refresh(db_user)
	return db_user


def get_repairman_by_phone(db: Session, phone_num: int):
	return db.query(models.Repairman).filter(models.Repairman.phone_num == phone_num).first()


def create_repairman(db: Session, repairman: schemas.RepairmanCreate):
	supposedly_hashed_password = repairman.password + "think its hashed"
	db_repairman = models.Repairman(name=repairman.name, phone_num=repairman.phone_num,
							   hashed_password=supposedly_hashed_password,
							   email=repairman.email, job=repairman.job, state=repairman.state, city=repairman.city)
	db.add(db_repairman)
	db.commit()
	db.refresh(db_repairman)
	return db_repairman


def get_repairmen_for_apartments(db: Session, apartment_id: int):
	return db.query(models.ApartmentAndRepairmen).filter(
		models.ApartmentAndRepairmen.apartment_id == apartment_id).all()
