SET search_path TO course_project, practice, lab;

INSERT INTO Positions (position_name, salary) VALUES
('Механик', 40000),
('Диспетчер', 35000);
INSERT INTO Staff (position_id, full_name, passport) VALUES
(1, 'Иванов Иван Иванович', '1111 111111'),
(2, 'Петров Петр Петрович', '2222 222222');
INSERT INTO Drivers (full_name, phone_number, passport) VALUES
('Сидоров Алексей', '+79991234567', '3333 333333'),
('Козлов Андрей', '+79997654321', '4444 444444');
INSERT INTO Cars (plate_number, car_name, color, VIN, status) VALUES
('A123BC777', 'Toyota Camry', 'Черный', 'JT123456789012345', 'готова'),
('B456DE777', 'Hyundai Solaris', 'Белый', 'KM812345678901234', 'в ремонте');
INSERT INTO Clients (full_name, rating, phone, email) VALUES
('Анна Смирнова', 4.7, '+79991112233', 'anna@example.com'),
('Дмитрий Орлов', 4.2, '+79992223344', 'dmitriy@example.com');
INSERT INTO Orders (client_id, starting_address, finish_address, price, status) VALUES
(1, 'ул. Ленина, 10', 'пр. Мира, 25', 350, 'выполнен'),
(2, 'ул. Пушкина, 5', 'ул. Чехова, 18', 420, 'выполнен');
INSERT INTO Assignments (driver_id, assignment_date, revenue) VALUES
(1, CURRENT_DATE, 0),
(2, CURRENT_DATE, 0);
INSERT INTO Orders_Drivers (id, driver_id, car_id, order_price) VALUES
(1, 1, 1, 350),
(2, 2, 2, 420);
INSERT INTO Tech_Inspection (car_id, mechanic_id, work_type, work_cost) VALUES
(1, 1, 'Плановая проверка', 1500),
(2, 1, 'Кузовной ремонт', 5000);
