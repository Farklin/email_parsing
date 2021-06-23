import sqlite3
from sqlite3 import Error


class Model: 

    def __init__(self, dbname='mydatabase.db'):
        self.dbname = dbname
        self.check_createbase() 


    def check_createbase(self): 
        try:
            self.conn = sqlite3.connect(self.dbname, check_same_thread=False)
            self.cursor = self.conn.cursor() 
        except: 
            pass
    
    def select(self, sql): 
        self.cursor.execute(sql)
        row = self.cursor.fetchall()
        return row

    def query(self, sql):
        self.cursor.execute(sql)
        self.conn.commit()