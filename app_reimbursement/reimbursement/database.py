# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def reset_db():
    from reimbursement.v1.hospital.models import Hospital # noqa
    db.drop_all()
    db.create_all()

