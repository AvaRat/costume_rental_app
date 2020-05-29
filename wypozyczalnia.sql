-- Generated by Oracle SQL Developer Data Modeler 19.1.0.081.0911
--   at:        2020-05-26 15:23:52 CEST
--   site:      Oracle Database 11g
--   type:      Oracle Database 11g



CREATE TABLE business (
    client_id   INTEGER NOT NULL,
    nip         VARCHAR2(10 CHAR) NOT NULL
);

ALTER TABLE business ADD CONSTRAINT business_clients_pk PRIMARY KEY ( client_id );

ALTER TABLE business ADD CONSTRAINT business__un UNIQUE ( client_id );

CREATE TABLE client (
    client_id   INTEGER NOT NULL,
    address     VARCHAR2(20 CHAR) NOT NULL,
    phone_nr    VARCHAR2(9 CHAR) NOT NULL,
    email       VARCHAR2(20 CHAR)
);

ALTER TABLE client ADD CONSTRAINT client_pk PRIMARY KEY ( client_id );

CREATE TABLE collection (
    name VARCHAR2(20 CHAR) NOT NULL
);

ALTER TABLE collection ADD CONSTRAINT collection_pk PRIMARY KEY ( name );

CREATE TABLE employee (
    emp_id                 INTEGER NOT NULL,
    address                VARCHAR2(20 CHAR) NOT NULL,
    name                   VARCHAR2(20 CHAR) NOT NULL,
    surname                VARCHAR2(20 CHAR) NOT NULL,
    manager_id             INTEGER NOT NULL,
    location_location_id   INTEGER NOT NULL,
    employee_emp_id        INTEGER
);

ALTER TABLE employee ADD CONSTRAINT employee_pk PRIMARY KEY ( emp_id );

CREATE TABLE individual (
    client_id   INTEGER NOT NULL,
    pesel       VARCHAR2(13 CHAR) NOT NULL
);

ALTER TABLE individual ADD CONSTRAINT individual_clients_pk PRIMARY KEY ( client_id );

ALTER TABLE individual ADD CONSTRAINT individual_clients_pkv1 UNIQUE ( client_id );

CREATE TABLE inventory (
    costume_id                 INTEGER NOT NULL,
    reservation_reserv_id      INTEGER NOT NULL,
    costume_model_model_id     INTEGER NOT NULL,
    location_location_id       INTEGER NOT NULL,
    costume_rental_rental_id   INTEGER NOT NULL,
    model_id                   INTEGER NOT NULL,
    rental_id                  INTEGER NOT NULL
);

ALTER TABLE inventory ADD CONSTRAINT inventory_pk PRIMARY KEY ( costume_id );

ALTER TABLE inventory ADD CONSTRAINT costumes_inventory_pk UNIQUE ( costume_id );

CREATE TABLE location (
    location_id   INTEGER NOT NULL,
    name          VARCHAR2(20 CHAR) NOT NULL,
    address       VARCHAR2(20 CHAR) NOT NULL,
    manager_id    INTEGER NOT NULL
);

ALTER TABLE location ADD CONSTRAINT location_pk PRIMARY KEY ( location_id );

CREATE TABLE model (
    model_id                    INTEGER NOT NULL,
    name                        VARCHAR2(30 CHAR) NOT NULL,
    "size"                      VARCHAR2(2 CHAR) NOT NULL,
    price                       REAL NOT NULL,
    collection_collecion_name   VARCHAR2(20 CHAR) NOT NULL,
    type_type                   VARCHAR2(20 CHAR) NOT NULL,
    name1                       VARCHAR2(20 CHAR) NOT NULL
);

ALTER TABLE model ADD CONSTRAINT model_pk PRIMARY KEY ( model_id );

CREATE TABLE rental (
    rental_id                      INTEGER NOT NULL,
    start_date                     DATE NOT NULL,
    end_date                       DATE NOT NULL,
    subscription_subscription_id   INTEGER NOT NULL,
    reservation_reserv_id          INTEGER NOT NULL,
    subs_id                        INTEGER NOT NULL
);

ALTER TABLE rental ADD CONSTRAINT rental_pk PRIMARY KEY ( rental_id );

ALTER TABLE rental ADD CONSTRAINT costume_rental_pk UNIQUE ( rental_id );

CREATE TABLE reservation (
    reserv_id          INTEGER NOT NULL,
    reservation_date   DATE NOT NULL,
    pick_up_date       DATE NOT NULL,
    employee_emp_id    INTEGER NOT NULL,
    client_client_id   INTEGER NOT NULL
);

ALTER TABLE reservation ADD CONSTRAINT reservation_pk PRIMARY KEY ( reserv_id );

CREATE TABLE subs (
    subs_id              INTEGER NOT NULL,
    start_date           DATE NOT NULL,
    end_date             DATE NOT NULL,
    nr_of_costumes       INTEGER NOT NULL,
    business_client_id   INTEGER NOT NULL
);

ALTER TABLE subs ADD CONSTRAINT subs_pk PRIMARY KEY ( subs_id );

ALTER TABLE subs ADD CONSTRAINT subscription_pk UNIQUE ( subs_id );

CREATE TABLE type (
    type VARCHAR2(20 CHAR) NOT NULL
);

ALTER TABLE type ADD CONSTRAINT type_pk PRIMARY KEY ( type );

ALTER TABLE business
    ADD CONSTRAINT business_clients_client_fk FOREIGN KEY ( client_id )
        REFERENCES client ( client_id );

ALTER TABLE employee
    ADD CONSTRAINT employee_employee_fk FOREIGN KEY ( employee_emp_id )
        REFERENCES employee ( emp_id );

ALTER TABLE employee
    ADD CONSTRAINT employee_location_fk FOREIGN KEY ( location_location_id )
        REFERENCES location ( location_id );

ALTER TABLE individual
    ADD CONSTRAINT individual_clients_client_fk FOREIGN KEY ( client_id )
        REFERENCES client ( client_id );

ALTER TABLE inventory
    ADD CONSTRAINT inventory_location_fk FOREIGN KEY ( location_location_id )
        REFERENCES location ( location_id );

ALTER TABLE inventory
    ADD CONSTRAINT inventory_model_fk FOREIGN KEY ( costume_model_model_id )
        REFERENCES model ( model_id );

ALTER TABLE inventory
    ADD CONSTRAINT inventory_rental_fk FOREIGN KEY ( costume_rental_rental_id )
        REFERENCES rental ( rental_id );

ALTER TABLE inventory
    ADD CONSTRAINT inventory_reservation_fk FOREIGN KEY ( reservation_reserv_id )
        REFERENCES reservation ( reserv_id );

ALTER TABLE model
    ADD CONSTRAINT model_collection_fk FOREIGN KEY ( collection_collecion_name )
        REFERENCES collection ( name );

ALTER TABLE model
    ADD CONSTRAINT model_type_fk FOREIGN KEY ( type_type )
        REFERENCES type ( type );

ALTER TABLE rental
    ADD CONSTRAINT rental_reservation_fk FOREIGN KEY ( reservation_reserv_id )
        REFERENCES reservation ( reserv_id );

ALTER TABLE rental
    ADD CONSTRAINT rental_subs_fk FOREIGN KEY ( subscription_subscription_id )
        REFERENCES subs ( subs_id );

ALTER TABLE reservation
    ADD CONSTRAINT reservation_client_fk FOREIGN KEY ( client_client_id )
        REFERENCES client ( client_id );

ALTER TABLE reservation
    ADD CONSTRAINT reservation_employee_fk FOREIGN KEY ( employee_emp_id )
        REFERENCES employee ( emp_id );

ALTER TABLE subs
    ADD CONSTRAINT subs_business_fk FOREIGN KEY ( business_client_id )
        REFERENCES business ( client_id );

CREATE OR REPLACE TRIGGER arc_fkarc_1_individual BEFORE
    INSERT OR UPDATE OF client_id ON individual
    FOR EACH ROW
DECLARE
    d INTEGER;
BEGIN
    SELECT
        a.client_id
    INTO d
    FROM
        client a
    WHERE
        a.client_id = :new.client_id;

    IF ( d IS NULL OR d <> client_id ) THEN
        raise_application_error(-20223, 'FK Individual_clients_Client_FK in Table Individual violates Arc constraint on Table Client - discriminator column client_ID doesn''t have value client_ID'
        );
    END IF;

EXCEPTION
    WHEN no_data_found THEN
        NULL;
    WHEN OTHERS THEN
        RAISE;
END;
/

CREATE OR REPLACE TRIGGER arc_fkarc_1_business BEFORE
    INSERT OR UPDATE OF client_id ON business
    FOR EACH ROW
DECLARE
    d INTEGER;
BEGIN
    SELECT
        a.client_id
    INTO d
    FROM
        client a
    WHERE
        a.client_id = :new.client_id;

    IF ( d IS NULL OR d <> client_id ) THEN
        raise_application_error(-20223, 'FK Business_clients_Client_FK in Table Business violates Arc constraint on Table Client - discriminator column client_ID doesn''t have value client_ID'
        );
    END IF;

EXCEPTION
    WHEN no_data_found THEN
        NULL;
    WHEN OTHERS THEN
        RAISE;
END;
/



-- Oracle SQL Developer Data Modeler Summary Report: 
-- 
-- CREATE TABLE                            12
-- CREATE INDEX                             0
-- ALTER TABLE                             32
-- CREATE VIEW                              0
-- ALTER VIEW                               0
-- CREATE PACKAGE                           0
-- CREATE PACKAGE BODY                      0
-- CREATE PROCEDURE                         0
-- CREATE FUNCTION                          0
-- CREATE TRIGGER                           2
-- ALTER TRIGGER                            0
-- CREATE COLLECTION TYPE                   0
-- CREATE STRUCTURED TYPE                   0
-- CREATE STRUCTURED TYPE BODY              0
-- CREATE CLUSTER                           0
-- CREATE CONTEXT                           0
-- CREATE DATABASE                          0
-- CREATE DIMENSION                         0
-- CREATE DIRECTORY                         0
-- CREATE DISK GROUP                        0
-- CREATE ROLE                              0
-- CREATE ROLLBACK SEGMENT                  0
-- CREATE SEQUENCE                          0
-- CREATE MATERIALIZED VIEW                 0
-- CREATE MATERIALIZED VIEW LOG             0
-- CREATE SYNONYM                           0
-- CREATE TABLESPACE                        0
-- CREATE USER                              0
-- 
-- DROP TABLESPACE                          0
-- DROP DATABASE                            0
-- 
-- REDACTION POLICY                         0
-- 
-- ORDS DROP SCHEMA                         0
-- ORDS ENABLE SCHEMA                       0
-- ORDS ENABLE OBJECT                       0
-- 
-- ERRORS                                   0
-- WARNINGS                                 0