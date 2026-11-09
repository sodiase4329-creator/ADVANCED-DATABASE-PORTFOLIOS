-- MIVACARE HOSPITAL Management System - Portfolio 3: Concurrency and isolation (MySQL / InnoDB)
-- Open TWO sessions (two MySQL Workbench query tabs or two terminals). Run the steps in the order shown.

-- ===== A. Non-repeatable read under READ COMMITTED =====
-- Session 1:  SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;
-- Session 1:  START TRANSACTION;
-- Session 1:  SELECT PaymentStatus FROM Billing WHERE AppointmentID = 2;   -- 'Pending'
-- Session 2:  UPDATE Billing SET PaymentStatus = 'Paid' WHERE AppointmentID = 2;  (autocommit on)
-- Session 1:  SELECT PaymentStatus FROM Billing WHERE AppointmentID = 2;   -- 'Paid'  <-- value changed inside one transaction
-- Session 1:  COMMIT;

-- ===== B. Same steps under REPEATABLE READ (MySQL default) =====
-- Session 1:  SET SESSION TRANSACTION ISOLATION LEVEL REPEATABLE READ;
-- Session 1:  START TRANSACTION;  SELECT PaymentStatus FROM Billing WHERE AppointmentID = 2;
-- Session 2:  UPDATE Billing SET PaymentStatus = 'Pending' WHERE AppointmentID = 2;
-- Session 1:  SELECT PaymentStatus FROM Billing WHERE AppointmentID = 2;   -- unchanged: consistent snapshot
-- Session 1:  COMMIT;

-- ===== C. Lost update PREVENTED with row locking (SELECT ... FOR UPDATE) =====
-- Two receptionists both try to take the last slot / update the same bill.
-- Session 1:  START TRANSACTION;
-- Session 1:  SELECT Amount FROM Billing WHERE AppointmentID = 2 FOR UPDATE;      -- row locked
-- Session 2:  START TRANSACTION;
-- Session 2:  SELECT Amount FROM Billing WHERE AppointmentID = 2 FOR UPDATE;      -- BLOCKS, waiting
-- Session 1:  UPDATE Billing SET Amount = Amount + 200 WHERE AppointmentID = 2;  COMMIT;   -- Session 2 now proceeds
-- Session 2:  UPDATE Billing SET Amount = Amount + 300 WHERE AppointmentID = 2;  COMMIT;   -- both changes kept

-- ===== D. Deadlock (InnoDB detects it and rolls one session back) =====
-- Session 1:  START TRANSACTION;  UPDATE Billing SET Amount = Amount WHERE AppointmentID = 1;
-- Session 2:  START TRANSACTION;  UPDATE Billing SET Amount = Amount WHERE AppointmentID = 2;
-- Session 1:  UPDATE Billing SET Amount = Amount WHERE AppointmentID = 2;   -- waits
-- Session 2:  UPDATE Billing SET Amount = Amount WHERE AppointmentID = 1;   -- ERROR 1213 Deadlock found; this session is rolled back
-- Session 1:  COMMIT;
-- Check details with:  SHOW ENGINE INNODB STATUS;
