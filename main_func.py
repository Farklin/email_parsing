from soupsieve import select
from parsing_email import ParsingEmail 
from parsing_sites import ParsingSites 
from data_base import DataBase 
from export_excel import ExportExcel 
from threading import Thread
import math 
from tqdm import tqdm
import time 

class MainF: 

    def __init__(self): 
        self.phrazes = [] 
        self.finished = False 
        self.db = DataBase('mydatabase.db') 

    #Ввод фраз на парсинг 
    def get_prazhes(self, phrazes):
        self.phrazes = phrazes 
    #парсинг выдачи по фразам 
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

    #парсинг сайтов нахождение email адресов 
    def parsing_emails(self):

        #разбиение массива на n частей 
        def func_chunks_num(lst, c_num):
            n = math.ceil(len(lst) / c_num)

            for x in range(0, len(lst), n):
                e_c = lst[x : n + x]

                if len(e_c) < n:
                    e_c = e_c + [None for y in range(n - len(e_c))]
                yield e_c

       

        while self.finished == False: 
            
            sites = self.db.select('Select * From sites where status ="start"') 
            theads = [] 

            if len(sites) > 0: 
                for stack_sites in func_chunks_num(sites, 4): 
                    thead = Thread(target = self.parsing_stack_emails, args=(stack_sites, ))
                    thead.start()
                    theads.append(thead)
                
                for thead in theads: 
                    thead.join() 
        
    #парсин сайтов и email в 2 поточном режиме 
    def parsing_all(self):
        if(len(self.phrazes)) > 0: 
            thead_parsing_extradition = Thread(target = self.parsing_extradition) 
            thead_parsing_extradition.start()
            thead_parsing_eamils = Thread(target = self.parsing_emails) 
            thead_parsing_eamils.start() 
    
    #парсинг массива сайтов для поточного режима
    def parsing_stack_emails(self, sites): 
        for site in sites: 
            print(site[0])
            if ParsingEmail(site[0]).start(): 
                for email in ParsingEmail(site[0]).start(): 
                    self.db.create_email(email['email'], email['source'], site[0], '16.06.2021')

            self.db.sql_command('UPDATE sites set status = "finished" where url = "' +site[0]+ '"')

    def export_excle_email(self):
        ExportExcel(self.db).export_emails() 

                        

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
