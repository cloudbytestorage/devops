#!/usr/bin/env python

import smtplib
from multiprocessing.reduction import send_handle
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

_author_='naveenkumar b'
_email_='naveen.b@emc.com'

def send_mail(send_from, send_to, subject, text, files=None,
              server="outlook2.corp.emc.com"):
    assert isinstance(send_to, list)

    msg = MIMEMultipart(
        From=send_from,
        To=COMMASPACE.join(send_to),
        Date=formatdate(localtime=True),
        Subject=subject
    )
    msg.attach(MIMEText(text))

    for f in files or []:
        with open(f, "rb") as fil:
            msg.attach(MIMEApplication(
                fil.read(),
                Content_Disposition='attachment; filename="%s"' % basename(f),
                Name=basename(f)
            ))

    smtp = smtplib.SMTP(server)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()

if __name__ == '__main__':
    send_mail("naveenkumar.bysani@gmail.com", "naveen.b@emc.com", "regression automation test result", "testing", None)