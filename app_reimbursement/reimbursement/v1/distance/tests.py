# -*- coding: utf-8 -*-
import unittest
import random
import uuid
import requests

from .utils import cal_distance\
        , trans_new_hospital_to_distance

class Pos(object):
    def __init__(self, lng, lat):
        self.id = str(uuid.uuid4())
        self.lng = lng
        self.lat = lat

class UtilsTest(unittest.TestCase):
    def test_cal_distance(self):
        src = Pos(40.45, 116.34)
        dst = [Pos(round(random.uniform(40, 42), 2), \
                round(random.uniform(116, 118), 2), \
                ) for _ in range(3)]
        res = cal_distance(src, dst)
        self.assertEqual(res['status'], 0)
        self.assertEqual(len(res['result']), 3)
        print res

    def test_trans_new_hospital_to_distance(self):
        res = trans_new_hospital_to_distance([Pos(round(random.uniform(40, 42), 2), \
                round(random.uniform(116, 118), 2), \
                ) for _ in range(3)])
        self.assertEqual(len(old), 5)

class DistanceTest(unittest.TestCase):
    def test_list(self):
        url = 'http://localhost:5000/api/v1/distance/'
        payload = {
            'num': 10,
            'target': 20
        }
        res = requests.get(url, params=payload)
        self.assertEqual(res.status_code, 200)
        print res.json()

