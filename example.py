#!/usr/bin/python

import os
import sys
from pprint import pprint

sys.path.insert(0, os.path.abspath('./modules'))

import pySigfox

login = os.getenv('SIGFOX_LOGIN')
password = os.getenv('SIGFOX_PASSWORD')

s = pySigfox.Sigfox(login, password)

s.login_test()
print("API login OK")

print("Getting list of all devices:")
for device_type in s.device_types_list():
    for device in s.device_list(device_type):
        pprint(device)
        last_device = device

print("== Last 3 messages from " + last_device['name'] + ":")
pprint(s.device_messages(last_device, limit=3))
