# -*- coding: utf-8 -*-

from flask import Blueprint
from flask_restplus import Api

from .auth import api as auth_ns
from .hospital import api as hospital_ns
from .distance import api as distance_ns
from .location import api as location_ns

blueprint = Blueprint('api_v1', __name__, url_prefix='/api/v1')
api = Api(
    blueprint,
    title='RESTful API for reimbeursement application',
    version='1.0',
    description='A description',
    # All API metadatas
)

api.add_namespace(auth_ns)
api.add_namespace(hospital_ns)
api.add_namespace(distance_ns)
api.add_namespace(location_ns)

