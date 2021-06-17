from abc import abstractproperty
from typing import ClassVar
import requests
from bs4 import BeautifulSoup 
import re

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
    
            if re.findall('\w+@\w+.\w+', str(bs.select('body')[0].text)) :
                self.mas_email = re.findall('\w+@\w+.\w+', str(bs.select('body')[0].text)) 
                self.mas_email = set(self.mas_email) 
            
            

            for email in self.mas_email: 
                self.result_email.append({'email':email, 'source': self.url, 'domain': self.url})

            r.close() 
            print(self.result_email)
            return self.result_email
        except Exception as e: 
            pass 


