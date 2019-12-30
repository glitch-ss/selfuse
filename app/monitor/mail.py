import smtplib
from email.mime.text import MIMEText
from email.header import Header

class lucien801():
    def __init__(self):
        self.mail_host='smtp.sina.com'
        self.mail_user='lucien801@sina.com'
        self.mail_pass='atobefuji'
        
        self.sender='lucien801@sina.com'
        self.receiver=['380589027@qq.com']
        self.receiver2=['547076180@qq.com']
      

    def sm(self, band, message):
        self.subject = band
        self.message = MIMEText(message,'plain','utf-8')
        self.message['From'] = Header('lucien801@sina.com')
        self.message['To'] = Header('<547076180@qq.com>','utf-8')
        self.message['Subject']=Header(self.subject,'utf-8')
        smtpObj=smtplib.SMTP()
        smtpObj.connect(self.mail_host,25)
        smtpObj.login(self.mail_user,self.mail_pass)
        smtpObj.sendmail(self.sender, self.receiver, self.message.as_string())
        #smtpObj.sendmail(self.sender, self.receiver2, self.message.as_string())

