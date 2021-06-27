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
        self.count_site = 0
        self.parsng_site = ParsingSite
        self.finished = False 

    def set_phrazes(self, phrazes):
        self.phrazes = phrazes  

    def start(self): 

        trhead_site = Thread(target=self.parsing_extdition, args=())
        trhead_site.start() 

    def parsing_extdition(self): 
        try: 
            if len(self.phrazes) > 0: 
                for phraze in self.phrazes: 
                    if self.finished == False: 
                        data = self.parsng_site().sbor(phraze)
                        self.save_site += data
                        self.count_site += len(data)
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
        self.processed_site_count = 0 
        self.processed_email_count = 0 
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
                for stack_sites in func_chunks_num(self.site_queue, 5): 
                    thead = Thread(target = self.parsing_email_thead, args=(stack_sites, ))
                    thead.start()
                    theads.append(thead)

                for thead in theads: 
                    thead.join() 

            else: 
                self.parsng_email_status = False

    def parsing_email_thead(self, stack_sites):
        for site in stack_sites: 
            try: 
                self.site_queue.remove(site)
                self.save_emails += self.parsing_email(site[0]).start()
               
                print(site)
                self.site_update.append(site[0])
               
                self.processed_site_count += 1
                self.processed_email_count += len(self.save_emails)
               
            except: 
                pass 
       
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
        thead_save_database = Thread(target=self.save_database)
        thead_update_status = Thread(target=self.update_status)
        thead_queue = Thread(target=self.queue)

        thead_update_status.start() 
        thead_save_database.start() 
        thead_queue.start() 

class ControllerColecting: 
    
    def __init__(self, phraze) -> None:
        
        self.phraze = phraze
        self.ColectingSites = ControllerColectingSites(self.phraze)
        self.ColectingEmails = ControllerColectingEmails() 

        self.QueueEmail = QueueEmail() 
        self.QueueSite = QueueSite() 

        self.finished = False
        
    def exchange(self):
        while self.finished == False: 
            
            print(len(self.ColectingEmails.site_update))

            self.QueueSite.site_update += self.ColectingEmails.site_update
            

            if (len(self.ColectingEmails.site_queue) == 0): 
                self.ColectingEmails.site_queue = self.QueueSite.site_queue
                self.QueueSite.site_queue = [] 

            if len(self.ColectingSites.save_site) != 0: 
                self.QueueSite.site_save += self.ColectingSites.save_site
                self.ColectingSites.save_site = []
            
            if len(self.QueueEmail.emails_save) == 0: 
                self.QueueEmail.emails_save += self.ColectingEmails.save_emails
                self.ColectingEmails.save_emails = [] 

            sleep(10)

        
    def stop(self): 
        self.QueueEmail.finished = True 
        self.QueueSite.finished = True 

        self.ColectingSites.finished = True 
        self.ColectingEmails.finished = True 
        
        self.finished = True 



    def start(self):
                
        self.ColectingSites.set_phrazes(self.phraze)
        self.ColectingSites.start() 
        self.ColectingEmails.start()

        self.QueueSite.start()
        self.QueueEmail.start() 
        
        thead_exchange = Thread(target=self.exchange)
        thead_exchange.start() 

        


class DevControllerColecting: 
    
    def __init__(self, phraze) -> None:
        
        #фразы для сбора сайтов 
        self.phraze = phraze

        self.ColectingSites = ControllerColectingSites(self.phraze)
        self.ColectingEmails = ControllerColectingEmails() 

        self.QueueEmail = QueueEmail() 
        self.QueueSite = QueueSite() 

        self.finished = False
        
    def exchange(self):
        while self.finished == False: 
            
            print(len(self.ColectingEmails.site_update))

            self.QueueSite.site_update += self.ColectingEmails.site_update
            

            if (len(self.ColectingEmails.site_queue) == 0): 
                self.ColectingEmails.site_queue = self.QueueSite.site_queue
                self.QueueSite.site_queue = [] 

            if len(self.ColectingSites.save_site) != 0: 
                self.QueueSite.site_save += self.ColectingSites.save_site
                self.ColectingSites.save_site = []
            
            if len(self.QueueEmail.emails_save) == 0: 
                self.QueueEmail.emails_save += self.ColectingEmails.save_emails
                self.ColectingEmails.save_emails = [] 

            sleep(10)

        
    def stop(self): 
        self.QueueEmail.finished = True 
        self.QueueSite.finished = True 

        self.ColectingSites.finished = True 
        self.ColectingEmails.finished = True 
        
        self.finished = True 



    def start(self):
                
        self.ColectingSites.set_phrazes(self.phraze)
        self.ColectingSites.start() 
        self.ColectingEmails.start()

        self.QueueSite.start()
        self.QueueEmail.start() 
        
        thead_exchange = Thread(target=self.exchange)
        thead_exchange.start() 

        










