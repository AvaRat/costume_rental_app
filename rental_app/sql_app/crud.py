from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import asc, or_, and_, func, not_
from sqlalchemy.sql import text, subquery
import uuid
from . import models, schemas
from datetime import datetime, timedelta


#get_available = text(""" """)

def create_costume_model(db: Session, model: schemas.CostumeModelBase):
    total_costumes = len(db.query(models.CostumeModel).all())
    db_costume_model = models.CostumeModel(**model.dict(), id=total_costumes+1)
    db.add(db_costume_model)
    db.commit()
    db.refresh(db_costume_model)
    return db_costume_model


def create_reservation_without_checks(db: Session, reservation: schemas.ReservationCreateTest, username: str):
    total_res = len(db.query(models.Reservation).all())
    reservation.pick_up_location_id = 1
    reservation_db_model = schemas.ReservationDb(**reservation.dict(), id=total_res+1, \
        date=datetime.now(), client_id=get_client_id_from_username(db,username))

    #selected_costumes = db.query(models.CostumeItem).with_entities(models.CostumeItem, models.CostumeModel). \
    #                                                                join(models.CostumeModel).filter(models.CostumeModel.id.\
    #                                                                    in_(reservation.costumes)).all()
    selected_costumes = db.query(models.CostumeItem).filter(models.CostumeItem.id.in_(reservation.costume_ids)).all()
    db_reservation = models.Reservation(**reservation_db_model.dict())
    
    #selcted_costume = [item, model]

    db.add(db_reservation)

    for costume in selected_costumes:
        costume.reservation = db_reservation    
    db.commit()
    return db_reservation

def create_reservation(db: Session, reservation: schemas.ReservationCreate, username: str):
    #BUG -> passing multiple model_id of the same value in a list

    total_res = len(db.query(models.Reservation).all())
    date_from = reservation.pick_up_date
    date_to = reservation.return_date

    available_items = get_available_costumes_between_dates(db, reservation.pick_up_date, reservation.return_date)
    #check:
    #   -> if wanted costume_model exist
    #   -> if costume_items quantity is available
    #   -> #TODO show when wanted model will be available

    models_count = available_items.join(models.CostumeModel).with_entities(models.CostumeModel.id, func.count(models.CostumeModel.id)).filter(models.CostumeModel.id.in_(\
        [c.model_id for c in reservation.costumes])).group_by(models.CostumeModel.id).order_by(models.CostumeModel.id.asc())

    if(len(models_count.all()) < len(reservation.costumes)):
        raise RuntimeError('Given model is unavailable at this time')

    wanted_costume_counts = {}  #{model_id: quantity}
    for wanted in models_count.all():
        #print(f'\n\nmodel_id: {wanted[0]}  quantity: {wanted[1]}')
        wanted_costume_counts[wanted[0]] = wanted[1]

    for wanted_costume in reservation.costumes:
        if(wanted_costume_counts[wanted_costume.model_id] < wanted_costume.quantity):
            error_msg = str(f"needed {wanted_costume.quantity} pieces of  model {wanted_costume.model_id} but we got only {wanted_costume_counts[wanted_costume.model_id]} costumes of that model available")
            raise RuntimeError(error_msg)

    # ALL CHECKS DONE
    # WE HAVE ALL NECESSARY STUFF TO CREATE RESERVATIONS
    reservation_db_model = schemas.ReservationDb(**reservation.dict(), id=total_res+1, \
        date=datetime.now(), client_id=get_client_id_from_username(db,username))

    db_reservation = models.Reservation(**reservation_db_model.dict())

    selected_available_costumes = available_items.with_entities(models.CostumeItem).filter(models.CostumeItem.model_id.\
                            in_([c.model_id for c in reservation.costumes])).order_by(models.CostumeItem.model_id.asc(), models.CostumeItem.id.asc())


    #iterate through each model_id to pick exactly the quantity of CostumeItem, that user wants
    for costume_info in reservation.costumes:
        model_id = costume_info.model_id
        quantity = costume_info.quantity
        #print(f'model_id: {model_id}, quantity:{quantity}')
        costumes_with_given_mode_id = selected_available_costumes.filter(models.CostumeItem.model_id==model_id).limit(quantity)
        for costume in costumes_with_given_mode_id:
            #print(f'model: {costume.model_id} item:{costume.id}\n')
            costume.reservation = db_reservation


    #print(f'total wanted models available: {len(selected_available_costumes.all())}')

    db.add(db_reservation)
    db.commit()
    return db_reservation

def modify_reservation(db: Session, reservation_new: schemas.ReservationModify, client: models.Client):
    reservation_old = db.query(models.Reservation).filter(models.Reservation.id == reservation_new.id)
    if not(reservation_old.first().client_id == client.id):
        raise  Exception("This reservation belongs to other user")
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

def get_all_models(db: Session) -> List[models.CostumeModel]:
    return db.query(models.CostumeModel).all()

# (max(models.Reservation.pick_up_date, date_from) < min(models.Reservation.return_date, date_to))

#DateRangesOverlap = max(start1, start2) < min(end1, end2)

def get_available_costumes_between_dates(db: Session, date_from: datetime, date_to: datetime):
    return db.query(models.CostumeItem).join(models.Reservation, isouter=True).join(models.CostumeRental, models.CostumeRental.id==models.CostumeItem.rental_id, isouter=True). \
                filter(or_(or_(or_(date_to < models.Reservation.pick_up_date, date_from > models.Reservation.return_date), models.CostumeItem.reservation_id==None), \
                        date_to < models.CostumeRental.start_date, date_from > models.CostumeRental.end_date))

def get_available_costume_items(db: Session, date_from: datetime, date_to: datetime, limit: int):
    available_ = get_available_costumes_between_dates(db, date_from, date_to)
    print(str(available_))
    return available_.order_by(models.CostumeItem.id.asc()).limit(limit).all() # db.query(costume_items).with_entities(func.count(costume_items.)).group_by(costume_items.column).all()



def get_all_costume_items(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.CostumeItem).order_by(models.CostumeItem.id.asc()).offset(skip).limit(limit).all()

def get_client(db: Session, email: str):
    return db.query(models.Client).filter(models.Client.email == email).first()

def get_user_reservations(db:Session, user_id: int) -> List[models.Reservation]:
    return db.query(models.Reservation).filter(models.Reservation.client_id == user_id).order_by(models.Reservation.date.asc()).all()

def get_costume_models_from_reservation(db: Session, reservation_id: int) -> List[models.CostumeModel]:
    res = db.query(models.Reservation).get(reservation_id)
    return [costume.model for costume in res.costumes]

def get_items_from_reservation(db: Session, reservation_id: int) -> List[models.CostumeItem]:
    res = db.query(models.Reservation).get(reservation_id)
    return res.costumes

def get_model_quantities_in_reservation(db: Session, reservation: models.Reservation):
    quantities_query = db.query(models.CostumeItem.model_id.label('model_id'), func.count(models.CostumeItem.model_id).label('quantity')). \
                            filter(models.CostumeItem.reservation_id==reservation.id).group_by(models.CostumeItem.model_id).subquery()
    r = db.query(models.CostumeModel).with_entities(models.CostumeModel, quantities_query.c.quantity).join(quantities_query, quantities_query.c.model_id==models.CostumeModel.id).all()
    return r

def get_models_from_reservation(db:Session, reservation: models.Reservation) -> List[models.CostumeModel]:
    return db.query(models.CostumeItem).filter_by(reservation_id=reservation.id).all()

def get_all_users(db):
    return db.query(models.Client).all()

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