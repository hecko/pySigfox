#!/usr/bin/python

import os
import sys
from pprint import pprint

import PySigfox.PySigfox as SF

login = os.getenv('SIGFOX_API_LOGIN')
password = os.getenv('SIGFOX_API_PASSWORD')

s = SF.PySigfox(login, password)

try:
    s.login_test()
    print("API login OK")
except Exception as e:
    print(str(e))
    sys.exit(1)

for device_type_id in s.device_types_list():
    pprint(s.device_list(device_type_id))

pprint(s.device_list())
