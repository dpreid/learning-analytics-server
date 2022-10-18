#!/bin/bash
app="analytics"
volume="user-storage"
docker build . -t ${app}
docker volume create ${volume}
docker run -d \
  --name ${app} \
  --mount source=${volume},target=/app \
  ${app}