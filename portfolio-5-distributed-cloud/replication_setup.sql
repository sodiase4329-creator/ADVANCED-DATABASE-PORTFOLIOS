-- Run on PRIMARY:
CREATE USER 'repl'@'%' IDENTIFIED BY 'replpass';
GRANT REPLICATION SLAVE ON *.* TO 'repl'@'%';

-- Run on REPLICA:
CHANGE REPLICATION SOURCE TO SOURCE_HOST='mysql-primary', SOURCE_USER='repl',
  SOURCE_PASSWORD='replpass', SOURCE_AUTO_POSITION=1, GET_SOURCE_PUBLIC_KEY=1;
START REPLICA;
SHOW REPLICA STATUS\G   -- expect Replica_IO_Running: Yes, Replica_SQL_Running: Yes

-- Verify: insert on primary, read on replica
-- PRIMARY: INSERT INTO Patients(Name,DOB,ContactInfo) VALUES ('Test Patient','2000-01-01','test@mail.com');
-- REPLICA: SELECT * FROM Patients WHERE Name='Test Patient';
