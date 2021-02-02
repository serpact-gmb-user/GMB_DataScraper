import smtplib, ssl
import yagmail

### GENERIC EMAIL SENDING SOLUTION WITH SSL.
""" port = 465
smtp_server = "smtp.gmail.com"
sender_email = "stoyan.ch.stoyanov11@gmail.com"
receiver_email = "stoyan.ch.stoyanov11@gmail.com"
password = input("Type in your password here:")
message = Add docstring here
Subject: Test_Email


This message is a test email message from PyCharm IDE 2020."""

# Create a secure SSL context.
"""context = ssl.create_default_context()

with smtplib.SMTP_SSL(smtp_server, port, context=context) as email_server:
    email_server.login(sender_email, password)
    email_server.sendmail(sender_email, receiver_email, message)
"""
### SENDING EMAILS VIA YAGMAIL MODULE (SPECIFIC FOR GMAIL)
receiver = "stoyan.ch.stoyanov11@gmail.com"
body = "Hello, there, this is a test email!"
filename = "Execution.log"
password = input("Please, input a password here:")

try:
    yag = yagmail.SMTP("stoyan.ch.stoyanov11@gmail.com", password=password)
    yag.send(to=receiver, subject="Mail sent with attachment", contents=body, attachments=filename)
except Exception as e:
    print(f"Error: {e}")
