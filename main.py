from typing import List
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from SQL import crud, models, schemas
from SQL.databases import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


#  SCHEMA FOR LOGGING IN
class verify(BaseModel):
	phone: int
	password: str


# dependency

def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()


# ENDPOINT FOR USERS
@app.post("/user", response_model=schemas.User)
def creat_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
	db_user = crud.get_user_by_phone(db, phone_num=user.phone_num)
	if db_user:
		raise HTTPException(status_code=404, detail="phone number already exists")
	return crud.create_user(db, user)


@app.post('/user/login', response_model=schemas.User)
def login(user: verify, db: Session = Depends(get_db)):
	db_user = crud.get_user_by_phone(db=db, phone_num=user.phone)
	if db_user:
		if db_user.hashed_password == (user.password + "think its hashed"):
			return db_user
		else:
			raise HTTPException(status_code=404, detail="wrong pass or phone")
	else:
		raise HTTPException(status_code=404, detail="wrong pass or phone")


@app.patch('/user/{phone_num}', response_model=schemas.User)
def update_user(user: schemas.UserUpdate, phone_num: int, db: Session = Depends(get_db)):
	db_user = crud.update_user_apartment(db=db, user=user, phone_num=phone_num)
	if db_user is None:
		raise HTTPException(status_code=404, detail="user not found")
	return db_user


@app.get("/users", response_model=List[schemas.User])
def get_users(db: Session = Depends(dependency=get_db)):
	users = crud.get_users(db)
	return users


@app.get('/user/{phone_num}', response_model=schemas.User)
def get_user(phone_num: int, db: Session = Depends(get_db)):
	db_user = crud.get_user_by_phone(db=db, phone_num=phone_num)
	if db_user is None:
		raise HTTPException(status_code=404, detail="user not found")
	return db_user


@app.get('/users/{apartment_id}', response_model=List[schemas.User])
def get_users_by_apartment(apartment_id, db: Session = Depends(get_db)):
	users = crud.get_users_by_apartment(db, apartment_id)
	if users is None:
		raise HTTPException(status_code=404, detail='no user was found for this apartment')
	return users


# ENDPOINT FOR REPAIRMAN
@app.post("/repairmen", response_model=schemas.Repairman)
def creat_repairman(repairman: schemas.RepairmanCreate, db: Session = Depends(get_db)):
	db_repairman = crud.get_repairman_by_phone(db, phone_num=repairman.phone_num)
	if db_repairman:
		raise HTTPException(status_code=404, detail="phone number already exists")
	return crud.create_repairman(db, repairman)


@app.post('/repairman/login', response_model=schemas.Repairman)
def login(repairman: verify, db: Session = Depends(get_db)):
	db_repairman = crud.get_repairman_by_phone(db=db, phone_num=repairman.phone)
	if db_repairman:
		if db_repairman.hashed_password == (repairman.password + "think its hashed"):
			return db_repairman
		else:
			raise HTTPException(status_code=404, detail="wrong pass or phone")
	else:
		raise HTTPException(status_code=404, detail="wrong pass or phone")


@app.get('/repairman/{phone_num}', response_model=schemas.Repairman)
def get_repairman(phone_num: int, db: Session = Depends(get_db)):
	db_repairman = crud.get_repairman_by_phone(db=db, phone_num=phone_num)
	if db_repairman is None:
		raise HTTPException(status_code=404, detail="user not found")
	return db_repairman


# ENDPOINT FOR APARTMENT
@app.post('/apartment', response_model=schemas.Apartment)
def create_apartment(apartment: schemas.ApartmentCreate, db: Session = Depends(get_db)):
	return crud.creat_apartment(db, apartment=apartment)


@app.get('/manager/apartment/{phone_num}', response_model=schemas.Apartment)
def get_apartment_by_manager(phone_num: int, db: Session = Depends(get_db)):
	apartment = crud.get_apartment_by_manager(db, phone_num=phone_num)
	if apartment is None:
		raise HTTPException(status_code=404, detail="user not found")
	if apartment == 0:
		raise HTTPException(status_code=404, detail="phone num does not belong to manager")
	if apartment == 1:
		raise HTTPException(status_code=404, detail="manager has no apartment")
	return apartment


@app.get('/user/apartment/{phone_num}', response_model=schemas.Apartment, )
def get_apartment_by_user(phone_num: int, db: Session = Depends(get_db)):
	apartment = crud.get_apartment_by_user(db, phone_num)
	if apartment is None:
		raise HTTPException(status_code=404, detail="user not found")
	if apartment == 0:
		raise HTTPException(status_code=404, detail="user has no apartment")
	return apartment


@app.get('/apartment/{apartment_id}', response_model=schemas.Apartment)
def get_apartment_by_id(apartment_id: int, db: Session = Depends(get_db)):
	apartment = crud.get_apartment(db, apartment_id)
	if apartment is None:
		raise HTTPException(status_code=404, detail="apartment not found")
	return apartment
