# MIVACARE HOSPITAL – Advanced Database Portfolio

**Course:** MIT 8103 Advanced Database Systems – First Semester CA, 2026/2027 (MIVA Open University)
**Student:** Alali John Boma (2026AMIT0094)
**Assessment:** Individual Practical Database Portfolio (40 marks)

## Selected case study / organisation
| | |
|---|---|
| **Organisation** | MIVACARE HOSPITAL (simulated general hospital) |
| **Nature of system** | Hospital Management System for outpatient appointments and billing |
| **Users** | Receptionists, doctors, billing officers, hospital administrators |
| **Major data** | Departments, doctors, patients, appointments, billing records (plus patient documents in NoSQL) |
| **Key operations** | Register patient, book appointment, retrieve patient history, record payment, revenue reporting |

The same case study is used in all five portfolio activities.

## Repository structure
```
advanced-database-portfolio/
├── portfolio-1-database-design/        ER diagram, schemas (MySQL/PostgreSQL/SQL Server/SQLite), sample data, notes
├── portfolio-2-query-optimisation/     queries, benchmark script, execution plans, results
├── portfolio-3-transactions-concurrency/  commit/rollback, isolation, locking, deadlock
├── portfolio-4-nosql/                  MongoDB documents, commands, key-value/graph examples
├── portfolio-5-distributed-cloud/      replication, sharding, availability, cloud design
├── docs/                               final documentation and schema summary
├── screenshots/                        evidence screenshots (add yours here)
└── README.md
```

## Portfolio summary
| # | Activity | Where | Status |
|---|---|---|---|
| 1 | Database Design and Modelling | [portfolio-1-database-design](portfolio-1-database-design/) | ER diagram, schema, constraints, normalisation |
| 2 | Query Processing and Optimisation | [portfolio-2-query-optimisation](portfolio-2-query-optimisation/) | 8 queries, execution plans, before/after index timings |
| 3 | Transactions and Concurrency | [portfolio-3-transactions-concurrency](portfolio-3-transactions-concurrency/) | Commit, rollback, savepoint, locking, isolation |
| 4 | NoSQL and Advanced Data Models | [portfolio-4-nosql](portfolio-4-nosql/) | MongoDB document model |
| 5 | Distributed and Cloud Database | [portfolio-5-distributed-cloud](portfolio-5-distributed-cloud/) | Replication, sharding, CAP discussion, cloud design |
| – | Final documentation | [docs/](docs/) | 2–3 page summary and reflection |

## How each activity was tested
- **SQLite scripts** (`schema_sqlite.sql`, `sample_data_sqlite.sql`, all queries, both Python demos) were executed and their outputs are saved in `portfolio-2.../results/` and `portfolio-3.../results/`.
- **MySQL scripts** were written for MySQL 8 but were not executed in this environment.
- **MongoDB, replication and sharding files** are provided as design/setup files; not run, so no screenshots exist for them.

## Evidence images
Real script output is rendered as images in [screenshots/](screenshots/) (schema, query results, execution plans before/after indexing, performance summary, commit/rollback, atomicity, concurrency). They are captioned as **SQLite output**, not MySQL Workbench. Regenerate with `python3 screenshots/render_evidence.py`.

Not included: MongoDB, replication and cloud screenshots (those files were written but not executed). Add your own MySQL Workbench or MongoDB screenshots to `screenshots/` if you have them.

## AI Use Declaration
Microsoft Copilot was used as a guide for structuring queries, schema design and documentation. All outputs were tested and verified manually in MySQL Workbench.
Claude (Anthropic) was used to reorganise the repository, write the benchmark and transaction demo scripts, and draft documentation. Scripts were executed and outputs reviewed; the student is responsible for understanding and verifying all submitted work.
*(Edit this declaration so it reflects exactly what you used and how you checked it.)*

## References
- MySQL 8.0 Reference Manual – InnoDB locking and transaction isolation levels.
- SQLite documentation – EXPLAIN QUERY PLAN.
- MongoDB Manual – schema validation, aggregation, replication and sharding.
