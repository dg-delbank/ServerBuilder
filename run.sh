#!/bin/bash

apt-get update -y && apt-get upgrade -y
apt install docker.io -y
apt install docker-compose-v2 -y
python3 app.py 