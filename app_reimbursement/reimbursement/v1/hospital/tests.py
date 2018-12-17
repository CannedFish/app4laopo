# -*- coding: utf-8 -*-

import unittest
import requests
import json

class HospitalTest(unittest.TestCase):
    def setUp(self):
        self.base = 'http://127.0.0.1:5000/api/v1/hospital'

    def _create_hospital(self):
        url = self.base + '/'
        data = {
            "hospitals": [
                {
                    'name_ch': 'A医院',
                    'name_en': 'A hospital',
                    'address': 'Some where A'
                },
                {
                    'name_ch': 'B医院',
                    'name_en': 'B hospital',
                    'address': 'Some where B'
                }
            ]
        }
        headers = {
            'Content-Type': 'application/json'
        }
        res = requests.post(url, data=json.dumps(data), headers=headers)
        self.assertEqual(res.status_code, 201)
        return res.json()

    def _get_hospital_list(self):
        url = self.base + '/'
        res = requests.get(url)
        self.assertEqual(res.status_code, 200)
        return res.json()

    def _get_hospital(self, hospital_id):
        url = self.base + '/' + hospital_id
        res = requests.get(url)
        self.assertEqual(res.status_code, 200)
        return res.json()

    def _update_hospital(self, hospital_id):
        data = {
            'id': hospital_id,
            'name_ch': hospital_id + u'医院',
            'name_en': '%s hospital new' % hospital_id,
            'address': 'Some where %s new' % hospital_id
        }
        url = self.base + '/' + hospital_id
        headers = {
            'Content-Type': 'application/json'
        }
        res = requests.put(url, data=json.dumps(data), headers=headers)
        self.assertEqual(res.status_code, 200)
        return res.json()

    def _delete_hospital(self, hospital_id):
        url = self.base + '/' + hospital_id
        res = requests.delete(url)
        self.assertEqual(res.status_code, 200)
        return res.json()

    def test_hospital(self):
        hospitals = self._create_hospital()
        print hospitals
        print self._get_hospital_list()
        for hospital in hospitals['hospitals']:
            print self._get_hospital(hospital['id'])
            print self._update_hospital(hospital['id'])
            print self._delete_hospital(hospital['id'])

if __name__ == '__main__':
    unittest.main()
