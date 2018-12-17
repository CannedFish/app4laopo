# -*- coding: utf8 -*-
import logging

from flask_restplus import Namespace, Resource

from .serializers import Distance as distance
from .models import Distance as DistanceModel

LOG = logging.getLogger(__name__)

api = Namespace('disks'
        , description='Disks related operations'
        , path='/distance')

api.models[distance.name] = distance

@api.route('/')
class DistanceList(Resource):
    @api.doc('list distances')
    @api.marshal_list_with(distance)
    def get(self):
        pass
