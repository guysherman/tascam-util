#! /bin/sh
virtualenv .env
sh ./.env/bin/activate
pip3 install -r requirements.txt
