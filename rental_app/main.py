from typing import List
import secrets

from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from .sql_app import crud, models, schemas
from .sql_app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
security = HTTPBasic()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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

@app.get("/welcome")
def welcome_page():
    return {"message": "witaj w wypożyczalni strojów. Zaloguj się aby zmienić rezerwację. Odwiedź /costumes aby zobaczyć dostępne stroje"}

@app.post("/user/new_reservation", response_model=bool)
def create_reservation(reservation: schemas.ReservationCreate, user: models.Client = Depends(get_current_user), db: Session = Depends(get_db)):
    
    return crud.create_reservation(db, reservation, username=user.login)

@app.get("/user/my_reservations")
def view_reservations(user: models.Client = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.get_user_reservations(db, user_id)

@app.get("/models", response_model=List[schemas.CostumeModel])
def read_models(db: Session = Depends(get_db)):
    return crud.get_all_models(db)

@app.get("/costumes", response_model=List[schemas.CostumeItem])
def get_costumes(available_only: bool=False, skip: int=0, limit: int=10, db: Session = Depends(get_db)):
    if(only_available):
        return crud.get_available_costume_items(db, skip=skip, limit=limit)
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