import sqlite3
from sqlite3 import Error


conn = sqlite3.connect('mydatabase.db')

cursor = conn.cursor() 

cursor.execute("""CREATE TABLE email
                  (name text, source text, domain text,
                   date text)
               """)