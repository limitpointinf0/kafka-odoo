#!/bin/bash

#remove all containers
docker-compose down
#remove database volume
sudo rm -rf db
#remove any json
sudo rm data/*
#remove all docker volumes
docker volume prune