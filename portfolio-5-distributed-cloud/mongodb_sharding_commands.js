// MIVACARE HOSPITAL - Portfolio 5: MongoDB replica set + sharding (design commands, run in mongosh)
rs.initiate({ _id: "mivacareRS", members: [
  { _id: 0, host: "mongo1:27017" }, { _id: 1, host: "mongo2:27017" }, { _id: 2, host: "mongo3:27017" } ] });
// Read from secondaries for reporting; writes need majority acknowledgement:
db.patients.insertOne({ _id: "P900", name: "Test" }, { writeConcern: { w: "majority", j: true } });
db.getMongo().setReadPref("secondaryPreferred");
// Sharding (on a sharded cluster via mongos): hashed key spreads patients evenly
sh.enableSharding("mivacare_hospital");
sh.shardCollection("mivacare_hospital.patients", { _id: "hashed" });
