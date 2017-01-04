#!/usr/bin/python

import os
import sys
import json
import requests
from pprint import pprint

class Sigfox:
    def __init__(self, login, password):
        if not login or not password:
            raise Exception("Please define login and password when initiating pySigfox class!")
        self.login    = login
        self.password = password
        self.api_url  = 'https://backend.sigfox.com/api/'

    def login_test(self):
        """Try to login into the  Sigfox backend API - if unauthorized or any other issue raise Exception

        """
        url = self.api_url + 'devicetypes'
        r = requests.get(url, auth=requests.auth.HTTPBasicAuth(self.login, self.password))
        if r.status_code != 200:
            raise Exception("Unable to login to Sigfox API: " + str(r.status_code))

    def device_types_list(self):
        """Return list of device types IDs

        """
        out = []
        url = self.api_url + 'devicetypes'
        r = requests.get(url, auth=requests.auth.HTTPBasicAuth(self.login, self.password))
        for device in json.loads(r.text)['data']:
            out.append(device['id'])
        return out

    def device_list(self, device_type_id = 0):
        """Return array of dictionaries - one array item per device.

        :param device_type_id: Return only devices of a certain type ID.
            If set to 0 returns all devices of all types (default)! 
        :type device_type_id: int
        :return: List of dictionaries 
        :rtype: list

        """
        device_type_ids = []
        out = []
        if device_type_id != 0:
            device_type_ids.append(device_type_id)
        else:
            device_type_ids = self.device_types_list()

        for device_type_id in device_type_ids:
            # print("Getting data for device type id " + device_type_id)
            url = self.api_url + 'devicetypes/' + device_type_id + '/devices'
            r = requests.get(url, auth=requests.auth.HTTPBasicAuth(self.login, self.password))
            out.extend(json.loads(r.text)['data'])
        return out

    def device_messages(self, device_id, limit=10):
        """Return array of 10 last messages from specific device.
           
        :param device_id: ID of the device
        :type device_id: str
        :param limit: how many messages to retrieve - max limit 100
        :type limit: int

        """

        url = self.api_url + 'devices/' + str(device_id) + '/messages?limit=' + str(limit)
        r = requests.get(url, auth=requests.auth.HTTPBasicAuth(self.login, self.password))

        try:
            out = json.loads(r.text)['data']
        except Exception as e:
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
