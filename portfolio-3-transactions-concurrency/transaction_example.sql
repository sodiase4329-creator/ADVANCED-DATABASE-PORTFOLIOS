-- MIVACARE HOSPITAL Management System - Portfolio 3: Transactions (MySQL 8.0.16+ / InnoDB)
-- Run schema_mysql.sql and sample_data_mysql.sql first.

-- ===== 1. COMMIT: patient pays the bill for appointment 2 =====
START TRANSACTION;
SELECT BillID, Amount, PaymentStatus FROM Billing WHERE AppointmentID = 2 FOR UPDATE;  -- lock the row
UPDATE Billing SET PaymentStatus = 'Paid' WHERE AppointmentID = 2 AND PaymentStatus = 'Pending';
UPDATE Appointments SET Status = 'Completed' WHERE AppointmentID = 2;
COMMIT;
SELECT AppointmentID, Status FROM Appointments WHERE AppointmentID = 2;   -- Completed
SELECT AppointmentID, PaymentStatus FROM Billing WHERE AppointmentID = 2; -- Paid

-- ===== 2. ROLLBACK: a bad update is undone =====
START TRANSACTION;
UPDATE Billing SET Amount = Amount * 2 WHERE AppointmentID = 1;
SELECT AppointmentID, Amount FROM Billing WHERE AppointmentID = 1;        -- 5000.00 (uncommitted)
ROLLBACK;
SELECT AppointmentID, Amount FROM Billing WHERE AppointmentID = 1;        -- back to 2500.00

-- ===== 3. Constraint failure -> ROLLBACK (CHECK Amount >= 0) =====
START TRANSACTION;
UPDATE Appointments SET Status = 'Cancelled' WHERE AppointmentID = 3;     -- succeeds
UPDATE Billing SET Amount = -500.00 WHERE AppointmentID = 3;              -- ERROR 3819: check constraint violated
ROLLBACK;                                                                  -- the Cancelled change is undone too (atomicity)
SELECT Status FROM Appointments WHERE AppointmentID = 3;                  -- still Completed

-- ===== 4. SAVEPOINT: partial rollback =====
START TRANSACTION;
UPDATE Billing SET PaymentStatus = 'Paid' WHERE AppointmentID = 2;
SAVEPOINT after_payment;
UPDATE Billing SET PaymentStatus = 'Refunded' WHERE AppointmentID = 2;
ROLLBACK TO SAVEPOINT after_payment;                                       -- keeps 'Paid'
COMMIT;
