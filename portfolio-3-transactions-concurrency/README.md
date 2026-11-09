# Portfolio 3 – Transactions and Concurrency (MIVACARE HOSPITAL)

| Item | File |
|---|---|
| MySQL transactions (commit, rollback, constraint failure, savepoint) | [transaction_example.sql](transaction_example.sql) |
| Two-session isolation, locking and deadlock scenarios | [concurrency_mysql.sql](concurrency_mysql.sql) |
| Runnable demo (SQLite) | [transaction_demo_sqlite.py](transaction_demo_sqlite.py) |
| Captured output | [results/transaction_output.txt](results/transaction_output.txt) |

## What is demonstrated
1. **Commit** – paying a bill and completing the appointment together.
2. **Rollback** – an uncommitted change disappears.
3. **Atomicity** – a CHECK violation (negative amount) rolls back an earlier successful update in the same transaction.
4. **Savepoint** – partial rollback.
5. **Concurrency control** – row locks (`SELECT … FOR UPDATE`) and a conditional update (`… AND PaymentStatus='Pending'`) stop two users from paying the same bill twice.
6. **Isolation levels** – READ COMMITTED vs REPEATABLE READ, and an InnoDB deadlock (MySQL, two sessions).

The SQLite demo was executed and its output is saved. `concurrency_mysql.sql` is a step-by-step script for two MySQL Workbench tabs; take screenshots of your own runs.
