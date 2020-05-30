from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship



from .database import Base


class Location(Base):
    __tablename__ = "Locations"

    id = Column("location_id", Integer, primary_key=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)

    reservations = relationship("Reservation", back_populates="pick_up_location")
    employees = relationship("Employee", back_populates="location")


class Employee(Base):
    __tablename__ = "Employees"

    id = Column("employee_id", Integer, primary_key=True)
    address = Column(String, nullable=False)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    location_id = Column(Integer, ForeignKey("Locations.location_id"), nullable=False)

    location = relationship("Location", back_populates="employees")

class CostumeItem(Base):
    __tablename__ = "Costume_items"

    id = Column("costume_id", Integer, primary_key=True)
    model_id = Column("model_id", Integer, ForeignKey("Costume_models.model_id"))
    rental_id = Column("rental_id", Integer, ForeignKey("Costume_rentals.rental_id"), nullable=True)
    reservation_id = Column(Integer, ForeignKey("Reservations.reservation_id"), nullable=True)

    model = relationship("CostumeModel", back_populates="items")
    rental = relationship("CostumeRental", back_populates="items")
    reservation = relationship("Reservation", back_populates="costumes")

class CostumeModel(Base):
    __tablename__ = "Costume_models"

    id = Column("model_id", Integer, primary_key=True)
    name = Column(String, nullable=False)
    size = Column(String, nullable=False)
    type_ = Column("type_name", String, nullable=False)
    collection = Column("collection_name", String, nullable=False)
    price = Column(Float(precision=8), nullable=False)

    items = relationship("CostumeItem", back_populates="model")

class CostumeRental(Base):
    __tablename__ = "Costume_rentals"

    id = Column("rental_id", Integer, primary_key=True)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)

    #subscription_id = relationship("subscription_id", back_populates="Subscriptions")
    reservation_id = Column(Integer, ForeignKey("Reservations.reservation_id"), nullable=True)

    items = relationship("CostumeItem", back_populates="rental")
    reservation = relationship("Reservation", back_populates="rental")

class Reservation(Base):
    __tablename__="Reservations"
    id = Column("reservation_id", Integer, primary_key=True)
    date = Column("reservation_date", DateTime, nullable=False)
    pick_up_date = Column(DateTime, nullable=False)
    return_date = Column(DateTime, nullable=False)

    client_id = Column(ForeignKey("Clients.client_id"), nullable=False)
    pick_up_location_id = Column(ForeignKey("Locations.location_id"), nullable=False)


    client = relationship("Client", back_populates="reservations")
    pick_up_location = relationship("Location", back_populates="reservations")
    rental = relationship("CostumeRental", back_populates="reservation")
    costumes = relationship("CostumeItem", back_populates="reservation")

class Client(Base):
    __tablename__="Clients"

    id = Column("client_id", Integer, primary_key=True)
    address = Column(String, nullable=False)
    phone_nr = Column(String, nullable=False)
    email = Column(String, nullable=False)
    login = Column(String, nullable=False)
    password = Column(String, nullable=False) # TODO insecure password storage!!!

    reservations = relationship("Reservation", back_populates="client")


