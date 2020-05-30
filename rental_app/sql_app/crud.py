from sqlalchemy.orm import Session
import uuid
from . import models, schemas

def create_costume_model(db: Session, model: schemas.CostumeModel):
    total_costumes = len(db.query(models.CostumeModel).all())
    db_costume_model = models.CostumeModel(**model.dict(), id=total_costumes+1)
    db.add(db_costume_model)
    db.commit()
    db.refresh(db_costume_model)
    return db_costume_model

def get_all_models(db: Session):
    return db.query(models.CostumeModel).all()

def get_available_costume_items(db: Session):
    return db.query(models.CostumeItem).filter(models.CostumeItem.reservation_id == None).first()

def get_client(db: Session, email: str):
    return db.query(models.Client).filter(models.Client.email == email).first()

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