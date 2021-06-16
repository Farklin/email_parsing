from parsing_email import ParsingEmail 
from parsing_sites import ParsingSites 
from data_base import DataBase 

from threading import Thread


db = DataBase('mydatabase.db')


phrazes = [
    #'магазин одежды', 
    # 'магазин мебели', 
    # 'магазин одежды с доставкой', 
    # 'книжный магазин', 
    # 'магазин тканей', 
    # 'магазин бытовой', 
    # 'спортивный магазин', 
    # 'купить огнетушитель', 
    'огнетушитель оп купить', 
    # 'огнетушитель автомобильный купить', 
] 

search_email = ParsingEmail


def chunks(lst, chunk_size):
    return [lst[i:i+chunk_size] for i in range(0, len(lst), chunk_size)]


def stack_email(mas):
    for url in mas: 
        print(search_email(url).start()) 



# yandex = ParsingSites() 
# for phraze in phrazes: 
#     for site in yandex.sbor(phraze): 
#         db.create_sites(site['url'],site['status'], site['date'])


mas = [] 
for rows in db.select('Select * FROM sites'): 
    mas.append(rows[0])
    print(search_email(rows[0]).start()) 

for elem in chunks(mas, 10): 
    thead = Thread(stack_email, args = (elem, ))
    thead.start() 



      
            




