#!/usr/bin/env python
import requests
import json
import pgpy
import time

VERSION = 0.1

class Pace2PaceMasterRequest():
    ''' handles the creation of Pace2Pace request from master key provider
    '''
    def __init__(self, action: str, data: dict, timestamp: int = None, version: float =VERSION):
        ''' Builds a Pace2Pace request object
        :param action: gets any of the actions
        :param dict: gets a dict with action params
        :return: returns nothing
        '''
        self.action = action
        self.data = data
        if version > VERSION:
            raise NotImplementedError('Your installed version support only version %.2f and down' % VERSION) 
        self.version = version
        self.timestamp = int( time.time() ) if timestamp == None else timestamp

    def to_json(self):
        ''' Returns a json representation of the unsigned request'''
        return json.dumps({'Pace2Pace': {
            'version': self.version, 'action': self.action, 
            'data': self.data, 'timestamp': self.timestamp
        }})

    def send_to_master_via_file(self, file=None):
        '''Sends request to master
        :param file: is either filename or handler, required for file 
        '''
        with open(file, 'w') as f:
            f.write(self.to_json())

class NewUserRequest(Pace2PaceMasterRequest):
    def __init__(self, name: str, comment: str = '', timestamp: int = None, version: float = VERSION):
        Pace2PaceMasterRequest.__init__(self, 'new_user', {'Pace2Pace': {'name': name, 'comment': comment}})
