# -*- coding: utf8 -*-

import logging
import requests

from reimbursement.settings import KEY
from reimbursement.v1.distance.models import Distance

LOG = logging.getLogger(__name__)

def cal_distance(srcs, dsts):
    """
    :param src array<HospitalModel>: origins of hospital
    :param dsts array<HospitalModel>: destinations of hospital
    """
    if len(srcs) == 0 or len(dsts) == 0:
        LOG.warning('Call cal_distance with empty peramters')
        return {'status': 2}

    url = 'http://api.map.baidu.com/routematrix/v2/driving'
    payload = {
        'output': 'json',
        'origins': '|'.join(['%f,%f' % (src.lng, src.lat) for src in srcs]),
        'destinations': '|'.join(['%f,%f' % (dst.lng, dst.lat) for dst in dsts]),
        'ak': KEY
    }
    res = requests.get(url, params=payload)
    LOG.debug("Calculate distances request to %s" % res.url)
    return res.json()

def trans_new_hospital_to_distance(hospitals, old):
    for h in hospitals:
        ret = cal_distance([h], old)
        if ret['status'] == 0:
            Distance.create({'distances': [{'src_id': h.id, \
                    'dst_id': oh.id, \
                    'distance': r['distance']['value']} \
                    for oh, r in zip(old, ret['result'])]})

        ret = cal_distance(old, [h])
        if ret['status'] == 0:
            Distance.create({'distances': [{'src_id': oh.id, \
                    'dst_id': h.id, \
                    'distance': r['distance']['value']} \
                    for oh, r in zip(old, ret['result'])]})

        old.append(h)

    return old

