import openpyxl 

class ExportExcel: 

    def __init__(self, db, ) -> None:
        self.db = db 
        self.book = openpyxl.Workbook()
        self.sheet = self.book.active
    
    def export_emails(self): 
        
        rows = self.db.select('SELECT * FROM email')
        for row, row_val in enumerate(rows): 
            for column, column_val in enumerate(row_val): 
                self.sheet.cell(row+1, column+1).value = column_val
        
        self.book.save('export.xlsx')

