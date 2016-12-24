import subprocess
import time


# Logging function
def AddLog(status):
    # Add line to status log
    logFile = open('restartlog.txt', 'a')
    timeString = time.asctime(time.localtime(time.time()))
    logFile.write('%s %s\n' % (timeString, status))
    # Force the log to be written out
    logFile.flush()
    logFile.close()


# Start the process first time
process = subprocess.Popen(['/home/pi/miniconda/bin/python', '/home/pi/pitimer/pitimer.py'])
AddLog('Started')

while True:
    # Check the state of the process
    status = process.poll()

    if status is not None:
        # Terminated, restart process
        process = subprocess.Popen(['/home/pi/miniconda/bin/python', '/home/pi/pitimer/pitimer.py'])
        print 'Termination code %d, restarted' % (status)
        AddLog('Restarted')
    else:
        # Still running
        time.sleep(1)
