from abc import abstractproperty
from typing import ClassVar
import requests
from bs4 import BeautifulSoup 
import re

from requests import api



#Объект Email 
class Email: 

    def __init__(self, name, source, domain):
        self.name =  name 
        self.source = source
        self.domain = domain 

#сбор на старнице с укзааным url 
class ParsingEmail: 

    def __init__(self, url):

        self.mas_email = []
        self.result_email = []

        self.url = url

    def start(self): 
        r = requests.get(self.url) 

        bs = BeautifulSoup(r.content, 'html.parser')

        if re.findall('.*?@', str(r.content)) :
            self.mas_email = re.findall('\w+@\w+.\w+', str(r.content)) 
            self.mas_email = set(self.mas_email) 
            

        for email in self.mas_email: 
            self.result_email.append(Email(email, self.url, self.url))

        return self.result_email


print(ParsingEmail('https://www.karcher.ru/ru/servis/professional/servis_proftehniki_karcher.html').start()) 