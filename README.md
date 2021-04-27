# Getting Started With Kafka - Odoo CDC Implementation using Docker Compose
Example for integrating a legacy app into Kafka.

## Installation

You must install docker and docker-compose before you begin.
You may use the following script to install: https://gist.githubusercontent.com/limitpointinf0/6a9490ff4fef82a0b385d8a07c15a5c7/raw/5caf17d077fe5e17ffa2eba25fc5c0486e0b657d/install_docker.sh 

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
- Connect to the postgres container and set the WAL level to logical
```sql
ALTER SYSTEM SET wal_level = 'logical';
```
- Restart the postgres container

- Install the POS module in Odoo

#creating the connector in Kafka for Postgres
```bash
curl -i -X POST -H "Accept:application/json" -H "Content-Type:application/json" localhost:8083/connectors/ -d '{ "name": "pos-order-connector", "config": { "connector.class": "io.debezium.connector.postgresql.PostgresConnector", "tasks.max": "1", "database.hostname": "db", "database.port": "5432", "database.user": "odoo", "database.password": "odoo", "database.server.id": "184054", "database.server.name": "odoo", "database.dbname": "kafka", "database.whitelist": "kafka", "table.whitelist": "public.pos_order", "database.history.kafka.bootstrap.servers": "kafka:9092", "database.history.kafka.topic": "schema-changes.odoo", "decimal.handling.mode": "double", "plugin.name":"pgoutput", "publication.name":"odoo_publication"}}'

#watch the changes
docker compose up watcher
```
- Navigate to localhost:8069 and create a POS Order

- Check the output in the watcher container


## License
[MIT](https://choosealicense.com/licenses/mit/)