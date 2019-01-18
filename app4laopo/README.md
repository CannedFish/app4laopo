# Deploy

```shell
virtualenv venv
source venv/bin/activate
pip install -e .
flask init-db

pip install waitress
export FLASK_ENV=product

sudo mkdir /var/log/app4laopo
sudo chown simon:simon /var/log/app4laopo
waitress-serve --call 'app4laopo:create_app'

tail -f /var/log/app4laopo/ui.log
```
