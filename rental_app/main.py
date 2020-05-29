from sqlalchemy.orm import Session

from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

new_model = schemas.CostumeModel(name="Piracki kozak", size="M", price=100, type_="okazyjny", collection="karaiby")



db = SessionLocal()
#print(crud.create_costume_model(db, new_model).json())
print(crud.get_all_models(db)[0].__dict__)

db.close()