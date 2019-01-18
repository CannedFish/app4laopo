# Deploy

```shell
virtualenv venv
source venv/bin/activate
python install -e .
flask init-db
pip install waitress
export FLASK_ENV=product
waitress-serve --call 'app4laopo:create_app'
```
