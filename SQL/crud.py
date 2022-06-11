from sqlalchemy.orm import Session

from . import models, schemas


# USER STUFF ###################################
def get_user(db: Session, user_id: int):
	return db.query(models.User).filter(models.User.id == user_id).first()


def get_users(db: Session):
	return db.query(models.User).limit(100).all()


def get_user_by_phone(db: Session, phone_num: int):
	return db.query(models.User).filter(models.User.phone_num == phone_num).first()


def create_user(db: Session, user: schemas.UserCreate):
	supposedly_hashed_password = user.password + "think its hashed"
	db_user = models.User(phone_num=user.phone_num, hashed_password=supposedly_hashed_password, home_num=user.home_num,
						  role=user.role, name=user.name, email=user.email)
	db.add(db_user)
	db.commit()
	db.refresh(db_user)
	return db_user


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


# REPAIRMAN STUFF ###########################
def get_repairman_by_phone(db: Session, phone_num: int):
	return db.query(models.Repairman).filter(models.Repairman.phone_num == phone_num).first()


def get_repairman(db: Session, repairman_id):
	return db.query(models.Repairman).filter(models.Repairman.id == repairman_id).first()


def create_repairman(db: Session, repairman: schemas.RepairmanCreate):
	supposedly_hashed_password = repairman.password + "think its hashed"
	db_repairman = models.Repairman(name=repairman.name, phone_num=repairman.phone_num,
									hashed_password=supposedly_hashed_password,
									email=repairman.email, job=repairman.job, state=repairman.state,
									city=repairman.city)
	db.add(db_repairman)
	db.commit()
	db.refresh(db_repairman)
	return db_repairman


# APARTMENT STUFF ######################

def get_apartment_by_manager(db: Session, phone_num: int):
	manager = get_user_by_phone(db=db, phone_num=phone_num)
	if manager is None:
		return None
	if manager.role == 0:
		return 0
	print(manager.id)
	db_apartment = db.query(models.Apartment).filter(models.Apartment.manager_id == manager.id).first()
	if db_apartment is None:
		return 1
	return db_apartment


def get_apartment_by_user(db: Session, user_phone):
	user = get_user_by_phone(db=db, phone_num=user_phone)
	if user is None:
		return None
	ap_id = user.apartment_id
	if ap_id is None:
		return 0
	return db.query(models.Apartment).filter(models.Apartment.id == ap_id).first()


def get_apartment(db: Session, apartment_id: int):
	return db.query(models.Apartment).filter(models.Apartment.id == apartment_id).first()


def creat_apartment(db: Session, apartment: schemas.ApartmentCreate):
	db_apartment = models.Apartment(name=apartment.name, address=apartment.address, city=apartment.city,
									state=apartment.state, floor_num=apartment.floor_num, unit_num=apartment.unit_num,
									manager_id=apartment.manager_id)
	db.add(db_apartment)
	db.commit()
	db.refresh(db_apartment)
	return db_apartment

# def get_repairmens_for_apartment(db: Session, apartment_id: int):
# 	return db.query(models.ApartmentAndRepairmen).filter(
# 		models.ApartmentAndRepairmen.apartment_id == apartment_id).all()
#

# def get_apartments_for_repairman(db: Session, repairman_id: int):
# 	return db.query(models.ApartmentAndRepairmen).filter(
# 		models.ApartmentAndRepairmen.repairman_id == repairman_id).all()
