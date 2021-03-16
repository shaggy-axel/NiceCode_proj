#!/bin/bash

pip install -U pip
pip install git
mkdir django-dev
git clone https://github.com/shaggy-axel/NiceCode_proj.git ~/django-dev
cd ~/django-dev
pip install -r requirements.txt
# shellcheck disable=SC1009
sudo apt install python3-venv
python3 -m venv my_env
source my_env/bin/activate
python3 manage.py migrate
python3 manage.py runserver

