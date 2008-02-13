'''Log creashes to file and mail them.

Use either "import crashlog" in your code or run with "python -m crashlog"
'''

__author__ = "Miki Tebeka <miki.tebeka@gmail.com>"

# This program is distributed under the MIT license, please read
# http://www.opensource.org/licenses/mit-license.php

import sys
from cStringIO import StringIO
from datetime import datetime
from email.MIMEText import MIMEText
from smtplib import SMTP
from traceback import print_tb
from os import environ
from os.path import split, isdir, join
from socket import gethostname

_LOG_FILE = "/tmp/crashlog.log"
_MAIL_TO = [
    "taz@looney.com",
    "duffy@looney.com",
    "bugs@looney.com"
]

# Don't mail anyone when not on production machine, just the developer
if gethostname() != "production-machine":
    default_user = "duffy"
    if "USER" in environ:
        user = environ["USER"]
    elif "SCRIPT_FILENAME" in environ:
        dirs = split(environ["SCRIPT_FILENAME"])
        # /home/duffy
        if isdir(join(*dirs[:2])):
            user = dirs[1]
        else:
            user = default_user
    else:
        user = default_user

    _MAIL_TO = [ "%s@looney.com" % user ]

_LOADED = 0
_AS_MAIN = 0

def format_message(type, value, traceback):
    # execfile playes tricks with argv
    if _AS_MAIN:
        program = sys.argv[1]
        args = sys.argv[1:]
    else:
        program = sys.argv[0]
        args = sys.argv

    # Format message
    io = StringIO()
    print >> io, "Arguments: %s" % " ".join(args)
    print >> io, "Date: %s" % datetime.now()
    print >> io, "Environment:"
    for var in environ:
        print >> io, "\t%s --> %s" % (var, environ[var])
    
    print >> io, "Traceback:"
    print_tb(traceback, file=io)
    print >> io, "%s: %s" % (type, value)
    print >> io

    return io.getvalue(), program

def write_to_log(message):
    fo = open(_LOG_FILE, "at")
    fo.write(message)
    fo.close()

def mail_message(message, program):
    mail = MIMEText(message)
    mail["From"] = "crashlog@%s" % gethostname()
    mail["To"] = "Crashers"
    mail["Subject"] = "%s crashed" % program
    smtp = SMTP("smtp.looney.com")

    smtp.helo()
    smtp.starttls()
    smtp.sendmail("crashlog@looney.com", _MAIL_TO, mail.as_string())
    smtp.close()

def excepthook(type, value, traceback):
    message, program = format_message(type, value, traceback)
    write_to_log(message)
    mail_message(message, program)

    # Run original exception hook
    sys.__excepthook__(type, value, traceback)

if not _LOADED:
    sys.excepthook = excepthook
    _LOADED = 1

if __name__ == "__main__":
    _AS_MAIN = 1
    execfile(sys.argv[1])
