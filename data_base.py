import sqlite3
from sqlite3 import Error




class DataBase:

    def __init__(self, dbname='mydatabase.db'): 
        self.dbname = dbname
        self.check_reatebase() 
         

    def check_reatebase(self): 
        try:
            self.conn = sqlite3.connect(self.dbname, check_same_thread=False)
            self.cursor = self.conn.cursor() 
        except: 
            pass
            #print('База данных не создана')
        
    def create_base_email(self):
        try: 
            self.cursor.execute("""CREATE TABLE email(
                            name text,          
                            source text,
                            domain text,
                            date text)
                        """)
            self.conn.commit()
        except: 
            print('база данных Email уже создана')
            return False 
             
    def create_base_sites(self):
        try: 
            self.cursor.execute("""CREATE TABLE sites(
                            url text,          
                            status text,   
                            date text)
                        """)
            self.conn.commit()
        except: 
            #print('база данных Sites уже создана')
            return False 

    def create_email(self, name, source, domain, date): 

        if len(self.select('select * From email where name="'+name+'"')) < 1: 
                
            try:
                sql_insert = """INSERT INTO email VALUES (?,?,?,?);"""
                data_email = (name, source, domain, date)
                self.cursor.execute(sql_insert, data_email)
                self.conn.commit()
            except sqlite3.Error as error:
                pass
                #print("Ошибка при работе с SQLite", error)
            
    def create_sites(self, url, status, date): 
        try:
            sql_insert = """INSERT INTO sites VALUES (?,?,?);"""
            data_email = (url, status, date)
            self.cursor.execute(sql_insert, data_email)
            self.conn.commit()
        except sqlite3.Error as error:
            pass
            #print("Ошибка при работе с SQLite", error)

    def select(self, sql): 
        self.cursor.execute(sql)
        row = self.cursor.fetchall()
        return row

    def sql_command(self, sql):
        self.cursor.execute(sql)
        row = self.cursor.fetchall()


#DataBase('mydatabase.db').create_email('ivanhel@yandex.ru', 'первосоздатель', 'rost-seo', '15.06.2021')
#DataBase('mydatabase.db').create_base_sites() 
#DataBase('mydatabase.db').create_sites('rost-seo.ru', 'finished', '15.06.2021')