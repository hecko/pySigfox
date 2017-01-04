#!/usr/bin/python

import os
import sys
from pprint import pprint

import pySigfox

login = os.getenv('SIGFOX_LOGIN')
password = os.getenv('SIGFOX_PASSWORD')

s = pySigfox.Sigfox(login, password)

try:
    s.login_test()
    print("API login OK")
except Exception as e:
    print(str(e))
    sys.exit(1)


print("Getting list of all devices:")
for device_type_id in s.device_types_list():
    for device in s.device_list(device_type_id):
        pprint(device)
        last_device = device

print("== Messages for " + last_device['name'] + ":")
messages = s.device_messages(last_device['id'])
pprint(messages)
print("Number of messages: " + str(len(messages)))
