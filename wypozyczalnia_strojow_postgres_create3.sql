CREATE TABLE "Locations" (
	"location_id" int NOT NULL,
	"name" TEXT NOT NULL,
	"address" TEXT NOT NULL,
	CONSTRAINT "Locations_pk" PRIMARY KEY ("location_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Employees" (
	"employee_id" int NOT NULL,
	"address" TEXT NOT NULL,
	"name" TEXT NOT NULL,
	"surname" TEXT NOT NULL,
	"manager_id" int,
	"location_id" int NOT NULL,
	CONSTRAINT "Employees_pk" PRIMARY KEY ("employee_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Reservations" (
	"reservation_id" int NOT NULL,
	"reservation_date" TIMESTAMP NOT NULL,
	"pick_up_date" TIMESTAMP NOT NULL,
	"return_date" TIMESTAMP NOT NULL,
	"client_id" int NOT NULL,
	"pick_up_location_id" int NOT NULL,
	CONSTRAINT "Reservations_pk" PRIMARY KEY ("reservation_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Clients" (
	"client_id" int NOT NULL,
	"address" TEXT NOT NULL,
	"phone_nr" TEXT NOT NULL,
	"email" TEXT NOT NULL,
	"login" TEXT NOT NULL,
	"password" TEXT NOT NULL,
	CONSTRAINT "Clients_pk" PRIMARY KEY ("client_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Business_clients" (
	"NIP" numeric(10) NOT NULL UNIQUE,
	"client_id" int NOT NULL,
	CONSTRAINT "Business_clients_pk" PRIMARY KEY ("client_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Individual_clients" (
	"PESEL" numeric(11) NOT NULL,
	"client_id" int NOT NULL,
	CONSTRAINT "Individual_clients_pk" PRIMARY KEY ("client_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Subsciptions" (
	"subscribtion_id" int NOT NULL,
	"start_date" TIMESTAMP NOT NULL,
	"end_date" TIMESTAMP NOT NULL,
	"nr_of_costumes" int NOT NULL,
	"client_id" int NOT NULL,
	"attendant_id" int NOT NULL,
	CONSTRAINT "Subsciptions_pk" PRIMARY KEY ("subscribtion_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Costume_rentals" (
	"rental_id" int NOT NULL,
	"start_date" TIMESTAMP NOT NULL,
	"end_date" TIMESTAMP NOT NULL,
	"subscription_id" int,
	"reservation_id" int,
	CONSTRAINT "Costume_rentals_pk" PRIMARY KEY ("rental_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Costume_items" (
	"costume_id" int NOT NULL,
	"model_id" int NOT NULL,
	"rental_id" int,
	"reservation_id" int,
	CONSTRAINT "Costume_items_pk" PRIMARY KEY ("costume_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Costume_models" (
	"model_id" int NOT NULL,
	"name" TEXT NOT NULL,
	"size" character NOT NULL,
	"price" real NOT NULL,
	"type_name" TEXT NOT NULL,
	"collection_name" TEXT NOT NULL,
	CONSTRAINT "Costume_models_pk" PRIMARY KEY ("model_id")
) WITH (
  OIDS=FALSE
);




ALTER TABLE "Employees" ADD CONSTRAINT "Employees_fk0" FOREIGN KEY ("manager_id") REFERENCES "Employees"("employee_id");
ALTER TABLE "Employees" ADD CONSTRAINT "Employees_fk1" FOREIGN KEY ("location_id") REFERENCES "Locations"("location_id");

ALTER TABLE "Reservations" ADD CONSTRAINT "Reservations_fk0" FOREIGN KEY ("client_id") REFERENCES "Clients"("client_id");
ALTER TABLE "Reservations" ADD CONSTRAINT "Reservations_fk1" FOREIGN KEY ("pick_up_location_id") REFERENCES "Locations"("location_id");


ALTER TABLE "Business_clients" ADD CONSTRAINT "Business_clients_fk0" FOREIGN KEY ("client_id") REFERENCES "Clients"("client_id");

ALTER TABLE "Individual_clients" ADD CONSTRAINT "Individual_clients_fk0" FOREIGN KEY ("client_id") REFERENCES "Clients"("client_id");

ALTER TABLE "Subsciptions" ADD CONSTRAINT "Subsciptions_fk0" FOREIGN KEY ("client_id") REFERENCES "Business_clients"("client_id");
ALTER TABLE "Subsciptions" ADD CONSTRAINT "Subsciptions_fk1" FOREIGN KEY ("attendant_id") REFERENCES "Employees"("employee_id");

ALTER TABLE "Costume_rentals" ADD CONSTRAINT "Costume_rentals_fk0" FOREIGN KEY ("subscription_id") REFERENCES "Subsciptions"("subscribtion_id");
ALTER TABLE "Costume_rentals" ADD CONSTRAINT "Costume_rentals_fk1" FOREIGN KEY ("reservation_id") REFERENCES "Reservations"("reservation_id");

ALTER TABLE "Costume_items" ADD CONSTRAINT "Costume_items_fk0" FOREIGN KEY ("model_id") REFERENCES "Costume_models"("model_id");
ALTER TABLE "Costume_items" ADD CONSTRAINT "Costume_items_fk1" FOREIGN KEY ("rental_id") REFERENCES "Costume_rentals"("rental_id");
ALTER TABLE "Costume_items" ADD CONSTRAINT "Costume_items_fk2" FOREIGN KEY ("reservation_id") REFERENCES "Reservations"("reservation_id");


