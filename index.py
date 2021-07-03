from model.models import ModelEmail, ModelSite
from libray.export_excel import ExportExcel
#from controller.controllers import ControllerColectingSites, QueueSite, ControllerColectingEmails, ControllerColecting 
from controller.controllersdev import ControllerColectingEmails, ControllerColectingSites 


# data_site = ModelSite()
# data_site.create()
# data_site.write('rost-seo.ru', 'start', '21.09.21')

# data_emails = ModelEmail() 
# data_emails.create() 
# data_emails.write('ivanhel@yandex.ru', 'rost-seo.ru', '', '')
# ExportExcel().export_emails() 

# collecting =ControllerColectingSites([])
# collecting.set_phrazes(['спортивный магазин'])
# collecting.start() 

# rows = ModelEmail().select("SELECT * FROM sites")
# ModelEmail().query("UPDATE sites SET status ='start'")
# for row in rows: 
#     print(row[0], row[1])



site = ControllerColectingSites(['купить мороженное оптом', 'Купить брикет']) 


site.start()



 
