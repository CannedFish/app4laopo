# The Reimbursement Application
=============

This repository contains an implementation of RESTful API for laopo application based on Flask and Flask-RESTPlus.

## Install

``` shell
virtualenv venv
source venv/bin/activate
pip install -e .
```

## Initialize

``` shell
python tools.py -c db
```

## Deploy for development

``` shell
python reimbursement/app.py
```

## Deploy for production

``` shell
# Deploy with apache2 on ubuntu
sudo apt install libapache2-mod-wsgi
sudo a2enmod wsgi_mod
# Add custom ports by modifing /etc/apache2/ports.conf
sudo mkdir /var/www/app4laopo
ln -s /path/to/app_reimbursement.wsgi /var/www/app4laopo/app_reimbursement.wsgi
ln -s /path/to/app_reimbursement.conf /etc/apache2/sites-available/app_reimbursement.conf
sudo a2ensite app_reimbursement.conf
sudo systemctl reload apache2
```

