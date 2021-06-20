from PyQt5 import uic, QtWidgets 
from main_func import MainF 
from data_base import DataBase 


Form, _ = uic.loadUiType("untitled.ui")


class Ui(QtWidgets.QMainWindow, Form): 
    def __init__(self):
        super(Ui, self).__init__() 
        self.setupUi(self)

        self.main_function = MainF() 

        self.fill_table() 
        self.btn_start.clicked.connect(self.start)
        self.btn_refresh.clicked.connect(self.refresh_table)
        self.btn_next.clicked.connect(self.next_parsing_emails)
        self.btn_export.clicked.connect(self.main_function.export_excle_email)


    def start(self): 

        self.set_phrazes() 
        self.main_function.finished = False 
        self.main_function.parsing_all()


    #статусы кнопок
    def status_btn(self):
        sites = self.db.select("SELECT * FROM sites where status='start'")
        if len(sites) > 0: 
            self.btn_next.setEnabled(True)
        else: 
            self.btn_next.setEnabled(False)
        

    # продолжить сбор email адресов
    def next_parsing_emails(self): 
        self.main_function.finished = False 
        self.main_function.parsing_emails()
        self.status_btn() 

    def refresh_table(self): 
       self.fill_table() 
        
    def fill_table(self): 
        self.table_emails.setRowCount(0)
        db = DataBase() 
        row = db.select("SELECT * FROM email LIMIT 1")
        self.table_emails.setColumnCount(len(row[0]))

        rows = db.select("SELECT * FROM email")
        self.table_emails.setRowCount(len(rows))

        for row, stroka in enumerate(rows):
            for column, cell in enumerate(stroka):  
                self.table_emails.setItem(row,column, QtWidgets.QTableWidgetItem(cell))

    def set_phrazes(self):
        phrazes = self.plain_text_edit_phrazes.toPlainText().split('\n')
        self.main_function.get_prazhes(phrazes)
        


if __name__ ==  "__main__": 
    import sys 

    app = QtWidgets.QApplication(sys.argv)
    w = Ui() 
    w.show() 
    sys.exit(app.exec_())

   