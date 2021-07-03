import openpyxl 
from core.model import Model 



class ExportExcel: 

    def __init__(self):
        self.db = Model() 
        self.book = openpyxl.Workbook()
        self.sheet = self.book.active
    
    def export_emails(self, path): 
        
        rows = self.db.select('SELECT * FROM emails')
        for row, row_val in enumerate(rows): 
            for column, column_val in enumerate(row_val): 
                self.sheet.cell(row+1, column+1).value = column_val
        
        self.book.save(path)

