"""
Renders REAL script output as terminal-style images for the MIVACARE HOSPITAL portfolio.
These are NOT MySQL Workbench screenshots: they are captures of SQLite output produced by
the scripts in this repository. Re-run any time:  python3 screenshots/render_evidence.py
"""
import sqlite3, pathlib, textwrap
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = pathlib.Path(__file__).resolve().parent
SQL = ROOT / "portfolio-1-database-design" / "sql"

def render(lines, title, fname):
    lines = [l.expandtabs(4) for l in lines]
    w = max(len(l) for l in lines + [title]) 
    fig_w = max(9, min(16, w * 0.105 + 0.8)); fig_h = 0.9 + 0.2 * len(lines)
    fig = plt.figure(figsize=(fig_w, fig_h), facecolor="#1e1e1e")
    ax = fig.add_axes([0, 0, 1, 1]); ax.axis("off"); ax.set_xlim(0, fig_w); ax.set_ylim(0, fig_h)
    ax.add_patch(plt.Rectangle((0, fig_h - 0.45), fig_w, 0.45, color="#333333"))
    ax.text(0.2, fig_h - 0.23, title, color="#dddddd", fontsize=9, va="center", family="DejaVu Sans")
    for i, l in enumerate(lines):
        c = "#9cdcfe" if l.startswith(("#", "MIVACARE")) else "#ce9178" if "plan:" in l else \
            "#6a9955" if l[:2].strip() and l[0].isdigit() else "#d4d4d4"
        ax.text(0.2, fig_h - 0.75 - 0.2 * i, l, color=c, fontsize=8.5, family="DejaVu Sans Mono", va="center")
    fig.savefig(OUT / fname, dpi=130, facecolor=fig.get_facecolor()); plt.close(fig)
    print("wrote", fname)

TAG = " – MIVACARE HOSPITAL – SQLite 3.45.1 script output (not MySQL Workbench)"

# ---------- Portfolio 1: schema + data loaded ----------
db = sqlite3.connect(":memory:")
db.executescript((SQL / "schema_sqlite.sql").read_text() + (SQL / "sample_data_sqlite.sql").read_text())
L = ["$ sqlite3 mivacare.db < schema_sqlite.sql sample_data_sqlite.sql", "", "-- tables created:"]
for (n,) in db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY 1"):
    cols = [f"{c[1]} {c[2]}{' PK' if c[5] else ''}" for c in db.execute(f"PRAGMA table_info({n})")]
    cnt = db.execute(f"SELECT COUNT(*) FROM {n}").fetchone()[0]
    L.append(f"  {n} ({cnt} rows): " + ", ".join(cols))
L += ["", "-- foreign keys:"]
for t in ("Doctors", "Appointments", "Billing"):
    for f in db.execute(f"PRAGMA foreign_key_list({t})"):
        L.append(f"  {t}.{f[3]} -> {f[2]}.{f[4]}")
render([textwrap.fill(x, 118, subsequent_indent="      ") if len(x) > 118 else x for x in L] and
       sum([textwrap.wrap(x, 118, subsequent_indent="      ") or [""] for x in L], []),
       "Portfolio 1 – schema created and sample data loaded" + TAG, "p1-schema-and-data.png")

# ---------- Portfolio 2: query results ----------
q = (ROOT / "portfolio-2-query-optimisation" / "hospital_queries.sql").read_text()
blocks = [b.strip() for b in q.split(";") if "SELECT" in b]
L = []
for b in blocks[:6]:
    title = [x for x in b.splitlines() if x.startswith("-- ")][-1][3:]
    sql = "\n".join(x for x in b.splitlines() if not x.startswith("--"))
    cur = db.execute(sql); cols = [d[0] for d in cur.description]; rows = cur.fetchall()
    L.append(f"{title}  [{len(rows)} rows]")
    L.append("  " + " | ".join(cols))
    for r in rows: L.append("  " + " | ".join(str(v) for v in r))
    L.append("")
render(L[:-1], "Portfolio 2 – query results (queries 1–6)" + TAG, "p2-query-results.png")

bench = (ROOT / "portfolio-2-query-optimisation" / "results" / "benchmark_output.txt").read_text().splitlines()
i_b = next(i for i, l in enumerate(bench) if "BEFORE" in l); i_a = next(i for i, l in enumerate(bench) if "AFTER" in l)
i_s = next(i for i, l in enumerate(bench) if "SUMMARY" in l)
render([bench[0], ""] + [l for l in bench[i_b:i_a] if l.strip() or True],
       "Portfolio 2 – execution plans BEFORE indexing" + TAG, "p2-explain-before-index.png")
render([bench[0], ""] + bench[i_a:i_s], "Portfolio 2 – execution plans AFTER indexing" + TAG, "p2-explain-after-index.png")
render(bench[i_s:], "Portfolio 2 – performance summary (before vs after)" + TAG, "p2-performance-summary.png")

# ---------- Portfolio 3 ----------
t = (ROOT / "portfolio-3-transactions-concurrency" / "results" / "transaction_output.txt").read_text().splitlines()
def sec(a, b=None):
    s = next(i for i, l in enumerate(t) if l.startswith(a)); e = next((i for i, l in enumerate(t) if b and l.startswith(b)), len(t))
    return t[s:e]
render([t[0], ""] + sec("1.", "3.")[:-1], "Portfolio 3 – COMMIT and ROLLBACK" + TAG, "p3-commit-rollback.png")
render(sec("3.", "5.")[:-1], "Portfolio 3 – atomicity (constraint failure) and SAVEPOINT" + TAG, "p3-atomicity-savepoint.png")
render(sec("5."), "Portfolio 3 – concurrency control (duplicate payment prevented)" + TAG, "p3-concurrency.png")
