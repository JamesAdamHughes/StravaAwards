import smtplib

sender = 'jahughes112@gmail.com'
receivers = ['jahughes112@gmail.com']

emailTemplate = """From: StravaAwards <from@fromdomain.com>
To: To Person <to@todomain.com>
Subject: You Won a Strava {0} Award!

{1}

Way to go you, keep it up!

Thanks,
Your StravaAwards Team
"""

def sendEmail(smtpserver, subject='test', body='body', receivers = receivers, sender = sender, test = 0):

    email = emailTemplate.format(subject, body)

    if test:
        #don't send email during testing
        return "Email disabled for test"
        
    # Try sending the email
    try:
       smtpserver.sendmail(sender, receivers, email)
       print "Successfully sent email"
    except smtplib.SMTPException:
       print "Error: unable to send email"

def getEmailServer():
    # Connect to GMail SMPT Server
    smtpserver = smtplib.SMTP("smtp.gmail.com", 587)

    # login with my credentials
    try:
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.ehlo()
        smtpserver.login('', '')
    except smtplib.SMTPAuthenticationError:
        print 'Incorrect Email login Details'
        exit()

    return smtpserver