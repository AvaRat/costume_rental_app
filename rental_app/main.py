from typing import List

from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException

from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

#app = FastAPI()
#
#def get_db():
#    db = SessionLocal()
#    try:
#        yield db
#    finally:
#        db.close()
#
#@app.get("/models", response_model=List[schemas.CostumeModel])
#def read_models(db: Session = Depends(get_db)):
#    return crud.get_all_models(db)
#
#
#
new_model = schemas.CostumeModel(name="Piracki kozak", size="M", price=100, type_="okazyjny", collection="karaiby")
#
#
#
db = SessionLocal()
#print(crud.create_costume_model(db, new_model).json())
print(crud.get_all_models(db)[0].__dict__)

db.close()