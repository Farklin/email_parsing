from model.models import ModelEmail, ModelSite
from libray.export_excel import ExportExcel
#from controller.controllers import ControllerColectingSites, QueueSite, ControllerColectingEmails, ControllerColecting 
from controller.controllersdev import ControllerColectingEmails


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

email = ControllerColectingEmails()

email.sites = [

'https://netology.ru/blog/email-all', 
'https://vc.ru/u/668536-sprutmonitor/208256-top-12-servisov-dlya-parsinga-email-adresov', 
'https://go-profit.com/kak-sobirat-email-adresa-besplatno.html', 
'https://www.unisender.com/ru/support/how-to-make/collect-emails/', 
'https://www.directline.pro/blog/sbor-email-adresov/', 
'https://zen.yandex.ru/media/id/5f5758dd75996c43cd2b9be6/gde-naiti-email-luchshie-praktiki-sbora-bazy-5f64735535960479b934889a', 
'https://www.interkassa.com/blog/kak-sobrat-bazu-email-adresov-dlya-rassylki-7-effektivnyh-sposobov-/', 
'https://planeta-zarabotka.ru/jeffektivnye-sposoby-privlechenie-klientov/email-extractor-programma-dlja-sbora-email-adresov.html', 
'https://www.emailory.com/email-marketing/collecting/', 
'https://ru.emailextractorpro.com/', 
'https://rusability.ru/internet-marketing/105-sposobov-sobrat-elektronnye-adresa-dlya-email-marketinga/', 
'https://www.insales.ru/blogs/university/baza-dlya-e-mail-rassylki', 
'https://WebEvolution.ru/blog/marketing/kak-sobrat-bazu-email-adresov-i-telefonov-dlya-rassilki/', 
'https://snov.io/blog/ru/best-email-finder-tools-ru/', 
'https://www.emailfinder.ru/', 
'https://Tools.seo-zona.ru/email.html', 
'http://www.poststar.ru/soft/msg.htm', 
'https://habr.com/ru/post/298646/', 
'https://xmldatafeed.com/10-luchshih-parserov-i-instrumentov-sbora-adresov-elektronnoj-pochty-v-2020-2021-godah-optimalnyj-vybor/', 
'https://yandex.ru/support/mail/web/preferences/collector.html', 
'https://conversion.im/44-sposoba-sbora-email-adresov', 
'https://stripo.email/ru/blog/best-ways-to-collect-email-addresses-to-grow-your-email-list/', 
'https://brandmonkey.ru/blog/e-mail-marketing/126-kak-spamery-sobirayut-email-adresa-i-kak-ot-etogo-zashchititsya', 
'https://www.mail365.ru/kb/%D1%81%D0%B1%D0%BE%D1%80-email-%D0%B0%D0%B4%D1%80%D0%B5%D1%81%D0%BE%D0%B2/', 
'https://blog.ringostat.com/ru/6-sposobov-sobrat-bazu-dlya-email-rassylki/', 
'https://www.epochta.ru/blog/email-marketing/kak-naiyti-1000-emailov/', 
'https://livepage.pro/blog/top-parsing-tools.html', 


]

email.queue() 