
from time import sleep
from PyQt5 import uic, QtWidgets
from PyQt5.uic.properties import float_list
from model.models import ModelEmail, ModelSite
from libray.export_excel import ExportExcel
from controller.controllersdev import ControllerColectingSites, ControllerColectingEmails
from threading import Thread
from PyQt5.QtCore import QThread, pyqtSignal

Form, _ = uic.loadUiType("untitled.ui")


class Ui(QtWidgets.QMainWindow, Form): 
    def __init__(self):
        super(Ui, self).__init__() 
        self.setupUi(self)

        self.fill_table() 
        self.btn_start.clicked.connect(self.start)
        self.btn_finish.clicked.connect(self.stop)
        self.btn_refresh.clicked.connect(self.fill_table)
        self.btn_next.clicked.connect(self.next_parsing_emails)
        self.btn_export.clicked.connect(self.export)




        #self.btn_export.clicked.connect(self.main_function.export_excle_email) 
        self.btn_finish.setEnabled(False)
        self.finish_parsing = False 
        self.site = ControllerColectingSites([]) 
        self.email = ControllerColectingEmails()
       

    def start(self):

        self.site.finished = False 
        self.email.finished = False
        self.finish_parsing = False 


        self.site.set_phrazes(self.set_phrazes()) 
        
        self.site.start()
        self.email.start()
        
        t = Thread(target=self.queue)
        t.start() 
        
        statis = Thread(target=self.statistic)
        statis.start()

        self.btn_start.setEnabled(False) 
        self.btn_finish.setEnabled(True) 

      


    def queue(self): 
        while self.finish_parsing == False: 

            if len(self.site.save_site) > 0 and self.email.queue.qsize() == 0:
                self.email.create_queue(self.site.save_site) 
                self.site.save_site = [] 
            
            if len(self.email.emails) > 0: 
                for em in self.email.emails: 
                    if em != []: 
                        ModelEmail().write(em['email'], em['source'], em['domain'], '30.06.2021')
                self.email.emails = []  


            count = self.site.count_site - self.email.count_sites

            if self.site.finished == True and self.email.queue.qsize() == 0 and count == 0 and self.email.work != True: 
                self.btn_start.setEnabled(True) 
                self.btn_finish.setEnabled(False) 
                self.email.finished = True
                self.finish_parsing = True
               


    def statistic(self): 

        while self.finish_parsing == False: 
            # self.queuesite = len(self.main_function.QueueSite.site_queue) 
            # self.label_queue_sites.setText(str(self.queuesite))

            # self.countsite = self.main_function.ColectingSites.count_site
            # self.label_count_sites.setText(str(self.countsite))

            # self.processed_site_count  = self.main_function.ColectingEmails.processed_site_count
            # self.label_processed_sites.setText(str(self.processed_site_count))
            
            self.label_queue_sites.setText(str(self.site.count_site - self.email.count_sites))
            self.label_count_sites.setText(str(self.site.count_site))

            self.label_processed_sites.setText(str(self.email.count_sites))
            self.label_count_email.setText(str(self.email.counts))
    
    #экспорт таблицы 
    def export(self): 
        try: 
            name = QtWidgets.QFileDialog.getSaveFileName(self, 'Сохранить файл', 'export',  '*.xlsx')
            ExportExcel().export_emails(name[0]) 
        except: 
            pass
        
        

    def stop(self): 
    
        self.btn_start.setEnabled(True) 
        self.btn_finish.setEnabled(False) 

        self.email.finished = True
        self.finish_parsing = True
        self.finish_parsing = True 

    def clean(self): 
        self.table_emails.setRowCount(0)
        self.table_emails.setColumnCount(4)
        ModelEmail().query('')



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