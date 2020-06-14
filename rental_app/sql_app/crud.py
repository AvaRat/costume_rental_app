from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import asc, or_, and_, func, not_
from sqlalchemy.sql import text
import uuid
from . import models, schemas
from datetime import datetime, timedelta


#get_available = text(""" """)

def create_costume_model(db: Session, model: schemas.CostumeModel):
    total_costumes = len(db.query(models.CostumeModel).all())
    db_costume_model = models.CostumeModel(**model.dict(), id=total_costumes+1)
    db.add(db_costume_model)
    db.commit()
    db.refresh(db_costume_model)
    return db_costume_model

def test_create_reservation(db: Session, reservation: schemas.ReservationCreate, username: str):
    available_costume_items = db.query(models.CostumeItem).join(models.Reservation).filter(or_(and_(reservation.pick_up_date < reservation.return_date,\
                                                                                            reservation.return_date<models.Reservation.pick_up_date), \
                                                                                            and_(reservation.pick_up_date>models.Reservation.return_date, \
                                                                                            reservation.return_date>reservation.return_date))) \
                                                                                        .order_by(models.CostumeItem.id.asc())

    return available_costume_items.all()

def create_reservation(db: Session, reservation: schemas.ReservationCreate, username: str):

    total_res = len(db.query(models.Reservation).all())

    #check:
    #   -> if wanted costume_model exist
    #   -> if costume_items quantity is available
    #   -> 

    # get list of all wanted models
    wanted_models = db.query(models.CostumeModel).filter(models.CostumeModel.id.in_([c.model_id for c in reservation.costumes])).all()
    if(len(wanted_models) != len(reservation.costumes)):
        raise Exception("Given model_id doesn't exist")


    # len(models)==len(costumes) -> robimy joina
    selected_costumes = db.query(models.CostumeItem).with_entities(models.CostumeItem, models.CostumeModel). \
                                                                    join(models.CostumeModel).filter(models.CostumeModel.id.\
                                                                        in_([c.model_id for c in reservation.costumes])).all()
    #check if we habe enough items on magazine
    if(len(selected_costumes) < len(wanted_models)):
        #we don't have enough items, and we have o order them for give reservation
        #TODO
        raise Exception("We don't have enough CostumeItems")


    reservation_db_model = schemas.ReservationDb(**reservation.dict(), id=total_res+1, \
        date=datetime.now(), client_id=get_client_id_from_username(db,username))

    db_reservation = models.Reservation(**reservation_db_model.dict())
    #selcted_costume = [item, model]
    #for costume_info in selected_costumes:
        
    #db.add(db_reservation)
    #
    #for costume in selected_costumes:
    #    costume.reservation = db_reservation
    #    #costume.location = None
    #db.commit()
    return selected_costumes

def modify_reservation(db: Session, reservation_new: schemas.ReservationModify, client: models.Client):
    reservation_old = db.query(models.Reservation).filter(models.Reservation.id == reservation_new.id)
    if not(reservation_old.first().client_id == client.id):
        raise Exception("This reservation belongs to other user")
    if(reservation_old.first().pick_up_date < datetime.now() or reservation_old.return_date < datetime.now()):
        raise Exception("Chosen date is in the past")


    if(reservation_new.cancel):
            db.query(models.Reservation).filter_by(id=reservation_new.id).delete()
            for costume in db.query(models.CostumeItem).filter_by(reservation_id=reservation_new.id).all():
                costume.reservation_id = None
            msg_info = "reservation_cancelled"
    else:
        reservation_old.pick_up_date = reservation_new.pick_up_date
        reservation_old.return_date = reservation_new.return_date
        msg_info = "succesfully modified reservation"
    db.commit()
    return {"message": msg_info}


def rent_from_reservation(db: Session, reservation_id: int, pick_up_code: int):
    total_rentals = len(db.query(models.CostumeRental).all())
    reservation = db.query(models.Reservation).filter(models.Reservation.id == reservation_id).first()
    if(reservation==None):
        raise Exception("given reservation doesn't exist")
    new_rental = models.CostumeRental(id=total_rentals+1, start_date=datetime.now(), end_date=reservation.return_date, \
                                    reservation_id=reservation_id)
    db.add(new_rental)
    for costume in reservation.costumes:
        costume.reservation = None
        costume.rental = new_rental

    db.commit()
    return True

def get_user_from_username(db: Session, username: str):
    return db.query(models.Client).filter(models.Client.login == username).first()


def get_client_id_from_username(db: Session, username: str):
    return db.query(models.Client).filter(models.Client.login == username).first().id

def get_all_models(db: Session):
    return db.query(models.CostumeModel).all()

# (max(models.Reservation.pick_up_date, date_from) < min(models.Reservation.return_date, date_to))

#DateRangesOverlap = max(start1, start2) < min(end1, end2)

def get_available_costume_items(db: Session, date_from: datetime, date_to: datetime, limit: int):
    available_costumes = db.query(models.CostumeItem).join(models.Reservation).filter(or_(date_to < models.Reservation.pick_up_date, date_from > models.Reservation.return_date))

    #costume_items = db.query(models.CostumeItem).join(models.Reservation).filter(or_(and_(date_from < date_to, date_to<models.Reservation.pick_up_date), \
    #                                                                                and_(date_from>models.Reservation.return_date, date_from < date_to))) \
    #                                                                                .order_by(models.CostumeItem.id.asc()).limit(limit)
    
    return available_costumes.order_by(models.CostumeItem.id.asc()).limit(limit).all() # db.query(costume_items).with_entities(func.count(costume_items.)).group_by(costume_items.column).all()



def get_all_costume_items(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.CostumeItem).order_by(models.CostumeItem.id.asc()).offset(skip).limit(limit).all()

def get_client(db: Session, email: str):
    return db.query(models.Client).filter(models.Client.email == email).first()

def get_user_reservations(db:Session, user_id: int) -> List[models.Reservation]:
    return db.query(models.Reservation).filter(models.Reservation.client_id == user_id).order_by(models.Reservation.date.asc()).all()

def get_costume_models_from_reservation(db: Session, reservation_id: int) -> List[models.CostumeModel]:
    res = db.query(models.Reservation).get(reservation_id)
    return [costume.model for costume in res.costumes]


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