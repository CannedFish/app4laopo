# -*- coding: utf8 -*-

from flask_restplus import Namespace, Resource, fields

api = Namespace('disks'
        , description='Disks related operations'
        , path='/distance')

vm = api.model('Disk', {})
