#!/bin/bash

cd ..
#Create virtual enviroment
python3 -m venv ./venv
#Activate virtual enviroment
source venv/bin/activate
#Instal required libraries
cd installation_and_setup
pip install -r requirements.txt

#Generate Django secret-key
cd ..
cd backend/key_value_server/key_value_server
secret_key=$(python3 -c "import secrets; print(secrets.token_urlsafe())")
## Add secret-key to .env
echo "DJANGO_SECRET_KEY=django-insecure-$secret_key" >> .env
