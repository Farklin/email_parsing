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
            for page in range(0, 11): 
                self.sbor_page(phraze, page)
       
    #сбор страницы сайтов органической выдачи 
    def sbor_page(self, phraze, page): 

        self.driver.get('https://yandex.ru/search/?text='+phraze+'&lr=192&p='+str(page))
                
        time.sleep(3)
        bs = BeautifulSoup( self.driver.page_source, 'html.parser') 

        for val, vidacha in enumerate(bs.select('.Organic>.OrganicTitle>.Link ')) : 
            self.mas_sites.append(vidacha.get('href'))
                         
v = SborPosition([
    'дом керамики',
    'керамическая плитка во владимире', 
    'керамическая плитка во владимире купить', 
    'керамическая плитка во владимире для ванной', 
    'напольная керамическая плитка', 
    'керамическая плитка во владимире каталог и цены', 
    'керамическая плитка во владимире купить недорого', 
    'шахтинская керамическая плитка во владимире', 
    'керамическая плитка для ванной', 
    'плитка керамическая 20 х30 темно синяя владимире', 
    'магазины керамической плитки во владимире', 
    'купить керамическую плитку', 
    'плитка керамическая напольная цена', 
    'керамическая плитка г владимир', 
    'керамическая плитка под дерево', 
    'керамическая плитка для ванной купить', 
    'керамическая плитка для пола', 
    'выбор керамической плитки', 
    'керамическая плитка лапарет', 
    'бордюр для плитки керамической', 
    'купить керамическую плитку в ванную комнату', 
    'производители керамической плитки', 
    'интернет магазин керамической плитки', 
    'керамическая плитка под дерево на пол', 
])
v.sbor() 
