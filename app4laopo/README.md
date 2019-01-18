# Deploy

```shell
virtualenv venv
source venv/bin/activate
pip install -e .
flask init-db
pip install waitress
export FLASK_ENV=product
waitress-serve --call 'app4laopo:create_app'
```
