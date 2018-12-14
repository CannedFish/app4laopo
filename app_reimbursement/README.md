# The Reimbursement Application
=============

This repository contains an implementation of RESTful API for laopo application based on Flask and Flask-RESTPlus.

## Initialize

``` shell
>>> from reimbursement.app import initialize_app, app
>>> from reimbursement.database import reset_db
>>>
>>> initialize_app(app)
>>> with app.app_context():
...     reset_db()
```

