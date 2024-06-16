# -*- coding: utf-8 -*

from micro import config

import requests
import socketio
import logging
import os

API_URL = os.getenv("API_URL")
API_TOKEN = os.getenv("API_TOKEN")

##
#

class Client:

    def __init__(self, url=API_URL, token=API_TOKEN, timeout=None):
        self.url = url
        self.timeout = timeout
        self.sios = {}

        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {token}"})
        
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

        sio = socketio.Client()
        sio.connect(self.url, transports=['websocket'])

        self.sios[name] = sio
                
        def decorator(handle):

            sio.emit("subscribe", {
                "name": name,
                "event": event,
                "criteria": criteria
            })
            
            @sio.on('message')
            def on_message(data):
                handle(data)

        return decorator

