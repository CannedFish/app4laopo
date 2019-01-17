# -*- coding: utf8 -*-

import logging
import requests
import time

from reimbursement.settings import KEY
from reimbursement.v1.distance.models import Distance

LOG = logging.getLogger(__name__)

UPPER_LIMIT = 30
WAIT = 2
RETRY = 5

def cal_distance(srcs, dsts):
    """
    :param src array<HospitalModel>: origins of hospital
    :param dsts array<HospitalModel>: destinations of hospital
    """
    if len(srcs) == 0 or len(dsts) == 0:
        LOG.warning('Call cal_distance with empty paramters')
        return {'status': 2, \
                'message': 'Call cal_distance with empty paramters'}

    url = 'http://api.map.baidu.com/routematrix/v2/driving'
    payload = {
        'output': 'json',
        'origins': '|'.join(['%f,%f' % (src.lat, src.lng) for src in srcs]),
        'destinations': '|'.join(['%f,%f' % (dst.lat, dst.lng) for dst in dsts]),
        'ak': KEY
    }
    for _ in range(RETRY):
        res = requests.get(url, params=payload)
        LOG.debug("Calculate distances request to %s" % res.url)
        time.sleep(WAIT)
        LOG.info("Waited for %d second(s)" % WAIT)
        ret = res.json()
        if ret['status'] == 401:
            LOG.error("Calc failed: %d, %s" % (ret['status'], ret['message']))
            LOG.debug("Retring by %d time" % _+1)
            continue
        return ret

def trans_new_hospital_to_distance(hospitals, old):
    if len(old) == 0:
        old.append(hospitals[0])

    for h in hospitals[1:]:
        for idx in range(len(old)/UPPER_LIMIT+1):
            start = UPPER_LIMIT*idx
            old_slice = old[start:start+UPPER_LIMIT]

            ret = cal_distance([h], old_slice)
            if ret['status'] == 0:
                Distance.create({'distances': [{'src_id': h.id, \
                        'dst_id': oh.id, \
                        'distance': r['distance']['value']} \
                        for oh, r in zip(old_slice, ret['result'])]})
            else:
                LOG.error("Calc failed: %d, %s" % (ret['status'], ret['message']))

            ret = cal_distance(old_slice, [h])
            if ret['status'] == 0:
                Distance.create({'distances': [{'src_id': oh.id, \
                        'dst_id': h.id, \
                        'distance': r['distance']['value']} \
                        for oh, r in zip(old_slice, ret['result'])]})
            else:
                LOG.error("Calc failed: %d, %s" % (ret['status'], ret['message']))

        old.append(h)

    return old

def location_search(name):
    url = 'http://api.map.baidu.com/place/v2/search'
    payload = {
        'output': 'json',
        'ak': KEY,
        'region': '北京',
        'query': name
    }
    for _ in range(RETRY):
        res = requests.get(url, params=payload)
        LOG.debug("[Get location] request to %s" % res.url)
        time.sleep(WAIT)
        LOG.info("Waited for %d second(s)" % WAIT)
        ret = res.json()
        if ret['status'] == 401:
            LOG.error("Calc failed: %d, %s" % (ret['status'], ret['message']))
            LOG.debug("Retring by %d time" % _+1)
            continue
        return ret

