"""
MIVACARE HOSPITAL - Portfolio 3 runnable demo (SQLite, standard library only).
Shows: COMMIT, ROLLBACK, atomicity on constraint failure, SAVEPOINT,
and a lost-update race vs. its fix (conditional/optimistic update).
Run: python3 transaction_demo_sqlite.py   (output saved to results/transaction_output.txt)
"""
import sqlite3, pathlib, tempfile, os
ROOT = pathlib.Path(__file__).resolve().parent
SQL = ROOT.parent / "portfolio-1-database-design" / "sql"
out = []
def log(s=""): print(s); out.append(s)

path = os.path.join(tempfile.mkdtemp(), "mivacare.db")
def conn():
    c = sqlite3.connect(path, isolation_level=None)  # manual transaction control
    c.execute("PRAGMA foreign_keys=ON"); return c
db = conn()
db.executescript((SQL / "schema_sqlite.sql").read_text() + (SQL / "sample_data_sqlite.sql").read_text())
q = lambda c, s: c.execute(s).fetchall()

log("MIVACARE HOSPITAL - transaction demo\n")
log("1. COMMIT - pay bill for appointment 2")
db.execute("BEGIN")
db.execute("UPDATE Billing SET PaymentStatus='Paid' WHERE AppointmentID=2")
db.execute("UPDATE Appointments SET Status='Completed' WHERE AppointmentID=2")
db.execute("COMMIT")
log(f"   after COMMIT: {q(db,'SELECT Status FROM Appointments WHERE AppointmentID=2')} {q(db,'SELECT PaymentStatus FROM Billing WHERE AppointmentID=2')}")

log("\n2. ROLLBACK - doubled amount is undone")
db.execute("BEGIN"); db.execute("UPDATE Billing SET Amount=Amount*2 WHERE AppointmentID=1")
log(f"   inside txn : {q(db,'SELECT Amount FROM Billing WHERE AppointmentID=1')}")
db.execute("ROLLBACK")
log(f"   after ROLLBACK: {q(db,'SELECT Amount FROM Billing WHERE AppointmentID=1')}")

log("\n3. Atomicity - constraint failure rolls back the whole unit of work")
db.execute("BEGIN")
db.execute("UPDATE Appointments SET Status='Cancelled' WHERE AppointmentID=3")
try:
    db.execute("UPDATE Billing SET Amount=-500 WHERE AppointmentID=3")
except sqlite3.IntegrityError as e:
    log(f"   error: {e}"); db.execute("ROLLBACK")
log(f"   appointment 3 status after rollback: {q(db,'SELECT Status FROM Appointments WHERE AppointmentID=3')}")

log("\n4. SAVEPOINT - partial rollback")
db.execute("BEGIN"); db.execute("UPDATE Billing SET PaymentStatus='Paid' WHERE AppointmentID=4")
db.execute("SAVEPOINT s1"); db.execute("UPDATE Billing SET PaymentStatus='Failed' WHERE AppointmentID=4")
db.execute("ROLLBACK TO s1"); db.execute("COMMIT")
log(f"   bill 4 status: {q(db,'SELECT PaymentStatus FROM Billing WHERE AppointmentID=4')}")

log("\n5. Concurrency - two sessions pay the same pending bill")
db.execute("UPDATE Billing SET PaymentStatus='Pending' WHERE AppointmentID=2")
a, b = conn(), conn()
a.execute("BEGIN IMMEDIATE")                    # session A takes the write lock
try:
    b.execute("BEGIN IMMEDIATE")
except sqlite3.OperationalError as e:
    log(f"   session B blocked while A holds the write lock: '{e}'")
a.execute("UPDATE Billing SET PaymentStatus='Paid' WHERE AppointmentID=2 AND PaymentStatus='Pending'"); a.execute("COMMIT")
b.execute("BEGIN IMMEDIATE")
cur = b.execute("UPDATE Billing SET PaymentStatus='Paid' WHERE AppointmentID=2 AND PaymentStatus='Pending'")
log(f"   session B conditional update affected {cur.rowcount} row(s) -> duplicate payment prevented")
b.execute("COMMIT")
log("\nAll demos completed.")

(ROOT / "results").mkdir(exist_ok=True)
(ROOT / "results" / "transaction_output.txt").write_text("\n".join(out) + "\n")
