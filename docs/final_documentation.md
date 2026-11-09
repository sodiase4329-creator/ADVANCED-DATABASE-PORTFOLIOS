# MIT 8103 Advanced Database Systems – Portfolio Documentation

**Student:** Alali John Boma (2026AMIT0094)  **Case study:** MIVACARE HOSPITAL
**GitHub repository:** https://github.com/johnalali123-cmyk/Alali_John_Boma_2026AMIT0094_AdvancedDatabasePortfolio *(private – make sure the assessor has access)*

## 1. Selected organisation
MIVACARE HOSPITAL is a simulated general hospital. The database supports outpatient operations: receptionists register patients and book appointments, doctors review patient history, billing officers record payments, and administrators report revenue. Major data: departments, doctors, patients, appointments and billing records. All five portfolios use this case study.

## 2. Portfolio 1 – Database Design and Modelling
The relational model has five tables: Departments, Doctors, Patients, Appointments and Billing. Relationships: Department 1–N Doctors; Patient 1–N Appointments; Doctor 1–N Appointments; Appointment 1–1 Billing (UNIQUE foreign key). Constraints include primary and foreign keys, NOT NULL, UNIQUE department names, CHECK on appointment and payment status, CHECK(Amount ≥ 0) and ON DELETE RESTRICT. The schema is in 3NF: attributes depend only on their table's key, so department names and doctor details are stored once. Scripts exist for MySQL, PostgreSQL, SQL Server and SQLite. *Evidence: ER diagram, `portfolio-1-database-design/`.*

## 3. Portfolio 2 – Query Processing and Optimisation
Eight queries cover joins, aggregation, filtering and reporting. A benchmark on 100,000 appointments and 100,000 bills compared execution plans before and after indexing. Patient-history lookup fell from 2.35 ms (full scan) to under 0.01 ms with an index on `Appointments(PatientID)`, and a composite index on `(AppointmentDate, Status)` cut a date filter from 3.97 ms to 0.04 ms. The two aggregate-heavy queries (unpaid bills, revenue by department) were slightly slower after indexing (37→56 ms and 51→78 ms) because they touch most rows; indexes help selective queries but add write and storage cost. *Evidence: `benchmark_output.txt`, EXPLAIN screenshots.*

## 4. Portfolio 3 – Transactions and Concurrency
Transactions demonstrate COMMIT (pay a bill and complete the appointment together), ROLLBACK, atomicity (a CHECK violation undoes an earlier update in the same transaction) and SAVEPOINT. For concurrency, two sessions trying to pay the same bill are controlled with row locks (`SELECT … FOR UPDATE`) and a conditional update (`WHERE PaymentStatus='Pending'`), which prevented a duplicate payment. A two-session MySQL script also covers READ COMMITTED vs REPEATABLE READ and an InnoDB deadlock. *Evidence: `transaction_output.txt`, two-session screenshots.*

## 5. Portfolio 4 – NoSQL and Advanced Data Models
A MongoDB document model stores each patient with embedded appointments, doctor summary, bill and medical history, using the same four patients as the SQL data. Schema validation, queries, a revenue aggregation pipeline and an index are in `mongodb_commands.js`. The model suits patient-centric reads (full history in one query) and flexible clinical data, but duplicates doctor details and makes cross-patient reporting harder, so the relational database stays the system of record for billing.

## 6. Portfolio 5 – Distributed and Cloud Database Exercise
Design: a MySQL primary handles writes and read replicas serve reports and the patient portal; a three-node MongoDB replica set provides automatic failover; `patients` can be sharded on a hashed `_id` to spread load. Appointments and payments need strong consistency (primary or `w: majority`), while dashboards tolerate replica lag (eventual consistency, CAP trade-off). Managed cloud options (Amazon RDS Multi-AZ, MongoDB Atlas) reduce operational work, with encryption and private networking for sensitive health data. *Evidence: Docker Compose and replication scripts, `SHOW REPLICA STATUS` screenshot.*

## 7. Individual technical reflection
*(Write this in your own words – the assessor will compare it with your commits. Suggested points:)*
- **Design choices:** why billing is a separate table linked 1–1 to appointments; why CHECK constraints and RESTRICT were used.
- **Challenges:** e.g. indexes did not speed up aggregate queries; keeping SQL and NoSQL data consistent; getting multi-session locking to behave as expected.
- **Lessons learned:** read execution plans before adding indexes; transactions group related changes; the right model depends on the access pattern.

## 8. AI Use Declaration
Microsoft Copilot was used as a guide for query structuring, schema design and documentation. Claude (Anthropic) was used to reorganise the repository and draft scripts and documentation. Scripts were executed and outputs reviewed by the student. *(Edit to match exactly what you used and checked.)*

## 9. References
MySQL 8.0 Reference Manual (InnoDB transactions and locking); SQLite documentation (EXPLAIN QUERY PLAN); MongoDB Manual (validation, aggregation, replication, sharding).
