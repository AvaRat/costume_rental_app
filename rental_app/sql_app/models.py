from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship



from .database import Base



class Location(Base):
    __tablename__ = "locations"

    id = Column("location_id", Integer, primary_key=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)

    manager_id = Column(Integer, ForeignKey("employees.employee_id"), nullable=False)

    manager = relationship("Employee", back_populates="location")


class Employee(Base):
    __tablename__ = "employees"

    id = Column("employee_id", Integer, primary_key=True)
    address = Column(String, nullable=False)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)


    location = relationship("Location", back_populates="manager")

class CostumeItem(Base):
    __tablename__ = "costume_items"

    id = Column("costume_id", Integer, primary_key=True)
    model_id = Column("model_id", Integer, ForeignKey("costume_models.model_id"))
    rental_id = Column("rental_id", Integer, ForeignKey("costume_rentals.rental_id"), nullable=True)

    model = relationship("CostumeModel", back_populates="items")
    rental = relationship("CostumeRental", back_populates="items")

class CostumeModel(Base):
    __tablename__ = "costume_models"

    id = Column("model_id", Integer, primary_key=True)
    name = Column(String, nullable=False)
    size = Column(String, nullable=False)
    type_ = Column("type_name", String, nullable=False)
    collection = Column("collection_name", String, nullable=False)
    price = Column(Float(precision=8), nullable=False)

    items = relationship("CostumeItem", back_populates="model")

class CostumeRental(Base):
    __tablename__ = "costume_rentals"

    id = Column("rental_id", Integer, primary_key=True)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)

    #subscription_id = relationship("subscription_id", back_populates="Subscriptions")
    #reservation_id = relationship("reservations", back_populates="reservation_")

    items = relationship("CostumeItem", back_populates="rental")
    #reservation = relationship("Reservation", back_populates="rental") #TODO

