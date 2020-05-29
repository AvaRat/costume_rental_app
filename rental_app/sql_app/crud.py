from sqlalchemy.orm import Session
import uuid
from . import models, schemas

def create_costume_model(db: Session, model: schemas.CostumeModel):
    db_costume_model = models.CostumeModel(**model.dict(), id=1)
    db.add(db_costume_model)
    db.commit()
    db.refresh(db_costume_model)
    return db_costume_model

def get_all_models(db: Session):
    return db.query(models.CostumeModel).all()

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