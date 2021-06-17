from soupsieve import select
from parsing_email import ParsingEmail 
from parsing_sites import ParsingSites 
from data_base import DataBase 

from threading import Thread

from tqdm import tqdm
import time 
db = DataBase('mydatabase.db')
db.create_base_email()
db.create_base_sites() 

phrazes = ['детский интернет магазин', 
'магазин продуктов', 
'магазин техники', 
'ювелирный магазин', 
'магазин косметики', 
'магазин запчастей', 
'часы магазин', 
'онлайн магазины', 
'спортивный магазин', 
'магазин игрушек', ]


def sbor(phraze): 

    for site in tqdm(ParsingSites().sbor(phraze)): 
        if len(db.select('select * From sites WHERE url="' +site['url']+ '"')) < 1:
            db.create_sites(site['url'], site['status'], '16.06.2021')
            if ParsingEmail(site['url']).start(): 
                for email in ParsingEmail(site['url']).start(): 
                    db.create_email(email['email'], email['source'], site['url'], '16.06.2021')


for phraze in phrazes: 
    thead = Thread(target = sbor, args=(phraze, ))
    thead.start()
    time.sleep(4 * 10)

for rows in db.select('select * From email'): 
    print(rows[0])      






