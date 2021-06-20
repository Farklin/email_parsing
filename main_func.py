from soupsieve import select
from parsing_email import ParsingEmail 
from parsing_sites import ParsingSites 
from data_base import DataBase 

from threading import Thread
import math 
from tqdm import tqdm
import time 
# db = DataBase('mydatabase.db')
# db.create_base_email()
# db.create_base_sites() 




# def sbor(phraze): 

#     for site in tqdm(ParsingSites().sbor(phraze)): 
#         if len(db.select('select * From sites WHERE url="' +site['url']+ '"')) < 1:
#             db.create_sites(site['url'], site['status'], '16.06.2021')
#             if ParsingEmail(site['url']).start(): 
#                 for email in ParsingEmail(site['url']).start(): 
#                     db.create_email(email['email'], email['source'], site['url'], '16.06.2021')


# for phraze in phrazes: 
#     thead = Thread(target = sbor, args=(phraze, ))
#     thead.start()
#     time.sleep(4 * 10)

# for rows in db.select('select * From email'): 
#     print(rows[0])      

class MainF: 

    def __init__(self): 
        self.phrazes = [] 
        self.finished = False 
        self.db = DataBase('mydatabase.db') 

    def get_prazhes(self, phrazes):
        self.phrazes = phrazes 
     
    def parsing_extradition(self): 
        
        for phraze in self.phrazes: 

            #завершение программы
            if self.finished == True: 
                    break 
                    

            for site in tqdm(ParsingSites().sbor(phraze)): 
                if len(self.db.select('select * From sites WHERE url="' +site['url']+ '"')) < 1:
                    self.db.create_sites(site['url'], site['status'], '16.06.2021')

                #завершение программы
                if self.finished == True: 
                    break 
        
        self.finished = True 


    def parsing_emails(self):

        while self.finished == False: 
            #разбиение массива на n частей 
            def func_chunks_num(lst, c_num):
                n = math.ceil(len(lst) / c_num)

                for x in range(0, len(lst), n):
                    e_c = lst[x : n + x]

                    if len(e_c) < n:
                        e_c = e_c + [None for y in range(n - len(e_c))]
                    yield e_c

            sites = self.db.select('Select * From sites where status ="start"') 
            theads = [] 

            if len(sites) > 0: 
                for stack_sites in func_chunks_num(sites, 4): 
                    thead = Thread(target = self.parsing_stack_emails, args=(stack_sites, ))
                    thead.start()
                    theads.append(thead)
                
                for thead in theads: 
                    thead.join() 

    def parsing_all(self):
        if(len(self.phrazes)) > 0: 
            thead_parsing_extradition = Thread(target = self.parsing_extradition) 
            thead_parsing_extradition.start()
            thead_parsing_eamils = Thread(target = self.parsing_emails) 
            thead_parsing_eamils.start() 
            

    def parsing_stack_emails(self, sites): 
        for site in sites: 
            if ParsingEmail(site[0]).start(): 
                for email in ParsingEmail(site[0]).start(): 
                    self.db.create_email(email['email'], email['source'], site[0], '16.06.2021')

            self.db.sql_command('UPDATE sites set status = "finished" where url = "' +site[0]+ '"')
        
                        

# phrazes = ['детский интернет магазин', 
# 'магазин продуктов', 
# 'магазин техники', 
# 'ювелирный магазин', 
# 'магазин косметики', 
# 'магазин запчастей', 
# 'часы магазин', 
# 'онлайн магазины', 
# 'спортивный магазин', 
# 'магазин игрушек', ]


# main = Main()
# main.get_prazhes(phrazes)
# main.parsing_extradition()
