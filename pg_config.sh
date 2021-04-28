#!/bin/bash

# dont do this!
docker exec -it db psql -U odoo -W kafka -c "ALTER USER odoo WITH SUPERUSER;"
#set wal level to logical
docker exec -it db psql -U odoo -W kafka -c "ALTER SYSTEM SET wal_level = 'logical';"
#restart db container
docker-compose restart db
sleep 20
#show wal level
docker exec -it db psql -U odoo -W kafka -c "SHOW wal_level;"
#create publications
docker exec -it db psql -U odoo -W kafka -c "CREATE PUBLICATION dbz_publication FOR TABLE pos_order, pos_order_line;"
#query all publications + tables
docker exec -it db psql -U odoo -W kafka -c "SELECT * FROM pg_catalog.pg_publication pub LEFT JOIN pg_catalog.pg_publication_tables tab ON pub.pubname = tab.pubname;"
