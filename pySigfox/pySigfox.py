#!/usr/bin/python

import os
import sys
import json
import requests
from pprint import pprint

class Sigfox:
    def __init__(self, login, password, debug=False):
        if not login or not password:
            raise Exception("Please define login and password when initiating pySigfox class!")
        self.login    = login
        self.password = password
        self.api_url  = 'https://api.sigfox.com/v2/'
        self.debug = debug

    def login_test(self):
        """Try to login into the  Sigfox backend API - if unauthorized or any other issue raise Exception

        """
        url = self.api_url + 'device-types'
        r = requests.get(url, auth=requests.auth.HTTPBasicAuth(self.login, self.password))
        if r.status_code != 200:
            raise Exception("Unable to login to Sigfox API ({}): {}".format(url, r.status_code))

    def device_types_list(self):
        """Return list of device types dictionaries

        """
        out = []
        url = self.api_url + 'device-types'
        r = requests.get(url, auth=requests.auth.HTTPBasicAuth(self.login, self.password))
        for device in json.loads(r.text)['data']:
            out.append(device)
        return out

    def device_rename(self, device_id, new_name):
        """Rename specific device

        """
        out = []
        url = self.api_url + 'devices/' + str(device_id)
        if self.debug:
            print("Connecting to " + url)
        r = requests.put(url, auth=requests.auth.HTTPBasicAuth(self.login, self.password), json={'name': new_name})

    def device_info(self, device_id):
        """Return information about specific device

        """
        out = []
        url = self.api_url + 'devices/' + str(device_id)
        if self.debug:
            print("Connecting to " + url)
        r = requests.get(url, auth=requests.auth.HTTPBasicAuth(self.login, self.password))
        try:
            return json.loads(r.text)
        except Exception as e:
            pprint(r.text)
            raise

    def groups_list(self):
        """Return list of groups

        """
        out = []
        url = self.api_url + 'groups'
        if self.debug:
            print("Connecting to " + url)
        r = requests.get(url, auth=requests.auth.HTTPBasicAuth(self.login, self.password))
        if self.debug:
            pprint(r.text)
        for group in json.loads(r.text)['data']:
            out.append(group)
        return out

    def device_create(self, device, cert, devicetype):
        """Add new device to a device type

        """
        if self.debug:
            print("Adding device " + device['id'] + " to device type " + devicetype['name'])
        to_post = {
                    "prefix": "api_added-",
                    "ids": [
                             { 'id': device['id'], 'pac': device['pac'] },
                           ],
                    "productCertificate": str(cert), 
                  }
        url = self.api_url + "devicetypes/" + devicetype['id'] + '/devices/bulk/create/async'
        if self.debug:
            print("Connecting to " + url)
            print("Posting following data:")
            pprint(to_post)
        r = requests.post(url,
                          auth=requests.auth.HTTPBasicAuth(self.login, self.password),
                          json = to_post)
        if self.debug:
            pprint("Response: " + str(r.text))
        return r.json()

    def device_types_create(self, new):
        """Create new device type

        """
        dtype = {
                  'name': 'test1',
                  'contractId': 'moire_la_30f0_30f1'
                }
        url = self.api_url + 'devicetypes/create'
        if self.debug:
            print("Connecting to " + url)
        r = requests.post(url, auth=requests.auth.HTTPBasicAuth(self.login, self.password), data = dtype)
        return r

    def device_list(self, device_type):
        """Return array of dictionaries - one array item per device.

        :param device_type: Return only devices of a certain type.
            This is a object from device_groups_list()
        :return: List of dictionaries
        :rtype: list

        """
        device_type_ids = []
        out = []
        url = self.api_url + 'devices?deviceTypeId=' + device_type['id']
        r = requests.get(url, auth=requests.auth.HTTPBasicAuth(self.login, self.password))
        try:
            out.extend(json.loads(r.text)['data'])
        except Exception as e:
            print("Unable to access data from returned RESP API call: " + str(e))
            pprint(r.text)
            raise
        return out

    def device_messages(self, device, limit=10):
        """Return array of 10 last messages from specific device.

        :param device: Device object
        :param limit: how many messages to retrieve - max limit 100
        :type limit: int

        """

        url = self.api_url + 'devices/' + str(device['id']) + '/messages?limit=' + str(limit)
        r = requests.get(url, auth=requests.auth.HTTPBasicAuth(self.login, self.password))

        try:
            out = json.loads(r.text)['data']
        except Exception as e:
            pprint(r.text)
            raise

        return out

    def device_messages_page(self, url):
        """Return array of message from paging URL.

        """
        out = []
        r = requests.get(url, auth=requests.auth.HTTPBasicAuth(self.login, self.password))
        out.extend(json.loads(r.text)['data'])
        try:
            json.loads(r.text)['paging']['next']
            out.extend(self.device_messages_page(json.loads(r.text)['paging']['next']))
        except Exception as e:
            # no more pages
            pass

        return out
