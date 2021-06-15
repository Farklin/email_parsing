from parsing_email import ParsingEmail 
from parsing_sites import ParsingSites 
from data_base import DataBase 

from threading import Thread


db = DataBase('mydatabase.db')


phrazes = [
    'магазин одежды', 
    # 'магазин мебели', 
    # 'магазин одежды с доставкой', 
    # 'книжный магазин', 
    # 'магазин тканей', 
    # 'магазин бытовой', 
    # 'спортивный магазин', 
    # 'купить огнетушитель', 
    # 'огнетушитель оп купить', 
    # 'огнетушитель автомобильный купить', 
] 

search_email = ParsingEmail


def emails(urls ): 
    for url in urls: 
        for email in search_email(url).start(): 
            print(email.name)

def chunks(lst, chunk_size):
        return [lst[i:i+chunk_size] for i in range(0, len(lst), chunk_size)]





# yandex = ParsingSites() 
# for phraze in phrazes: 
#     for site in yandex.sbor(phraze): 
#         db.create_sites(site['url'],site['status'], site['date'])

for row in db.select('Select * FROM sites'): 
    for i in chunks(row, 10): 
        thead = Thread(target= 'emails', args = i )
        thead.start() 

      
            




