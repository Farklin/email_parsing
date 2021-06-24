from os import remove
from time import sleep
from PyQt5.uic.properties import float_list
from libray.parsing_email import ParsingEmail 
from libray.parsing_site import ParsingSite
from threading import Thread
from model.models import ModelSite, ModelEmail
import math


class ControllerColectingSites: 

    def __init__(self, phrazes):

        self.phrazes = phrazes
        self.save_site = [] 

        self.parsng_site = ParsingSite
        self.finished = False 

    def set_phrazes(self, phrazes):
        self.data_phrazes = phrazes  

    def start(self): 

        trhead_site = Thread(target=self.parsing_extdition)
        trhead_site.start() 

    def parsing_extdition(self): 
        try: 
            if len(self.phrazes) > 0: 
                for phraze in self.phrazes: 
                    if self.finished == False: 
                        data = self.parsng_site().sbor(phraze)
                        self.save_site += data
                self.finished = False 
        except: 
            self.finished = True 
      
    def save(self): 
        pass 

class ControllerColectingEmails:
        
    def __init__(self):

        self.site_queue = [] 
        self.site_update = [] 

        self.save_emails = []  

        self.finished = False 

        self.parsing_email = ParsingEmail

    def parsing_emails(self): 

        def func_chunks_num(lst, c_num):
            n = math.ceil(len(lst) / c_num)

            for x in range(0, len(lst), n):
                e_c = lst[x : n + x]

                if len(e_c) < n:
                    e_c = e_c + [None for y in range(n - len(e_c))]
                yield e_c


        while self.finished==False: 
            
            if len(self.site_queue) > 0: 
                theads = [] 
                for stack_sites in func_chunks_num(self.site_queue, 4): 
                    thead = Thread(target = self.parsing_email_thead, args=(stack_sites, ))
                    thead.start()
                    theads.append(thead)

                for thead in theads: 
                    thead.join() 

            else: 
                self.parsng_email_status = False

    def parsing_email_thead(self, stack_sites):
        for site in stack_sites: 
            self.save_emails += self.parsing_email(site).start()
            self.site_queue.remove(site)
            self.site_update.append(site['url'])
       
    def start(self): 
        trhead_emails = Thread(target=self.parsing_emails)
        trhead_emails.start() 

class QueueEmail: 

    def __init__(self, emails_save = []) -> None:


        ''' класс потка очереди для обработки данных email в базе данных 

        параметры 
        emails_save - хранит данные для записи в базу данных 
    
        ''' 

        self.emails_save = emails_save 
        self.finished = False

    def save_database(self):

        '''принимает массив формата elem словаря со значениями email, source, domain для записи в базу данных '''
        while self.finished == False: 
            for email in self.emails_save: 
                ModelEmail().write(email['email'], email['source'], email['domain'], '22.06.2021')
                self.emails_save.remove(email)
        
    def start(self):
    
        thead_save = Thread(target=self.save_database) 
        thead_save.start()
                
class QueueSite: 
    
    def __init__(self) -> None:
        
        ''' класс потка очереди для обработки site в базе данных 

            параметры 
            site_save - хранит данные для записи в базу данных 
            site_update - хранит данные для обновление статуса в базе данных
            site_queue - хранит данные очереди сайты чей статус является start 
        
         ''' 

        self.site_save = []
        self.site_update = []
        self.site_queue = []
        self.finished = False

    def save_database(self):

        '''принимает массив формата elem словаря со значениями url, status, date для записи в базу данных '''
        while self.finished == False: 
            if len(self.site_save) > 0: 
                for site in self.site_save: 
                    ModelSite().write(site['url'], site['status'], site['date'])
                    self.site_save.remove(site)
    
    def update_status(self):
        '''принимает одномерный массив списко url адресов для изменение статуса на finished'''

        while self.finished == False: 
            if len(self.site_update) != 0: 
                for site in self.site_update: 
                    ModelSite().query("UPDATE sites SET status='finished' WHERE url = '" +site+ "'")
                    self.site_update.remove(site)

    def queue(self): 
        ''' формирует очередь на обработку ''' 
        while self.finished == False: 
            self.site_queue = ModelSite().select('SELECT * FROM sites WHERE status = "start" ')

    def start(self):
        while self.finished == False: 
            self.save_database() 
            self.update_status() 
            self.queue() 


class ControllerColecting: 
    
    def __init__(self, phraze) -> None:

        self.ColectingSites = ControllerColectingSites(phraze)
        self.ColectingEmails = ControllerColectingEmails

        self.QueueEmail = QueueEmail() 
        self.QueueSite = QueueSite() 

        self.finished = False
        
    def exchange(self):
        while self.finished == False: 
            self.QueueSite.site_save = self.ColectingSites.save_site
             
    def stop(self): 
        self.QueueEmail.finished = True 
        self.QueueSite.finished = True 

        self.ColectingSites.finished = True 
        self.ColectingEmails.finished = True 
        
        self.finished = True 



    def start(self):
        # thead_QueueColectingSites =  Thread(target = self.ColectingSites.parsing_extdition, args = ())
        # thead_QueueColectingSites.start() 

        # thead_QueueSite = Thread(target = self.QueueSite.start, args = ()) 
        # thead_QueueSite.start() 
        
        # thead_exchange = Thread(target=self.exchange)
        # thead_exchange.start() 
        print(self.ColectingSites.phrazes)
        self.ColectingSites.parsing_extdition() 

        






