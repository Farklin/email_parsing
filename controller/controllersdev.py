from os import remove
from time import sleep
from PyQt5.uic.properties import float_list
from libray.parsing_email import ParsingEmail 
from libray.parsing_site import ParsingSite
from threading import Thread
from model.models import ModelSite, ModelEmail
import math
from queue import Queue

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

        self.sites = [] 
        self.site_queue = Queue() 
        #статус очереди
        self.status_queue = True 


        self.save_emails = []  
        self.processed_site_count = 0 
        self.processed_email_count = 0

        self.finished = False 

        self.parsing_email = ParsingEmail

    def queue(self): 
        while self.finished == False: 
            # если очередь пустая ы
            if self.site_queue.empty() and len(self.sites) > 0: 

                for site in self.sites: 
                    self.site_queue.put(site)

                theards = [] 
                for site in range(0, self.site_queue.qsize()): 
                    for t_number in range(0, 10): 
                        
                        theard = Thread(target=self.sbor_email, args=(self.site_queue.get(), ))
                        theard.start()
                        theards.append(theard)

                
                for theard in theards: 
                    theard.join(15) 

                self.sites = [] 
                print('обработано сайтов' + str(self.processed_site_count))
                print('найдено контактов' + str(self.processed_email_count))
                    
    def sbor_email(self, site): 
        emails = self.parsing_email(site).start()
        self.save_emails += emails
        self.processed_email_count += len(emails) 
        self.processed_site_count += 1

        print(site)

        
    def start(self): 
        pass
        #trhead_emails = Thread(target=self.parsing_emails)
        #trhead_emails.start() 

