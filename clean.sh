#!/bin/bash
docker-compose down
sudo rm -rf db
docker volume prune