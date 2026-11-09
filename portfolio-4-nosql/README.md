# Portfolio 4 – NoSQL and Advanced Data Models (MIVACARE HOSPITAL)

| Item | File |
|---|---|
| Single patient document | [nosql_patient.json](nosql_patient.json) |
| Full collection (same 4 patients as the SQL sample data) | [patients_collection.json](patients_collection.json) |
| MongoDB schema validation, CRUD, aggregation, index | [mongodb_commands.js](mongodb_commands.js) |
| Key-value / graph design examples | [redis_keyvalue_example.md](redis_keyvalue_example.md) |

## Model
Document model (MongoDB). Each patient is one document with **embedded** appointments, doctor summary and bill, so the whole patient history is one read with no joins.

## Suitability
- **Good fit:** patient-centric reads, flexible medical history (varying fields), horizontal scaling by patient id.
- **Trade-offs:** doctor details are duplicated inside appointments (update anomalies), and cross-patient reports need aggregation. This is why the relational design remains the system of record for billing, and MongoDB serves as a read-optimised patient view.

Both JSON files were validated as well-formed JSON. The MongoDB script was written but not executed in this environment; run it with `mongosh` and screenshot the output.
