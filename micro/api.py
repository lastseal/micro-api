# -*- coding: utf-8 -*

from micro import config

import requests
import socketio
import logging
import time
import os

API_URL = os.getenv("API_URL")
API_TOKEN = os.getenv("API_TOKEN")

##
#

class Client:

    def __init__(self, url=API_URL, token=API_TOKEN, timeout=None, retries=3):
        self.url = url
        self.timeout = timeout
        self.sios = {}
        self.retries = retries

        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {token}"})

    def retry(func):
        def wrapper(self, *args, **kwargs):
            retries = 0
            while retries <= self.retries:
                try:
                    return func(self, *args, **kwargs)
                except Exception as ex:
                    retries += 1
                    logging.warning("retry: %d, ex: %s", retries, ex)
                    time.sleep(1)
                    if retries > self.retries:
                        raise ex
        return wrapper

    @retry
    def get(self, uri, params=None):
        
        url = f"{self.url}{uri}"

        logging.debug("GET url: %s, params: %s", url, params)
        
        res = self.session.get(url, params=params, timeout=self.timeout)

        if res.status_code >= 400:
            raise Exception({
                "status": res.status_code, 
                "message": res.text
            })
        
        return res.json()

    @retry
    def post(self, uri, data=None, files=None):

        url = f"{self.url}{uri}"

        logging.debug("POST url: %s, json: %s, files: %s", url, data, files)
        
        res = self.session.post(url, json=data, files=files, timeout=self.timeout)

        if res.status_code >= 400:
            raise Exception({
                "status": res.status_code, 
                "message": res.text
            })
        
        return res.json()

    @retry
    def put(self, uri, data):

        url = f"{self.url}{uri}"

        logging.debug("PUT url: %s, json: %s", url, data)
        
        res = self.session.put(url, json=data, timeout=self.timeout)

        if res.status_code >= 400:
            raise Exception({
                "status": res.status_code, 
                "message": res.text
            })
        
        return res.json()

    @retry
    def delete(self, uri, data):

        url = f"{self.url}{uri}"

        logging.debug("DELETE url: %s, json: %s", url, data)
        
        res = self.session.delete(url, timeout=self.timeout)

        if res.status_code >= 400:
            raise Exception({
                "status": res.status_code, 
                "message": res.text
            })
        
        return res.json()
    
    def subscribe(self, name, criteria={}, event="POST"):

        logging.debug("WS url: %s, criteria: %s", self.url, criteria)

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

