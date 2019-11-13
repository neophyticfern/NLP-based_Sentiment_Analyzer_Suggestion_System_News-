import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_mail(recipient, subject, message):  

    username = "nfernandes2@scu.edu"
    password = "XXXXXXX"

    msg = MIMEMultipart()
    msg['From'] = 'nfernandes2@scu.edu'
    msg['To'] = recipient
    msg['Subject'] = 'Hello'    
    msg.attach(MIMEText(message))

    try:
        print('sending mail to ' + recipient + ' on ' + subject)

        mailServer = smtplib.SMTP('smtp-mail.outlook.com', 587)
        mailServer.ehlo()
        mailServer.starttls()
        mailServer.ehlo()
        mailServer.login(username, password)
        mailServer.sendmail(username, recipient, msg.as_string())
        mailServer.close()

    except error as e:
        print(str(e))


send_mail('singuava@scu.edu', 'Importtant Articles', 'Please find the ImportantNewsarticles for last 7 days:')
