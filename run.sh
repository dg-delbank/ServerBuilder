#!/bin/bash

sudo apt-get update -y && sudo apt-get upgrade -y
sudo apt install docker.io -y
sudo apt install docker-compose-v2 -y
sudo ufw allow OpenSSH
python3 app.py 