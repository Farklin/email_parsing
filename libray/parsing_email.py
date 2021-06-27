import requests
from bs4 import BeautifulSoup 
import re
from urllib.parse import urlparse 
import time 


#сбор на старнице с укзааным url 
class ParsingEmail: 

    def __init__(self, url):

        self.mas_email = []
        self.result_email = []

        self.url = url

    def start(self): 
    
        try:
            r = requests.get(self.url, timeout=10, headers={'User-agent': 'Mozilla/5.0'}) 
            
            if r: 
                bs = BeautifulSoup(r.content, 'html.parser')
        
                if re.findall('([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)', r.text) :
                    self.mas_email = re.findall('([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)', r.text) 
                    self.mas_email = set(self.mas_email) 
                
                

                for email in self.mas_email: 
                        if email.find('.png') == -1 and email.find('.webp') == -1    and email.find('.jpeg') == -1 and email.find('.jpg') == -1 and email.find('.gif') == -1: 
                            hostname = urlparse(self.url).hostname
                            self.result_email.append({'email':email, 
                                                    'source': self.url,
                                                    'domain': hostname })
                r.close() 
                return self.result_email
            else: 
                return [] 


        except Exception as e: 
            return []  

