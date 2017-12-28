import os, sys, smtplib
from StravaAwards.service import ConfigService 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import current_app

TESTING = 0

emailTemplate = """
<h1>You Won a Strava Award!</h1>

{1}

Way to go you, keep it up!<br/><br/>

Thanks,<br/>
Your StravaAwards Team
"""

def send_email(subject='', body='body', receivers=['jahughes112@gmail.com'], sender='noreply@jameshughes.info', test=TESTING):
    """ Send an email """

    log("sending email...")

    message = MIMEMultipart('alternative')
    message['subject'] = subject
    message['To'] = ''.join(receivers)
    message['From'] = sender

    html_body = MIMEText(emailTemplate.format(subject, body, receivers[0]), 'html')

    message.attach(html_body)

    # Try sending the email
    try:
        smtpserver = get_email_server()        
        smtpserver.sendmail(sender, receivers, message.as_string())
        smtpserver.quit()
        log("Successfully sent email")
        return True
    except ValueError:
        log("[emailU] Error: unable to send email " + str(sys.exc_info()))
        return False


def get_email_server():
    """
    Connect to Postfix Server and Returns an SMTP server to send emails
    In dev this connects to my gmail, in prod this connects to a local postfix server
    """

    enviroment = os.getenv('ENVIROMENT')

    if enviroment == 'development':
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()

        gmail_user = ConfigService.getConfigVar("smpt.username")
        gmail_pwd = ConfigService.getConfigVar("smpt.password")

        server.login(gmail_user, gmail_pwd)
        return server
    else:
        return smtplib.SMTP("localhost", 25)
    
def log(text):
    current_app.logger.info("[emailUtils] " + str(text))