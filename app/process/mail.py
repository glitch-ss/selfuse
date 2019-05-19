import smtplib
from email.mime.text import MIMEText
from email.header import Header

class lucien801():
    def __init__(self, band, message):
        self.mail_host='smtp.sina.com'
        self.mail_user='lucien801@sina.com'
        self.mail_pass='atobefuji'
        
        self.sender='lucien801@sina.com'
        self.receiver=['380589027@qq.com']
        
        message = MIMEText(message,'plain','utf-8')
        message['From'] = Header('lucien801@sina.com')
        message['To'] = Header('7<380589027@qq.com>','utf-8')
        
        subject=band
        message['Subject']=Header(subject,'utf-8')
        
        smtpObj=smtplib.SMTP()
        smtpObj.connect(self.mail_host,25)
        smtpObj.login(self.mail_user,self.mail_pass)
        smtpObj.sendmail(self.sender, self.receiver, message.as_string())
