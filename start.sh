#!/bin/bash

## volume is located in host at /var/lib/docker/volumes/<volume-name>/
app="analytics"
volume="user-storage"
docker build . -t ${app}
docker volume create ${volume}
docker run -d -v ${volume}:/home/david/temp/docker ${app}