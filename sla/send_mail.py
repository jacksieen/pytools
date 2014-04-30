import smtplib
import socket

GMAIL_DEFAULT_CONTENT = ""
GMAIL_DEFAULT_DEBUG_LEVEL = 0
GMAIL_DEFAULT_MAIL_TO = ('user@user.com',)
GMAIL_DEFAULT_SUBJECT = "somesubject"
GMAIL_DEFAULT_USERNAME = "admin@admin.com"
GMAIL_DEFAULT_PASSWORD = "********"
GMAIL_HOST = 'smtp.admin.com'
GMAIL_PORT = 25


def send_mail(mail_to=GMAIL_DEFAULT_MAIL_TO,
              mail_subject=GMAIL_DEFAULT_SUBJECT,
              mail_content=GMAIL_DEFAULT_CONTENT,
              debug_level=GMAIL_DEFAULT_DEBUG_LEVEL):
    """
    Send mail.
    """
    mail_username = GMAIL_DEFAULT_USERNAME
    mail_password = GMAIL_DEFAULT_PASSWORD
    mail_from = mail_username
    mail = "From: %s\nreply-to:%s\nTo:%s\nsubject:%s\n\n%s" % \
           (mail_from, ', '.join(mail_to), ', '.join(mail_to),
            mail_subject, mail_content)

    smtp = smtplib.SMTP()
    smtp.set_debuglevel(debug_level)
    try:
        smtp.connect(GMAIL_HOST, GMAIL_PORT)
        smtp.starttls()
        smtp.login(mail_username, mail_password)
        smtp.sendmail(mail_from, mail_to, mail)
        smtp.quit()
        return True
    except socket.gaierror, gaierr:
        print str(gaierr)
        return False
    except smtplib.SMTPAuthenticationError, smtpexcpt:
        print str(smtpexcpt)
        return False
    except Exception, excpt:
        print str(excpt)
        return False

