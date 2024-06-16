# -*- coding: utf-8 -*

import requests
import socketio
import os

API_URL = os.getenv("API_URL")
APi_TOKEN = os.getenv("APi_TOKEN")

##
#

class Client:

    def __init__(self, url=API_URL, token=APi_TOKEN, timeout=None, websocket=False):
        self.url = url
        self.timeout = timeout
        self.sio = None

        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {token}"})
        
        if websocket:
            self.sio = socketio.SimpleClient()
            self.sio.connect(self.url, transports=['websocket'])

    def get(self, uri, params=None):
        
        url = f"{self.url}{uri}"
        res = self.session.get(url, params=params, timeout=self.timeout)

        if res.status_code >= 400:
            raise Exception({
                "status": res.status_code, 
                "message": res.text
            })
        
        return res.json()
    
    def post(self, uri, data):

        url = f"{self.url}{uri}"
        res = self.session.post(url, json=data, timeout=self.timeout)

        if res.status_code >= 400:
            raise Exception({
                "status": res.status_code, 
                "message": res.text
            })
        
        return res.json()
    
    def put(self, uri, data):

        url = f"{self.url}{uri}"
        res = self.session.put(url, json=data, timeout=self.timeout)

        if res.status_code >= 400:
            raise Exception({
                "status": res.status_code, 
                "message": res.text
            })
        
        return res.json()
    
    def delete(self, uri, data):

        url = f"{self.url}{uri}"
        res = self.session.delete(url, timeout=self.timeout)

        if res.status_code >= 400:
            raise Exception({
                "status": res.status_code, 
                "message": res.text
            })
        
        return res.json()
    
    def subscribe(self, name, criteria={}, event="POST"):
        if self.sio is not None:
            self.sio.emit("subscribe", {
                "name": name,
                "event": event,
                "criteria": criteria
            })
        
        def decorator(handle):
            handle()

        return decorator

