SET search_path TO course_project, practice, lab;

DROP TABLE IF EXISTS Tech_Inspection, Staff, Positions, Orders_Drivers, Assignments, Orders, Clients, Cars, Drivers;
DROP FUNCTION update_driver_rating(), validate_assignment_date(), update_assignment_revenue() CASCADE;