# -*- coding: utf-8 -*-

import argparse
import json
import requests
import logging.config
import os

logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__)\
        , './reimbursement/logging.conf'))
logging.config.fileConfig(logging_conf_path)
LOG = logging.getLogger(__name__)

def _reset_db():
    from reimbursement.app import initialize_app, app
    from reimbursement.database import reset_db

    initialize_app(app)
    with app.app_context():
        reset_db()

def _data_import(_p):
    content = []
    with open(_p, 'r') as fd:
        content = json.loads(fd.read())
    LOG.debug(len(content))
    to_del = []
    for c in content:
        flag = False
        for idx in range(len(content)):
            if c['title'] == content[idx]['title'] or c['address'] == content[idx]['address']:
                if not flag:
                    flag = True
                else:
                    to_del.append(idx)
    payload = [{
        'name_ch': content[idx]["title"], \
        'address': content[idx]["address"], \
        'lng': content[idx]["point"]["lng"], \
        'lat': content[idx]["point"]["lat"]
    } for idx in range(len(content)) if idx not in to_del]
    LOG.debug(len(payload))
    headers = {'Content-Type': 'application/json'}
    # LOG.debug(json.dumps(payload))
    res = requests.post('http://127.0.0.1:5000/api/v1/hospital/'\
            , data = json.dumps({'hospitals': payload}), headers = headers)
    LOG.debug(res.status_code)

def main():
    parser = argparse.ArgumentParser(description="Tools for reimbursement.")
    parser.add_argument('-c', '--cmd', help="sub cmds."\
            , choices=["db", "data"], required=True)
    parser.add_argument('-p', default="./data.dat", help="path of data.")
    args = parser.parse_args();
    if args.cmd == 'db':
        _reset_db()
    elif args.cmd == 'data':
        _data_import(args.p)

if __name__ == '__main__':
    main()
