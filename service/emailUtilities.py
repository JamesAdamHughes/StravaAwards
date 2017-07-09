import smtplib
import ConfigService

TESTING = 0

emailTemplate = """From: StravaAwards <from@fromdomain.com>
To: To Person <to@todomain.com>
Subject: You Won a Strava {0} Award!

{1}

Way to go you, keep it up!

Thanks,
Your StravaAwards Team
"""

def send_email(subject='test', body='body', receivers=['jahughes112@gmail.com'], sender='jahughes112@gmail.com', test=TESTING):
    """ Send an email """
    if test:
        #don't send email during testing
        print "[emailU] Email disabled for test"
        return "[emailU] Email disabled for test"

    print "[emailU] sending email..."
    smtpserver = get_email_server()
    email = emailTemplate.format(subject, body)

    # Try sending the email
    try:
        smtpserver.sendmail(sender, receivers, email)
        print "[emailU] Successfully sent email"
    except smtplib.SMTPException:
        print "[emailU] Error: unable to send email"


def get_email_server():
    """Connect to GMail SMPT Server"""
    smtpserver = smtplib.SMTP("smtp.gmail.com", 587)

    # login with my credentials
    try:
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.ehlo()
        smtpserver.login(ConfigService.getConfigVar('smpt.username'),
                         ConfigService.getConfigVar('smpt.password'))
    except smtplib.SMTPAuthenticationError:
        print 'Incorrect Email login Details'
        exit()

    return smtpserver
