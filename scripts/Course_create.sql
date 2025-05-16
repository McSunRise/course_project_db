SET search_path TO course_project, practice, lab;

CREATE TYPE car_status AS ENUM ('готова', 'в ремонте', 'списана');
CREATE TYPE order_status AS ENUM ('выполнен', 'принят', 'отменён');
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
	status car_status
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
	status order_status
);

CREATE TABLE Assignments(
	id serial PRIMARY KEY,
	driver_id serial REFERENCES Drivers(id),
	assignment_date date NOT NULL DEFAULT current_date CHECK (assignment_date <= current_date),
	revenue integer DEFAULT 0
);

CREATE TABLE Orders_Drivers(
	id serial PRIMARY KEY REFERENCES Orders (id),
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

CREATE OR REPLACE FUNCTION set_order_price()
RETURNS TRIGGER AS $$
BEGIN
	UPDATE Orders_Drivers
	SET order_price = (SELECT price FROM orders WHERE orders.id = orders_drivers.id)
	WHERE id = NEW.id;
	RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_set_order_price
AFTER INSERT ON Orders_Drivers
FOR EACH ROW
EXECUTE FUNCTION set_order_price();


CREATE OR REPLACE FUNCTION update_driver_rating()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE Drivers
    SET rating = rating + (5 - rating) * 0.05
    WHERE Drivers.id = NEW.driver_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_update_driver_rating
AFTER INSERT OR UPDATE ON Orders_Drivers
FOR EACH ROW
EXECUTE FUNCTION update_driver_rating();

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
AFTER INSERT OR UPDATE ON Orders_Drivers
FOR EACH ROW
EXECUTE FUNCTION update_assignment_revenue();

