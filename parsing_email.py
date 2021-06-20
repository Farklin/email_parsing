from abc import abstractproperty
from typing import ClassVar
import requests
from bs4 import BeautifulSoup 
import re
from urllib.parse import urlparse 
from requests import api
import time 
import signal


#сбор на старнице с укзааным url 
class ParsingEmail: 

    def __init__(self, url):

        self.mas_email = []
        self.result_email = []

        self.url = url

    def start(self): 
    
        try:
            r = requests.get(self.url, timeout=(3.05, 15)) 
            
            bs = BeautifulSoup(r.content, 'html.parser')
    
            if re.findall('([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)', r.text) :
                self.mas_email = re.findall('([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)', r.text) 
                self.mas_email = set(self.mas_email) 
            
            

            for email in self.mas_email: 
                hostname = urlparse(self.url).hostname
                self.result_email.append({'email':email, 'source': self.url, 'domain': hostname })

            r.close() 
            return self.result_email


        except Exception as e: 
            print(e)


