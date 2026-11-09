// MIVACARE HOSPITAL - Portfolio 4: MongoDB (document model)
// Run with:  mongosh mivacare_hospital mongodb_commands.js
// Import alternative: mongoimport --db mivacare_hospital --collection patients --file patients_collection.json --jsonArray

db.patients.drop();
db.createCollection("patients", {
  validator: { $jsonSchema: {
    bsonType: "object",
    required: ["_id", "name", "dob", "appointments"],
    properties: {
      name: { bsonType: "string" },
      appointments: { bsonType: "array",
        items: { bsonType: "object", required: ["appointmentId", "date", "status"],
          properties: { status: { enum: ["Scheduled", "Completed", "Cancelled", "Rescheduled"] } } } }
    } } }
});

// Load the data with mongoimport (or Compass > Import) instead of cat():
//   mongoimport --db mivacare_hospital --collection patients --file patients_collection.json --jsonArray

// 1. Retrieve full patient history in ONE read (no joins)
db.patients.findOne({ _id: "P001" });

// 2. Patients with unpaid bills
db.patients.find({ "appointments.bill.paymentStatus": { $in: ["Pending", "Failed"] } }, { name: 1, "appointments.bill": 1 });

// 3. Revenue by department (aggregation pipeline)
db.patients.aggregate([
  { $unwind: "$appointments" },
  { $group: { _id: "$appointments.department", revenue: { $sum: "$appointments.bill.amount" } } },
  { $sort: { revenue: -1 } }
]);

// 4. Book a new appointment (embedded document push)
db.patients.updateOne({ _id: "P002" }, { $push: { appointments: {
  appointmentId: 5, date: "2026-11-10", status: "Scheduled",
  doctor: { id: 1, name: "Dr. Anna Mensah", specialty: "Cardiologist" }, department: "Cardiology",
  bill: { billId: 5, amount: 2500.00, currency: "NGN", paymentStatus: "Pending" } } } });

// 5. Index for fast lookup by appointment status/date
db.patients.createIndex({ "appointments.status": 1, "appointments.date": 1 });
db.patients.find({ "appointments.status": "Scheduled" }).explain("executionStats");
