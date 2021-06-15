from re import S
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from bs4 import BeautifulSoup as BS
from selenium.webdriver.chrome.options import Options
from webdriver_manager import driver
from webdriver_manager.chrome import ChromeDriverManager
import time 
import urllib
from selenium.webdriver.common.keys import Keys
import os
import datetime 
from tqdm import tqdm
import openpyxl


class ParsingSites: 


    def __init__(self): 
        self.mas_sites = [] 
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.mas_position = [] 
        self.driver.minimize_window() 


    #сбор сайтов по всем фразам 10 страниц 
    def sbor(self, phraze):
        self.mas_sites = [] 
        for page in range(0, 15): 
            self.sbor_page(phraze, page)
       
        return self.mas_sites 


    #сбор страницы сайтов органической выдачи 
    def sbor_page(self, phraze, page): 

        self.driver.get('https://yandex.ru/search/?text='+str(phraze)+'&lr=213&p='+str(page))
                
        time.sleep(3)
        bs = BeautifulSoup( self.driver.page_source, 'html.parser') 

        for val, vidacha in enumerate(bs.select('.Organic>.OrganicTitle>.Link ')): 
            today = datetime.datetime.today()
            date = today.strftime("%Y-%m-%d-%H.%M.%S")

            data_elem = dict()
            data_elem['url'] = vidacha.get('href')
            data_elem['status'] = 'start'
            data_elem['date'] = date 
            self.mas_sites.append(data_elem)


                         

