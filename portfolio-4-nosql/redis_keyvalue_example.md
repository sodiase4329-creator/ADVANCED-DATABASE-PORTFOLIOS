# Key-value and graph extensions (MIVACARE HOSPITAL)

**Redis (key-value) – fast appointment slot lookup / session cache**
```
SET   doctor:1:slot:2026-10-05T09:00 "available"
SET   doctor:1:slot:2026-10-05T09:00 "booked:P002" NX      # NX = only if still free (prevents double booking)
HSET  patient:P001 name "John Smith" lastVisit "2026-10-01"
EXPIRE session:abc123 1800
```

**Neo4j (graph) – doctor/patient referral network**
```
CREATE (:Patient {id:'P001'})-[:BOOKED]->(:Appointment {id:1})<-[:ATTENDED_BY]-(:Doctor {id:1})
MATCH (p:Patient)-[:BOOKED]->()-[:ATTENDED_BY]->(d:Doctor) RETURN d.name, count(p)
```
These are design examples; they were not executed for this submission.
