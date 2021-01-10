import smtplib

from string import Template

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

MY_ADDRESS = 'stoyan.ch.stoyanov11@gmail.com'
PASSWORD = 'St-564289713'

email_address = "stoyan.ch.stoyanov11@gmail.com"
gmail_pwd = "St-564289713"
receiver_address = '12114108.stoyan.stoyanov@gmail.com'
email_subject = "Testing sending using gmail"
email_text = "Testing sending mail using gmail servers"
server = smtplib.SMTP('smtp.gmail.com', 587)
server.ehlo()
server.starttls()
server.login(gmail_user, gmail_pwd)
email_body = '\r\n'.join(['To: %s' % TO,
                          'From: %s' % email_address,
                          'Subject: %s' % email_subject,
                          '', email_text])

server.sendmail(gmail_user, [receiver_address], email_body)
print('email sent')
