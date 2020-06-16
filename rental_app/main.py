from typing import List
from datetime import date, timedelta
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

def check_dates_range(date_from: date, date_to: date):
    if(date_from < date_to):
        return True
    return False

def get_reservation_out(reservation: models.Reservation, db: Session) -> schemas.ReservationOut:
    costumes = crud.get_items_from_reservation(db, reservation.id)
    reservations_prices = [costume.model.price for costume in costumes]
    total_cost = sum(reservations_prices)
    models_quanity =  crud.get_model_quantities_in_reservation(db, reservation)

    print(models_quanity)

    return schemas.ReservationOut(reservation_code=reservation.id, date=reservation.date, pick_up_date=reservation.pick_up_date, \
        return_date=reservation.return_date, pick_up_address=reservation.pick_up_location, \
        costumes=[schemas.CostumeItemOut(quantity=model[1], \
            model=schemas.CostumeModelOut(**model[0].__dict__, model_id=model[0].id)) for model in models_quanity], \
        total_cost=total_cost)


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

@app.post("/test_new_reservation")
def post_test(reservation: schemas.ReservationCreateTest, db:Session = Depends(get_db)):
    return crud.create_reservation_without_checks(db, reservation, username='test')
    
@app.get("/")
def main_page():
    return {"message": "visit /docs for more info"}

@app.get("/welcome")
def welcome_page():
    return {"message": "witaj w wypożyczalni strojów. Zaloguj się aby zmienić rezerwację. Odwiedź /costumes aby zobaczyć dostępne stroje"}

@app.post("/create_user")
def create_user(user: schemas.ClientCreate, db: Session=Depends(get_db)):
    crud.create_client(db, user)
    return {"message": "succesfully created account"}

@app.get("/system_user/all_users", response_model=List[schemas.ClientBase])
def get_all_user_details(db: Session = Depends(get_db), admin: HTTPBasicCredentials = Depends(admin_check)):
    return [schemas.ClientBase(**c.__dict__, nr_reservations= len(crud.get_user_reservations(db,c.id))) for c in crud.get_all_users(db)]

#@app.post("/test_new_reservation")
#def create_test_reservation(reservation: schemas.ReservationCreate, user: models.Client = Depends(get_current_user), db: Session = Depends(get_db)):
#    if not(check_dates_range(reservation.pick_up_date, reservation.return_date)):
#        return {"error": "pick_up date is after return date"}
#    return crud.test_create_reservation(db, reservation, username=user.login)

@app.post("/new_reservation", status_code=status.HTTP_201_CREATED, response_model=schemas.ReservationOut)
def create_reservation(reservation: schemas.ReservationCreate, user: models.Client = Depends(get_current_user), db: Session = Depends(get_db)):
    #return crud.create_reservation(db, reservation, username=user.login)
    try:
        new_reservation = crud.create_reservation(db, reservation, username=user.login)
    except RuntimeError as e:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e),
            )
    return get_reservation_out(new_reservation, db)



@app.post("/modify_reservation", status_code=status.HTTP_200_OK)
def modify_reservation(reservation: schemas.ReservationModify, user:models.Client = Depends(get_current_user), db: Session = Depends(get_db)):
    if not(check_dates_range(reservation.pick_up_date, reservation.return_date)):
        return JSONResponse(content={"error": "pick_up date is after return date"})
    try:
        msg = crud.modify_reservation(db, reservation, user)
    except RuntimeError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e),
            )
    return {"message":msg}

@app.post("/system_user/rent_from_reservation/{reservation_id}/{pick_up_code}")
def rent_from_reservations(reservation_id: int, pick_up_code: int, db: Session = Depends(get_db), \
                            admin_name: HTTPBasicCredentials = Depends(admin_check)):
    return crud.rent_from_reservation(db, reservation_id, pick_up_code)

@app.get("/my_reservations", response_model=List[schemas.ReservationOut])
def get_user_reservations(user: models.Client = Depends(get_current_user), db: Session = Depends(get_db)):
    reservations_db = crud.get_user_reservations(db, user.id)
    models = []
    for res in reservations_db:
        models.append(get_reservation_out(res, db))
    return models

@app.get("/models", response_model=List[schemas.CostumeModelOut])
def get_all_models(db: Session = Depends(get_db)):
    all_models = crud.get_all_models(db)
    return [schemas.CostumeModelOut(**model.__dict__, model_id=model.id) for model in all_models]

@app.get("/available_costumes", response_model=List[schemas.CostumeItemOut])
def get_available_costumes(db: Session= Depends(get_db), date_from: date=date.today(), date_to: date=date.today()+timedelta(days=7), limit: int = 10):
    if not(check_dates_range(date_from, date_to)):
        return JSONResponse(content={"error": "pick_up date is after return date"})
    available_models= crud.get_available_costume_models_with_quantity(db, date_from, date_to, limit)
    #print(costume_items_db)
    return [schemas.CostumeItemOut(model=schemas.CostumeModelOut(**model_info[0].__dict__, model_id=model_info[0].id), quantity=model_info[1]) for model_info in available_models]


@app.get("/system_user/all_costumes", response_model=List[schemas.CostumeItemSystem])
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