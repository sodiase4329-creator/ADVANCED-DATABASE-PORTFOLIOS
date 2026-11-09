"""
MIVACARE HOSPITAL - Portfolio 2: Query Processing and Optimisation
Loads the SQLite schema, generates a larger synthetic dataset, then records
EXPLAIN QUERY PLAN output and timings BEFORE and AFTER adding indexes.

Run:  python3 benchmark_sqlite.py        (output is also saved in results/)
"""
import random, sqlite3, time, pathlib, datetime

ROOT = pathlib.Path(__file__).resolve().parent
SQL = ROOT.parent / "portfolio-1-database-design" / "sql"
random.seed(8103)  # reproducible

db = sqlite3.connect(":memory:")
db.executescript((SQL / "schema_sqlite.sql").read_text())
# Remove the starter indexes so we can measure "before" honestly
for ix in ("idx_doctors_deptid", "idx_appointments_patientid",
           "idx_appointments_doctorid", "idx_billing_paymentstatus"):
    db.execute(f"DROP INDEX IF EXISTS {ix}")

N_DEPT, N_DOC, N_PAT, N_APPT = 10, 200, 20_000, 100_000
db.executemany("INSERT INTO Departments(DeptName) VALUES (?)",
               [(f"Department {i}",) for i in range(1, N_DEPT + 1)])
db.executemany("INSERT INTO Doctors(Name,Specialty,DeptID) VALUES (?,?,?)",
               [(f"Dr. {i}", "General", random.randint(1, N_DEPT)) for i in range(1, N_DOC + 1)])
db.executemany("INSERT INTO Patients(Name,DOB,ContactInfo) VALUES (?,?,?)",
               [(f"Patient {i}", "1990-01-01", f"p{i}@mail.com") for i in range(1, N_PAT + 1)])
start = datetime.date(2025, 1, 1)
statuses = ["Scheduled", "Completed", "Cancelled", "Rescheduled"]
db.executemany("INSERT INTO Appointments(PatientID,DoctorID,AppointmentDate,Status) VALUES (?,?,?,?)",
               [(random.randint(1, N_PAT), random.randint(1, N_DOC),
                 (start + datetime.timedelta(days=random.randint(0, 700))).isoformat(),
                 random.choice(statuses)) for _ in range(N_APPT)])
db.executemany("INSERT INTO Billing(AppointmentID,Amount,PaymentStatus) VALUES (?,?,?)",
               [(i, round(random.uniform(500, 5000), 2),
                 random.choice(["Pending", "Paid", "Paid", "Failed", "Refunded"]))
                for i in range(1, N_APPT + 1)])
db.commit()

QUERIES = {
 "Q1 patient history (WHERE PatientID)":
   "SELECT a.AppointmentID,a.AppointmentDate,d.Name,a.Status FROM Appointments a "
   "JOIN Doctors d ON a.DoctorID=d.DoctorID WHERE a.PatientID=777",
 "Q2 unpaid bills per patient":
   "SELECT p.PatientID,p.Name,SUM(b.Amount) FROM Patients p JOIN Appointments a ON p.PatientID=a.PatientID "
   "JOIN Billing b ON a.AppointmentID=b.AppointmentID WHERE b.PaymentStatus IN ('Pending','Failed') "
   "GROUP BY p.PatientID,p.Name ORDER BY 3 DESC LIMIT 10",
 "Q3 revenue by department":
   "SELECT dep.DeptName,SUM(b.Amount) FROM Billing b JOIN Appointments a ON b.AppointmentID=a.AppointmentID "
   "JOIN Doctors d ON a.DoctorID=d.DoctorID JOIN Departments dep ON d.DeptID=dep.DeptID GROUP BY dep.DeptName",
 "Q4 scheduled appts on a date":
   "SELECT * FROM Appointments WHERE AppointmentDate='2025-06-15' AND Status='Scheduled'",
}
INDEXES = [
 "CREATE INDEX idx_doctors_deptid ON Doctors(DeptID)",
 "CREATE INDEX idx_appointments_patientid ON Appointments(PatientID)",
 "CREATE INDEX idx_appointments_doctorid ON Appointments(DoctorID)",
 "CREATE INDEX idx_billing_paymentstatus ON Billing(PaymentStatus)",
 "CREATE INDEX idx_appointments_date_status ON Appointments(AppointmentDate,Status)",
]

out = []
def log(s=""): print(s); out.append(s)

def run(label):
    log(f"\n######## {label} ########")
    times = {}
    for name, q in QUERIES.items():
        plan = [r[3] for r in db.execute("EXPLAIN QUERY PLAN " + q)]
        t = []
        for _ in range(5):
            s = time.perf_counter(); db.execute(q).fetchall(); t.append(time.perf_counter() - s)
        times[name] = min(t) * 1000
        log(f"\n{name}\n  best of 5: {times[name]:.2f} ms")
        for p in plan: log(f"  plan: {p}")
    return times

log(f"MIVACARE HOSPITAL benchmark | SQLite {sqlite3.sqlite_version} | rows: "
    f"{N_PAT} patients, {N_DOC} doctors, {N_APPT} appointments, {N_APPT} bills")
before = run("BEFORE indexes")
for ddl in INDEXES: db.execute(ddl)
db.execute("ANALYZE")
after = run("AFTER indexes")

log("\n######## SUMMARY (ms, best of 5) ########")
log(f"{'Query':40}{'Before':>10}{'After':>10}{'Speed-up':>10}")
for k in QUERIES:
    log(f"{k:40}{before[k]:>10.2f}{after[k]:>10.2f}{before[k]/after[k]:>9.1f}x")

(ROOT / "results").mkdir(exist_ok=True)
(ROOT / "results" / "benchmark_output.txt").write_text("\n".join(out) + "\n")
