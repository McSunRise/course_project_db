SET search_path TO course_project, practice, lab;
CREATE TABLE Drivers(
	id serial PRIMARY KEY,
	full_name text,
	phone_number varchar(12) UNIQUE,
	passport text UNIQUE,
	rating float
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
	order_datetime timestamp NOT NULL DEFAULT now(),
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
