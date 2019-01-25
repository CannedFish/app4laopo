# Deploy

```shell
virtualenv venv
source venv/bin/activate
pip install -e .
flask init-db

export FLASK_ENV=product

sudo mkdir /var/log/app4laopo
sudo chown <user>:<group> /var/log/app4laopo

# Deploy with waitress
pip install waitress
waitress-serve --call 'app4laopo:create_app'

# Deploy with apache2 on ubuntu
sudo apt install libapache2-mod-wsgi
sudo a2enmod wsgi_mod
# Add custom ports by modifing /etc/apache2/ports.conf
sudo mkdir /var/www/app4laopo
ln -s /path/to/app4laopo_ui.wsgi /var/www/app4laopo/app4laopo_ui.wsgi
ln -s /path/to/app4laopo.conf /etc/apache2/sites-available/app4laopo.conf
sudo a2ensite app4laopo.conf
sudo systemctl reload apache2

tail -f /var/log/app4laopo/ui.log
```
