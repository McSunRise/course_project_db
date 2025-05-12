SET search_path TO course_project, practice, lab;
CREATE TABLE Drivers(
	id serial PRIMARY KEY,
	full_name text,
	phone_number varchar(12) UNIQUE,
	passport text UNIQUE,
	rating float DEFAULT 2.5 CHECK (rating BETWEEN 0 AND 5)
);

CREATE TABLE Cars(
	id serial PRIMARY KEY,
	plate_number varchar(12) UNIQUE,
	car_name text,
	color text,
	VIN text UNIQUE,
	status text
);

CREATE TABLE Clients(
	id serial PRIMARY KEY,
	full_name text,
	rating float,
	phone varchar(12) UNIQUE,
	email text UNIQUE DEFAULT NULL
);

CREATE TABLE Orders(
	id serial PRIMARY KEY,
	client_id serial REFERENCES Clients(id),
	order_datetime timestamp NOT NULL DEFAULT now() CHECK (order_datetime <= now()),
	starting_address text,
	finish_address text,
	price SMALLINT,
	status text
);

CREATE TABLE Assignments(
	id serial PRIMARY KEY,
	driver_id serial REFERENCES Drivers(id),
	assignment_date date NOT NULL,
	revenue integer DEFAULT 0
);

CREATE TABLE Orders_Drivers(
	order_id serial PRIMARY KEY REFERENCES Orders (id),
	driver_id serial REFERENCES Drivers (id),
	car_id serial REFERENCES Cars (id),
	order_price SMALLINT
);

CREATE TABLE Positions(
	id serial PRIMARY KEY,
	position_name text,
	salary integer
);

CREATE TABLE Staff(
	id serial PRIMARY KEY,
	position_id serial REFERENCES Positions (id),
	full_name text,
	passport text UNIQUE
);

CREATE TABLE Tech_Inspection(
	id serial PRIMARY KEY,
	car_id serial REFERENCES Cars (id),
	mechanic_id serial REFERENCES Staff (id),
	inspection_date date DEFAULT now(),
	work_type text,
	work_cost integer
);

CREATE OR REPLACE FUNCTION update_driver_rating()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE Drivers
    SET rating = rating + (5 - rating) * 0.05
    WHERE id = NEW.driver_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_update_driver_rating
AFTER INSERT ON Orders_Drivers
FOR EACH ROW
EXECUTE FUNCTION update_driver_rating();


CREATE OR REPLACE FUNCTION validate_assignment_date()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.assignment_date < CURRENT_DATE THEN
        RAISE EXCEPTION 'Дата назначения не может быть в прошлом';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_validate_assignment_date
BEFORE INSERT ON Assignments
FOR EACH ROW
EXECUTE FUNCTION validate_assignment_date();

CREATE OR REPLACE FUNCTION update_assignment_revenue()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE Assignments
    SET revenue = revenue + NEW.order_price
    WHERE driver_id = NEW.driver_id AND assignment_date = CURRENT_DATE;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_update_assignment_revenue
AFTER INSERT ON Orders_Drivers
FOR EACH ROW
EXECUTE FUNCTION update_assignment_revenue();

