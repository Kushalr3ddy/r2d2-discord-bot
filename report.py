import smtplib,ssl
import os

port = 465


context = ssl.create_default_context()
server = smtplib.SMTP_SSL("smtp.gmail.com",port,context=context)

from_mail = "botdsu@gmail.com"
to_mail="pikkikushal@gmail.com"
message= "hello"
#server.connect()
server.login(from_mail,os.getenv("MAIL_PASSWORD"))

def sendmail():
    server.sendmail(from_mail,to_mail,message)
    with open("mail.log","a") as f:
        f.write(f"sent mail to:{to_mail}:{message}")
        print("done")

sendmail()