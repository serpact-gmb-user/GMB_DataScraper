#!/usr/bin/python
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders

# def send_mail(send_from,send_to,subject,text,files,server,port,username='',password='',isTls=True):
msg = MIMEMultipart()
msg['From'] = "stoyan.ch.stoyanov11@gmail.com"
msg['To'] = "12114108.stoyan.stoyanov@gmail.com"
msg['Date'] = formatdate(localtime=True)
msg['Subject'] = "Testing email with attachment"
text = "Testing email with attachment body section."
msg.attach(MIMEText(text))

part = MIMEBase('application', "octet-stream")
part.set_payload(open("GMB_End_Keyword_SearchTimes.csv", "rb").read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', 'attachment; filename="GMB_End_Keyword_SearchTimes.csv"')
msg.attach(part)

# context = ssl.SSLContext(ssl.PROTOCOL_SSLv3)
# SSL connection only working on Python 3+
smtp = smtplib.SMTP("smtp.gmail.com", 587)
smtp.starttls()
smtp.login("stoyan.ch.stoyanov11@gmail.com", "St-564289713")
smtp.sendmail("stoyan.ch.stoyanov11@gmail.com", "12114108.stoyan.stoyanov@gmail.com", msg.as_string())
smtp.quit()
