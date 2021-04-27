#!/bin/bash
docker-compose up -d zookeeper
docker-compose up -d kafka
docker-compose up -d kafdrop
docker-compose up -d connect
docker-compose up -d db
docker-compose up -d app