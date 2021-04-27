#!/bin/bash

#set wal level to logical
docker exec -it db psql -U odoo -W kafka -c "ALTER SYSTEM SET wal_level = 'logical';"
#restart db container
docker-compose restart db
sleep 20
#show wal level
docker exec -it db psql -U odoo -W kafka -c "SHOW wal_level;"
#create the first publication
docker exec -it db psql -U odoo -W kafka -c "CREATE PUBLICATION odoo_publication FOR TABLE pos_order;"
#query all publications + tables
docker exec -it db psql -U odoo -W kafka -c "SELECT * FROM pg_catalog.pg_publication pub LEFT JOIN  pg_catalog.pg_publication_tables tab ON pub.pubname = tab.pubname;"

# FOR ADDING TABLE TO PUBLICATION
# ALTER PUBLICATION odoo_publication ADD TABLE pos_order_line;