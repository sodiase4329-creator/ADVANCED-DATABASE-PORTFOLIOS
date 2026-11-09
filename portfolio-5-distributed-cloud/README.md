# Portfolio 5 – Distributed and Cloud Database Exercise (MIVACARE HOSPITAL)

| Item | File |
|---|---|
| MySQL primary + replica (Docker) | [docker-compose.mysql-replication.yml](docker-compose.mysql-replication.yml), [replication_setup.sql](replication_setup.sql) |
| MongoDB replica set and sharding | [mongodb_sharding_commands.js](mongodb_sharding_commands.js) |

## Design for MIVACARE HOSPITAL
- **Replication:** one primary handles writes (bookings, payments); one or more read replicas serve reports and the patient portal, reducing load and giving a failover target.
- **Availability:** a three-node MongoDB replica set elects a new primary automatically if one node fails; MySQL needs promotion of a replica (or managed failover on cloud).
- **Consistency (CAP):** appointments and billing need strong consistency, so they use the primary or `w: majority`. Dashboards can tolerate replica lag (eventual consistency).
- **Sharding:** if patient volume outgrows one server, shard `patients` on a hashed `_id` to spread data and writes evenly. Sharding by appointment date would create hot shards.
- **Cloud deployment:** a managed service such as Amazon RDS for MySQL (Multi-AZ plus read replicas) or MongoDB Atlas removes patching and backup work. Hospital data is sensitive, so use encryption at rest and in transit, private networking and role-based access.

These configurations are provided as design and setup files. They were not executed in this environment, so they are presented as design material.

## Evidence
No screenshots yet: these files were written as design/setup material and have not been executed.
