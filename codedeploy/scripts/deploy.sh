#!/bin/bash

# Ensure ssh agent running & add deploy key
eval $(ssh-agent)
ssh-add /home/ubuntu/.ssh/hishamapp5

# Deploy new version of the project
sudo rm -rf /home/ubuntu/hishamapp5
git clone git@github.com:Ureed-Tarjama/mt_translation_tool.git /home/ubuntu/hishamapp5 || true

cd /home/ubuntu/hishamapp5
git checkout .
git pull
git checkout master

sudo rm -rf /home/ubuntu/hishamapp5venv
sudo pip3 install virtualenv
virtualenv -p python3 /home/ubuntu/hishamapp5venv

cd /home/ubuntu/hishamapp5/

/home/ubuntu/hishamapp5venv/bin/pip install -r requirements.txt

