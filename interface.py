
from PyQt5 import uic, QtWidgets
from PyQt5.uic.properties import float_list 
from model.models import ModelEmail, ModelSite
from libray.export_excel import ExportExcel
from controller.controllers import ControllerColectingSites
from threading import Thread
from PyQt5.QtCore import QThread, pyqtSignal

Form, _ = uic.loadUiType("untitled.ui")


class Ui(QtWidgets.QMainWindow, Form): 
    def __init__(self):
        super(Ui, self).__init__() 
        self.setupUi(self)

        self.main_function = ControllerColectingSites() 

        self.fill_table() 
        self.btn_start.clicked.connect(self.start)
        self.btn_finish.clicked.connect(self.stop)
        self.btn_refresh.clicked.connect(self.fill_table)
        self.btn_next.clicked.connect(self.next_parsing_emails)
        #self.btn_export.clicked.connect(self.main_function.export_excle_email)

        self.loading_animation() 


    def start(self):
        self.main_function.finished = True
        self.main_function.finished = False 

        self.set_phrazes() 
        self.main_function.start()

        self.btn_start.setEnabled(False)


    def loading_animation(self): 
        while self.main_function.finished == False: 
            self.label_queue_sites.text(self.self.main_function.queue_sites)
        

    def stop(self): 
        self.main_function.finished = True
        self.btn_start.setEnabled(True)

    #статусы кнопок
    def status_btn(self):
        pass
        
    # продолжить сбор email адресов
    def next_parsing_emails(self): 
        pass
    
    #заполнить таблицу 
    def fill_table(self): 
        '''Запрашивает у базы данных значения из таблицы emails, после чего осуществляет заполнение таблицы формы ''' 
        self.table_emails.setRowCount(0)
        db = ModelEmail() 
        #row = db.select("select * from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME='emails'")
        self.table_emails.setColumnCount(4)

        rows = db.select("SELECT * FROM emails")
        self.table_emails.setRowCount(len(rows))

        for row, stroka in enumerate(rows):
            for column, cell in enumerate(stroka):  
                self.table_emails.setItem(row,column, QtWidgets.QTableWidgetItem(cell))

    #фразы для поиска email 
    def set_phrazes(self):
        if self.plain_text_edit_phrazes.toPlainText() != '': 
            phrazes = self.plain_text_edit_phrazes.toPlainText().split('\n')
            self.main_function.set_phrazes(phrazes)
            

if __name__ ==  "__main__": 
    import sys 

    app = QtWidgets.QApplication(sys.argv)
    w = Ui() 
    w.show() 
    sys.exit(app.exec_())