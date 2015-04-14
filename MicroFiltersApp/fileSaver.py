import subprocess
import time
import sys

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
print "done"
