#!/bin/bash
app="analytics"
docker build -t ${app}
docker volume create user-storage .
docker run -d \
--name ${app} \
--mount source=user-storage,target=/app \ 