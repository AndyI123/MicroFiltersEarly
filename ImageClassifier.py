from glob import glob
import mahotas
import mahotas.features
import mahotas.features.surf
import milk
import os
import PIL
from jug import TaskGenerator
from PIL import Image
import sys


positives = glob(sys.argv[1]+'/Yes/*.jpg') + glob(sys.argv[1]+'/Yes/*.png') + glob(sys.argv[1]+'/Yes/*.jpeg')
negatives = glob(sys.argv[1]+'/No/*.jpg') + glob(sys.argv[1]+'/No/*.png') + glob(sys.argv[1]+'/No/*.jpeg')
unlabeled = glob(sys.argv[1]+'/Test/*.jpg') + glob(sys.argv[1]+'/Test/*.png') + glob(sys.argv[1]+'/Test/*.jpeg')

for x in positives:
    try:
        img = Image.open(x)
        img = img.resize((200, 200), Image.ANTIALIAS)
        img = img.convert('RGB')
        print img.mode
        img.save(x)
    except Exception, e:
        pass
for x in negatives:
    try:
        img = Image.open(x)
        img = img.resize((200, 200), Image.ANTIALIAS)
        img = img.convert('RGB')
        print img.mode
        img.save(x)
    except Exception, e:
        pass
for x in unlabeled:
    try:
        img = Image.open(x)
        img = img.resize((200, 200), Image.ANTIALIAS)
        img = img.convert('RGB')
        print img.mode
        img.save(x)
    except Exception, e:
        pass

def features_for(imname):
    try:
        print imname
        img = mahotas.imread(imname)
        return mahotas.features.haralick(img).mean(0)
    except Exception, e:
        os.remove(x)
        raise e
        return

def learn_model(features, labels):
    learner = milk.defaultclassifier(mode='really-slow')
    return learner.train(features, labels)

def classify(model, features):
     return model.apply(features)

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

labels = [0] * len(negatives) + [1] * len(positives)
features = map(features_for, negatives + positives)
print
model = learn_model(features, labels)
labeled = [classify(model, features_for(str(u))) for u in unlabeled]


f = open(str(sys.argv[2]) + ".txt", 'w+')
for x in xrange(0, len(unlabeled)):
    f.write(unlabeled[x])
    f.write('\n')
    f.write(str(labeled[x]))
    f.write('\n')
f.close()

send_mail(send_from="testingmicrofilters@gmail.com", send_to=[sys.argv[3]], subject="Results: Job #"+str(sys.argv[2])[4:], text="The job you submitted to MicroFilters is ready for Download at the following URI: http://microfilter.cs.uwaterloo.ca/MF/" + str(sys.argv[2]) +". Thanks for using MicroFilters!! \n \n Sincerely, \n The MicroFilters team", files=[], server="smtp.gmail.com")
