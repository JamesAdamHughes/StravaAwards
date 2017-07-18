import smtplib
import ConfigService
import os

TESTING = 0

emailTemplate = """From: StravaAwards <noreply@jameshughes.info>
To: To Person <{2}>
Subject: You Won a Strava {0} Award!

{1}

Way to go you, keep it up!

Thanks,
Your StravaAwards Team
"""

def send_email(subject='test', body='body', receivers=['jahughes112@gmail.com', 'sn13762@my.bristol.ac.uk'  ,'test@allaboutspam.com'], sender='jahughes112@gmail.com', test=TESTING):
    """ Send an email """

    enviroment = os.getenv('ENVIROMENT')

    print "[emailU] sending email..."

    if enviroment == 'development':
        #don't send email during testing
        print "[emailU] Email disabled for test"
        return "[emailU] Email disabled for test"

    smtpserver = get_email_server()
    email = emailTemplate.format(subject, body, receivers[0])

    # Try sending the email
    try:
        smtpserver.sendmail(sender, receivers, email)
        print "[emailU] Successfully sent email"
    except smtplib.SMTPException:
        print "[emailU] Error: unable to send email"


def get_email_server():
    """Connect to Postfix Server"""
    smtpserver = smtplib.SMTP("localhost",25)

    return smtpserver
