-- Add profile columns to doctors table
ALTER TABLE doctors
ADD COLUMN fullname VARCHAR(255),
ADD COLUMN phone VARCHAR(20),
ADD COLUMN specialization VARCHAR(255),
ADD COLUMN clinic_name VARCHAR(255);
