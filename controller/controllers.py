from os import remove
from time import sleep
from PyQt5.uic.properties import float_list
from libray.parsing_email import ParsingEmail 
from libray.parsing_site import ParsingSite
from threading import Thread
from model.models import ModelSite, ModelEmail
import math
class ControllerColectingSites: 

    def __init__(self):
        self.data_phrazes = [] 
        self.data_sites = [] 
        self.data_emails = []  
        self.queue_sites = [] 

        self.parsng_site = ParsingSite
        self.parsing_email = ParsingEmail 
        
        self.parsng_site_status = True
        self.parsng_email_status = True

        self.finished = False 

    def set_phrazes(self, phrazes):
        self.data_phrazes = phrazes  

    def start(self): 

        trhead_queue_sites = Thread(target=self.queue_save_sites)
        trhead_queue_sites.start()

        trhead_queue_emails= Thread(target=self.queue_save_emails)
        trhead_queue_emails.start()

        trhead_site = Thread(target=self.parsing_extdition)
        trhead_site.start() 
            
        trhead_emails = Thread(target=self.parsing_emails)
        trhead_emails.start() 

        trhead_queue_view = Thread(target=self.queue_view)
        trhead_queue_view.start() 
        
    def parsing_extdition(self): 
        if len(self.data_phrazes) > 0: 
            for phraze in self.data_phrazes: 
                if self.finished == False: 
                    data = self.parsng_site().sbor(phraze)
                    self.data_sites += data

        self.parsng_site_status = False 

        #если очередь пустая то процесс сбора sites завершен 
        
    def parsing_emails(self): 

        def func_chunks_num(lst, c_num):
            n = math.ceil(len(lst) / c_num)

            for x in range(0, len(lst), n):
                e_c = lst[x : n + x]

                if len(e_c) < n:
                    e_c = e_c + [None for y in range(n - len(e_c))]
                yield e_c


        while self.finished==False: 
            
            if len(self.queue_sites) > 0: 
                self.parsng_email_status = True
                theads = [] 
                for stack_sites in func_chunks_num(self.queue_sites, 4): 
                    thead = Thread(target = self.parsing_email_thead, args=(stack_sites, ))
                    thead.start()
                    theads.append(thead)

                for thead in theads: 
                    thead.join() 

            else: 
                self.parsng_email_status = False

    def parsing_email_thead(self, stack_sites):
        for site in stack_sites: 
            self.data_emails += self.parsing_email(site).start()
            self.queue_sites.remove(site) 


    #очередь на добавление в базу данных сайтов 
    def queue_save_sites(self): 
        while self.finished == False: 
            if len(self.data_sites) > 0: 
                for site in self.data_sites: 
                    ModelSite().write(site['url'], site['status'], site['date'])
                    self.data_sites.remove(site)
            
            rows = ModelSite().select('SELECT * FROM sites WHERE status = "start" ')
            if len(rows) > 0: 

                for row in rows: 
                    self.queue_sites.append(row[0]) 
                    ModelSite().query("UPDATE sites SET status='finished' WHERE url = '" +row[0] + "'") 

    def queue_save_emails(self): 
        while self.finished == False: 
            if len(self.data_emails) > 0: 
                for email in self.data_emails: 
                    ModelEmail().write(email['email'], email['source'], email['domain'], '22.06.2021')
                    self.data_emails.remove(email)

    def queue_view(self): 
        while self.finished == False: 
            sleep(10)
            print(len(self.queue_sites), self.parsng_email_status, self.parsng_site_status, self.finished ) 

            #если очереди пустые завершаем все действия 
            if self.parsng_email_status == False and self.parsng_site_status == False: 
                self.finished = True
            
            
    def save(self): 
        pass 

    
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

        for email in self.emails_save: 
            ModelEmail().write(email['email'], email['source'], email['domain'], '22.06.2021')
            self.emails_save.remove(email)
                
                
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

        if len(self.site_save) > 0: 
            for site in self.site_save: 
                ModelSite().write(site['url'], site['status'], site['date'])
                self.site_save.remove(site)
    
    def update_status(self):
        '''принимает одномерный массив списко url адресов для изменение статуса на finished'''


        for site in self.save_update: 
            ModelSite().query("UPDATE sites SET status='finished' WHERE url = '" +site+ "'")
            self.site_update.remove(site)

    def queue(self): 
        ''' формирует очередь на обработку ''' 
        self.site_queue = ModelSite().select('SELECT * FROM sites WHERE status = "start" ')

