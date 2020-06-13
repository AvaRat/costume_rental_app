from typing import List
from datetime import datetime, timedelta
import secrets

from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from .sql_app import crud, models, schemas
from . import create_db
from .sql_app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
security = HTTPBasic()

origins = [
    'https://wypozyczalniastrojowteatrlnych.herokuapp.com',
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
def admin_check(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "admin1")
    correct_password = secrets.compare_digest(credentials.password, "wypozyczalnia")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@app.post("/create_db")
def create_database(admin_name: HTTPBasicCredentials = Depends(admin_check)):
    return create_db.populate_new_db()



def get_current_user(credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)):
    user = crud.get_user_from_username(db, credentials.username)
    if(user == None):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User doesn't exist",
            headers={"WWW-Authenticate": "Basic"},
        )
    correct_password = secrets.compare_digest(credentials.password, user.password)
    if not (correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return user

@app.post("/test_new_resrvation")
def post_test(reservation: schemas.ReservationCreate, db:Session = Depends(get_db)):
    return crud.create_reservation(db, reservation, username='test')
    
@app.get("/")
def main_page():
    return {"message": "visit /docs for more info"}

@app.get("/welcome")
def welcome_page():
    return {"message": "witaj w wypożyczalni strojów. Zaloguj się aby zmienić rezerwację. Odwiedź /costumes aby zobaczyć dostępne stroje"}

@app.post("/new_reservation", status_code=status.HTTP_201_CREATED)
def create_reservation(reservation: schemas.ReservationCreate, user: models.Client = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.create_reservation(db, reservation, username=user.login)

@app.post("/modify_reservation", status_code=status.HTTP_200_OK)
def modify_reservation(reservation: schemas.ReservationModify, user:models.Client = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        crud.modify_reservation(db, reservation, user)
    except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e),
            )
    return True

@app.post("/system_user/rent_from_reservation/{reservation_id}/{pick_up_code}")
def rent_from_reservations(reservation_id: int, pick_up_code: int, db: Session = Depends(get_db), \
                            admin_name: HTTPBasicCredentials = Depends(admin_check)):
    return crud.rent_from_reservation(db, reservation_id, pick_up_code)

@app.get("/my_reservations", response_model=List[schemas.ReservationOut])
def read_user_reservations(user: models.Client = Depends(get_current_user), db: Session = Depends(get_db)):
    reservations_db = crud.get_user_reservations(db, user.id)
    models = []
    for res in reservations_db:
        costumes = crud.get_costume_models_from_reservation(db, res.id)
        reservations_prices = [costume.price for costume in costumes]
        total_cost = sum(reservations_prices)
        models.append(schemas.ReservationOut(date=res.date, pick_up_date=res.pick_up_date, return_date=res.return_date, \
        pick_up_location_id=res.pick_up_location_id, costumes=crud.get_costume_models_from_reservation(db, res.id),\
        total_cost=total_cost))
    return models

@app.get("/models", response_model=List[schemas.CostumeModel])
def read_models(db: Session = Depends(get_db)):
    return crud.get_all_models(db)

@app.get("/available_costumes", response_model=List[schemas.CostumeItem])
def get_available_costumes(db: Session= Depends(get_db), date_from: datetime=datetime.now(), date_to: datetime=datetime.now()+timedelta(days=7), limit: int = 10):
    costume_items_db = crud.get_available_costume_items(db, date_from, date_to, limit)
    print(costume_items_db)
    return costume_items_db


@app.get("/system_user/costumes", response_model=List[schemas.CostumeItem])
def get_all_costumes(skip: int=0, limit: int=10, db: Session = Depends(get_db), admin_name: HTTPBasicCredentials = Depends(admin_check)):
    
    return crud.get_all_costume_items(db, skip=skip, limit=limit)

#
#
#new_model = schemas.CostumeModel(name="Piracki kozak", size="M", price=100, type_="okazyjny", collection="karaiby")
#
#
#
#db = SessionLocal()
##print(crud.create_costume_model(db, new_model).json())
#print(crud.get_all_models(db)[0].__dict__)
#
#db.close()