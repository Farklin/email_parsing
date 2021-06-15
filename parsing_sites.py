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


class SborPosition: 


    def __init__(self, mas_phraze): 
        self.mas_sites = [] 
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.mas_position = [] 
        self.mas_phraze = mas_phraze 
        self.driver.minimize_window() 


    #сбор сайтов по всем фразам 10 страниц 
    def sbor(self):
        
        for val, phraze in tqdm(enumerate(self.mas_phraze)):  
            for page in range(0, 15): 
                self.sbor_page(phraze, page)
       
    #сбор страницы сайтов органической выдачи 
    def sbor_page(self, phraze, page): 

        self.driver.get('https://yandex.ru/search/?text='+phraze+'&lr=213&p='+str(page))
                
        time.sleep(3)
        bs = BeautifulSoup( self.driver.page_source, 'html.parser') 

        for val, vidacha in enumerate(bs.select('.Organic>.OrganicTitle>.Link ')) : 
            self.mas_sites.append(vidacha.get('href'))
                         
v = SborPosition([
    'магазин одежды',
    'магазин мебели',
    'магазин одежды с доставкой',
    'книжный магазин',
    'магазин тканей',
    'магазин бытовой
    'спортивный магазин',
    'магазин джинсов',
    'магазин игрушек',
    'большой интернет магазин',
    'магазин детской одежды',
    'ремонт телефонов',
    'ремонт автомобилей',
    'ремонт стиральных',
    'ремонт ключей',
    'ремонт двигателя',
    'мебельная фурнитура',
    'купить фурнитуру',
    'фурнитура для бижутерии',
    'фурнитура для сумок',
    'купить сумку женскую',
    'магазин сумок купить',
    'купить огнетушитель',
    'огнетушитель оп купить',
    'огнетушитель автомобильный купить',
])
v.sbor() 
