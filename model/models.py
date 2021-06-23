from core.model import Model 

class ModelEmail(Model): 

    def __init__(self, dbname='mydatabase.db'):
        super().__init__(dbname=dbname)
        self.create() 


    def create(self):
        try:
            self.cursor.execute("""CREATE TABLE emails(
                            name text,          
                            source text,
                            domain text,
                            date text)
                        """)
            self.conn.commit()
        except: 
            pass
    

    def write(self, name, source, domain, date): 
        if len(self.select('select * From emails where name="'+name+'"')) < 1: 
            try: 
                sql_insert = """INSERT INTO emails VALUES (?,?,?,?);"""
                data_email = (name, source, domain, date)
                self.cursor.execute(sql_insert, data_email)
                self.conn.commit()
            except: 
                pass

class ModelSite(Model): 
    def __init__(self, dbname='mydatabase.db'):
        super().__init__(dbname=dbname)
        self.create() 

    def create(self):
        try: 
            self.cursor.execute("""CREATE TABLE sites(
                                url text,          
                                status text,   
                                date text)
                            """)
            self.conn.commit()
        except: 
            pass
      
    def write(self, url, status, date): 
        if len(self.select('select * From sites where url="'+url+'"')) < 1: 
            try: 
                sql_insert = """INSERT INTO sites VALUES (?,?,?);"""
                data_email = (url, status, date)
                self.cursor.execute(sql_insert, data_email)
                self.conn.commit()
            except: 
                pass
