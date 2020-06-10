#!/bin/bash

sudo systemctl restart hishamapp5.service

sudo nginx -t
sudo nginx -s reload
