from os import remove
import queue
from sys import flags
from time import sleep, thread_time
from PyQt5.uic.properties import float_list
from libray.parsing_email import ParsingEmail 
from libray.parsing_site import ParsingSite
from threading import Thread
from model.models import ModelSite, ModelEmail
import math
from multiprocessing import Queue

class ControllerColectingSites: 

    def __init__(self, phrazes):

        self.phrazes = phrazes
        self.save_site = [] 
        self.count_site = 0
        self.parsng_site = ParsingSite()
        self.finished = False 

    def set_phrazes(self, phrazes):
        self.phrazes = phrazes  

    def start(self): 
        trhead_syncing_data = Thread(target=self.syncing_data, args=())
        trhead_syncing_data.start() 

        trhead_site = Thread(target=self.parsing_extdition, args=())
        trhead_site.start() 

    def syncing_data(self): 
        while self.finished == False:

            if len(self.parsng_site.mas_sites) > 0: 
                data = self.parsng_site.mas_sites 
                self.save_site += data 
                self.count_site += len(data)
                self.parsng_site.mas_sites = [] 



    def parsing_extdition(self): 
        try: 
            if len(self.phrazes) > 0: 
                for phraze in self.phrazes: 
                    print(phraze)
                    if self.finished == False: 
                        self.parsng_site.sbor(phraze)
                self.phrazes = [] 
                self.finished = True 

        except: 
            self.finished = True 
      

class ControllerColectingEmails:
    
        
    def __init__(self):

        #сайты в очереди
        self.site = [] 

        #очередь
        self.queue = Queue() 
        self.emails = [] 

        self.parsing_email = ParsingEmail
        self.finished = False 
        self.work = False

        self.counts = 0
        self.count_sites = 0

    def create_queue(self, site): 
        self.site = site 
        for s in self.site: 
            self.queue.put(s)

    def hadler_queue(self): 
        while self.finished == False: 
             
            if self.queue.qsize() > 0: 
                trheads = [] 
                for i in range(0, 10): 
                    trhead = Thread(target = self.collection, args=(self.queue.get()['url'], ))
                    trhead.start() 
                    trheads.append(trhead)
                
                for t in trheads: 
                    t.join()
                

                       
    def collection(self, site):
        self.work = True 
        email = self.parsing_email(site).start()
        self.emails += email
        self.count(len(email))
        self.count_site(1)
        if email != []:     
            print(email)
        self.work = False

        


    def count(self, count): 
        self.counts += count

    def count_site(self, count): 
        self.count_sites += count
        
    def start(self): 
         
        trhead_emails = Thread(target=self.hadler_queue)
        trhead_emails.start() 

