import subprocess
import time
import sys
import smtplib, os
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders
import tarfile

def send_mail(send_from, send_to, subject, text, files=[], server="localhost"):
    assert type(send_to)==list
    assert type(files)==list

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach( MIMEText(text) )

    for f in files:
        part = MIMEBase('application', "octet-stream")
        part.set_payload( open(f,"rb").read() )
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
        msg.attach(part)

    smtp = smtplib.SMTP_SSL()
    smtp.connect(server, "465")
    smtp.ehlo()
    smtp.login("testingmicrofilters@gmail.com", "micromappers")
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()

done = 0
while done == 0:
    jobsI = subprocess.Popen(["curl", "http://localhost:6800/listjobs.json?project=default"], stdout=subprocess.PIPE)
    jobs = jobsI.communicate()[0]
    jobsArray = jobs.split(" ")
    print jobsArray
    indexRunning  = jobsArray.index('"pending":')
    index1 = jobsArray.index(str(sys.argv[1])[:-1] + ',')
    indexDone  = jobsArray.index('"finished":')
    if index1 > indexDone and indexRunning > index1:
        print index1
        print indexDone
        done=1
        break
    time.sleep(1)
    print "not done yet..."

tar = tarfile.open("TARS/" + str(sys.argv[2]) +".tar.gz", "w:gz")
tar.add("TARS/" + str(sys.argv[2]), arcname=str(sys.argv[2]))
tar.close()
os.chmod("TARS/" + str(sys.argv[2]) +".tar.gz", 0775)
send_mail(send_from="testingmicrofilters@gmail.com", send_to=[sys.argv[3]], subject="Results: Job #"+str(sys.argv[2]), text="The job you submitted to MicroFilters is ready for Download at the following URI: http://microfilter.cs.uwaterloo.ca/MF/TARS/. Your download code is" + str(sys.argv[2]) + " After downloading the attachment to this email, you can reupload it to microfilter.cs.uwaterloo.ca for classification and labeling. Good luck with the project! \n \n Sincerely, \n The MicroFilters team", files=[], server="smtp.gmail.com")
print "done"
