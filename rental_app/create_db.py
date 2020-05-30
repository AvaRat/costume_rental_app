import json

from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine

from fastapi.encoders import jsonable_encoder

models.Base.metadata.create_all(bind=engine)


#    db_costume_model = models.CostumeModel(**model.dict(), id=total_costumes+1)
#    db.add(db_costume_model)
#    db.commit()
#    db.refresh(db_costume_model)

with open("rental_app/initial_data.json", 'r') as f:
    data = json.load(f)
    db = SessionLocal()
    try:
        for client in data["Clients"]:
            models.Client(**client)
            db_client = models.Client(**client)
            db.add(db_client)
        for location in data["Locations"]:
            db_loc = models.Location(**location)
            db.add(db_loc)
        for employee in data["Employees"]:
            db_empl = models.Employee(**employee)
            db.add(db_empl)
        for model in data["Models"]:
            db_model = models.CostumeModel(**model)
            db.add(db_model)
        db.commit()
    finally:
        db.close()