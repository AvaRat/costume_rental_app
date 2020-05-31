from sqlalchemy.orm import Session
import uuid
from . import models, schemas
from datetime import datetime

def create_costume_model(db: Session, model: schemas.CostumeModel):
    total_costumes = len(db.query(models.CostumeModel).all())
    db_costume_model = models.CostumeModel(**model.dict(), id=total_costumes+1)
    db.add(db_costume_model)
    db.commit()
    db.refresh(db_costume_model)
    return db_costume_model

def create_reservation(db: Session, reservation: schemas.ReservationCreate, username: str):
    total_res = len(db.query(models.Reservation).all())
    reservation_db_model = schemas.ReservationDb(**reservation.dict(), id=total_res+1, \
        date=datetime.now(), client_id=get_client_id_from_username(db,username))
    db_reservation = models.Reservation(**reservation_db_model.dict())
    selected_costumes = db.query(models.CostumeItem).filter(models.CostumeItem.id.\
        in_(reservation.costumes)).all()
    db.add(db_reservation)

    for costume in selected_costumes:
        costume.reservation = db_reservation
        #costume.location = None
    db.commit()
    return True

def get_user_from_username(db: Session, username: str):
    return db.query(models.Client).filter(models.Client.login == username).first()


def get_client_id_from_username(db: Session, username: str):
    return db.query(models.Client).filter(models.Client.login == username).first().id

def get_all_models(db: Session):
    return db.query(models.CostumeModel).all()

def get_available_costume_items(db: Session):
    return db.query(models.CostumeItem).filter(models.CostumeItem.reservation_id == None).offset(skip).limit(limit).all()


def get_all_costume_items(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.CostumeItem).offset(skip).limit(limit).all()

def get_client(db: Session, email: str):
    return db.query(models.Client).filter(models.Client.email == email).first()

def get_client_reservations(db:Session, user_id: int):
    return db.query(models.Client.reservations).filter(models.Client.client_id == user_id).all()

def create_client(db: Session, client: schemas.ClientCreate):
    total_clients = len(db.query(models.Client).all())
    db_client = models.Client(**client.dict(), id=total_clients+1)
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client
#def get_user(db: Session, user_id: int):
#    return db.query(models.User).filter(models.User.id == user_id).first()
#
#
#def get_user_by_email(db: Session, email: str):
#    return db.query(models.User).filter(models.User.email == email).first()
#
#
#def get_users(db: Session, skip: int = 0, limit: int = 100):
#    return db.query(models.User).offset(skip).limit(limit).all()
#
#def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
#    db_item = models.Item(**item.dict(), owner_id=user_id)
#    db.add(db_item)
#    db.commit()
#    db.refresh(db_item)
#    return db_item