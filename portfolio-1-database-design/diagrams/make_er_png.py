"""Redraws the MIVACARE HOSPITAL ER diagram (crow's-foot style) -> ERDiagram_mivacare.png"""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
ent = {
 "Departments": (0.5, 5.0, ["DeptID (PK)", "DeptName (UQ)"]),
 "Doctors":     (5.0, 5.0, ["DoctorID (PK)", "Name", "Specialty", "DeptID (FK)"]),
 "Patients":    (0.5, 1.0, ["PatientID (PK)", "Name", "DOB", "ContactInfo"]),
 "Appointments":(5.0, 1.0, ["AppointmentID (PK)", "PatientID (FK)", "DoctorID (FK)", "AppointmentDate", "Status"]),
 "Billing":     (9.5, 1.0, ["BillID (PK)", "AppointmentID (FK, UQ)", "Amount", "PaymentStatus"]),
}
fig, ax = plt.subplots(figsize=(14, 8)); ax.set_xlim(0, 14); ax.set_ylim(0, 8.2); ax.axis("off")
ax.text(7, 7.8, "MIVACARE HOSPITAL – Entity Relationship Diagram", ha="center", fontsize=16, weight="bold")
box = {}
for n, (x, y, attrs) in ent.items():
    h = 0.95 + 0.38 * len(attrs); w = 3.4
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02", fc="#eef4fb", ec="#1f4e79", lw=1.5))
    ax.add_patch(FancyBboxPatch((x, y + h - 0.5), w, 0.5, boxstyle="round,pad=0.02", fc="#1f4e79", ec="#1f4e79"))
    ax.text(x + w/2, y + h - 0.25, n, ha="center", va="center", color="white", weight="bold", fontsize=12)
    for i, a in enumerate(attrs):
        ax.text(x + 0.15, y + h - 0.85 - 0.38*i, a, va="center", fontsize=10)
    box[n] = (x, y, w, h)
def link(a, b, la, lb, label):
    (x1,y1,w1,h1),(x2,y2,w2,h2) = box[a], box[b]
    if abs(x1-x2) < 0.1:   # vertical (b is below a)
        cx = x1 + w1/2; p1=(cx, y1); p2=(cx, y2+h2)
        ax.plot([p1[0],p2[0]],[p1[1],p2[1]], color="#333", lw=1.5)
        ax.text(cx+0.15, p1[1]-0.35, la, fontsize=12, weight="bold")
        ax.text(cx+0.15, p2[1]+0.15, lb, fontsize=12, weight="bold")
        ax.text(cx+0.3, (p1[1]+p2[1])/2, label, fontsize=10, style="italic", color="#1f4e79")
    else:                  # horizontal, a left of b, drawn at a common y inside both boxes
        y = y1 + 0.5
        p1=(x1+w1, y); p2=(x2, y)
        ax.plot([p1[0],p2[0]],[y,y], color="#333", lw=1.5)
        ax.text(p1[0]+0.1, y+0.15, la, fontsize=12, weight="bold")
        ax.text(p2[0]-0.3, y+0.15, lb, fontsize=12, weight="bold")
        ax.text((p1[0]+p2[0])/2, y-0.4, label, fontsize=10, style="italic", color="#1f4e79", ha="center")
link("Departments","Doctors","1","N","has")
link("Doctors","Appointments","1","N","attends")      # vertical
link("Patients","Appointments","1","N","books")
link("Appointments","Billing","1","1","generates")
fig.savefig(__file__.replace("make_er_png.py","ERDiagram_mivacare.png"), dpi=130, bbox_inches="tight", facecolor="white")
