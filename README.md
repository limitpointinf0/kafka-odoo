# Getting Started With Kafka - Odoo CDC Implementation using Docker Compose
Example for integrating a legacy app into Kafka.

## Installation

You must install docker and docker-compose before you begin.
You may use the following script to install: https://gist.githubusercontent.com/limitpointinf0/6a9490ff4fef82a0b385d8a07c15a5c7/raw/5caf17d077fe5e17ffa2eba25fc5c0486e0b657d/install_docker.sh 

## TLDR
```bash
chmod +x start.sh
chmod +x clean.sh
chmod +x pg_config.sh

#step 1: build containers
./start.sh

#step 2: create a db named 'kafka' with demo data from localhost:8069

#step 3: alter db
./pg_config.sh

#step 4: create connector
curl -i -X POST -H "Accept:application/json" -H "Content-Type:application/json" localhost:8083/connectors/ -d '{ "name": "odoo-connector", "config": { "connector.class": "io.debezium.connector.postgresql.PostgresConnector", "tasks.max": "1", "database.hostname": "db", "database.port": "5432", "database.user": "odoo", "database.password": "odoo", "database.server.id": "184054", "database.server.name": "odoo", "database.dbname": "kafka", "database.whitelist": "kafka", "table.whitelist": "public.res_users,public.res_partner", "database.history.kafka.bootstrap.servers": "kafka:9092", "database.history.kafka.topic": "schema-changes.odoo", "decimal.handling.mode": "double", "plugin.name":"pgoutput", "publication.name":"odoo_publication"}}'

#step 5: watch users table
docker compose up watcher

#step 6: create a new user and watch change in watcher
```

## Local Demo
- Run all of the following to set up the full environment:
```bash
#set up kafka
docker-compose up -d zookeeper
docker-compose up -d kafka
docker-compose up -d kafdrop
docker-compose up -d connect
#set up application
docker-compose up -d db
docker-compose up -d app
```
- Go to localhost:8069 and create the database: kafka (with demo data)

- Connect to the postgres container and set the WAL level to logical and restart the container
```bash
# dont do this!
docker exec -it db psql -U odoo -W kafka -c "ALTER USER odoo WITH SUPERUSER;"
#set wal level to logical
docker exec -it db psql -U odoo -W kafka -c "ALTER SYSTEM SET wal_level = 'logical';"
#restart db container
docker-compose restart db
#show wal level
docker exec -it db psql -U odoo -W kafka -c "SHOW wal_level;"
#create publications
docker exec -it db psql -U odoo -W kafka -c "CREATE PUBLICATION odoo_publication FOR TABLE pos_order, pos_order_line;"
#query all publications + tables
docker exec -it db psql -U odoo -W kafka -c "SELECT * FROM pg_catalog.pg_publication pub LEFT JOIN  pg_catalog.pg_publication_tables tab ON pub.pubname = tab.pubname;"
```

#creating the connector in Kafka for Postgres
```bash
curl -i -X POST -H "Accept:application/json" -H "Content-Type:application/json" localhost:8083/connectors/ -d '{ "name": "odoo-connector", "config": { "connector.class": "io.debezium.connector.postgresql.PostgresConnector", "tasks.max": "1", "database.hostname": "db", "database.port": "5432", "database.user": "odoo", "database.password": "odoo", "database.server.id": "184054", "database.server.name": "odoo", "database.dbname": "kafka", "database.whitelist": "kafka", "table.whitelist": "public.pos_order,public.pos_order_line", "database.history.kafka.bootstrap.servers": "kafka:9092", "database.history.kafka.topic": "schema-changes.odoo", "decimal.handling.mode": "double", "plugin.name":"pgoutput"}}'

#watch the changes
docker compose up watcher
```
- Navigate to localhost:8069 and create a new partner or user

- Check the output in the watcher container


## Extra
```bash
#start mysql container
docker-compose up -d db2

#make connector
curl -i -X POST -H "Accept:application/json" -H "Content-Type:application/json" localhost:8083/connectors/ -d '{ "name": "inventory-connector", "config": { "connector.class": "io.debezium.connector.mysql.MySqlConnector", "tasks.max": "1", "database.hostname": "db2", "database.port": "3306", "database.user": "debezium", "database.password": "dbz", "database.server.id": "184054", "database.server.name": "dbserver1", "database.whitelist": "inventory", "database.history.kafka.bootstrap.servers": "kafka:9092", "database.history.kafka.topic": "dbhistory.inventory" } }'
```
- connect to mysql container
    - host: localhost
    - database: inventory
    - username: root
    - password: debezium
    - port: 3306

```sql
insert into customers(first_name, last_name, email) values ('FIRST NAME', 'LAST NAME', 'YOUREMAIL@EMAIL.COM');
update customers set email='NEWEMAIL@acme.com' where id=1005;
```

## Cleanup
```bash
./clean.sh
```
## License
[MIT](https://choosealicense.com/licenses/mit/)