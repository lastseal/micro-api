# -*- coding: utf-8 -*

import os

API_URL = os.getenv("API_URL")
APi_TOKEN = os.getenv("APi_TOKEN")

##
#

class Client:

    def __init__(self, url=API_URL, token=APi_TOKEN):
        self.url = url
        self.token = token
