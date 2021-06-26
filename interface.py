
from time import sleep
from PyQt5 import uic, QtWidgets
from PyQt5.uic.properties import float_list 
from model.models import ModelEmail, ModelSite
from libray.export_excel import ExportExcel
from controller.controllers import ControllerColectingSites, ControllerColecting
from threading import Thread
from PyQt5.QtCore import QThread, pyqtSignal

Form, _ = uic.loadUiType("untitled.ui")


class Ui(QtWidgets.QMainWindow, Form): 
    def __init__(self):
        super(Ui, self).__init__() 
        self.setupUi(self)

        self.main_function = ControllerColecting([]) 

        self.fill_table() 
        self.btn_start.clicked.connect(self.start)
        self.btn_finish.clicked.connect(self.stop)
        self.btn_refresh.clicked.connect(self.fill_table)
        self.btn_next.clicked.connect(self.next_parsing_emails)
        #self.btn_export.clicked.connect(self.main_function.export_excle_email) 
        self.btn_finish.setEnabled(False)
        

    def start(self):
        self.main_function.phraze = self.set_phrazes()
        print(self.main_function.phraze)
        self.main_function.start() 
        self.btn_start.setEnabled(False)
        self.btn_finish.setEnabled(True)

        thead_statistic = Thread(target=self.statistic)
        thead_statistic.start() 

    def statistic(self): 

        while True: 
            sleep(4)
            self.queuesite = len(self.main_function.QueueSite.site_queue) 
            self.label_queue_sites.setText(str(self.queuesite))

            self.countsite = self.main_function.ColectingSites.count_site
            self.label_count_sites.setText(str(self.countsite))

            self.processed_site_count  = self.main_function.ColectingEmails.processed_site_count
            self.label_processed_sites.setText(str(self.processed_site_count))

            self.label_count_email.setText(str(self.main_function.ColectingEmails.processed_email_count))
        

    def stop(self): 
        self.main_function.stop()
        self.btn_start.setEnabled(True)
        self.btn_finish.setEnabled(False)

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
            return phrazes
            

if __name__ ==  "__main__": 
    import sys 

    app = QtWidgets.QApplication(sys.argv)
    w = Ui() 
    w.show() 
    sys.exit(app.exec_())