import subprocess, sys

subprocess.Popen(["/usr/bin/time", "-v", sys.executable, './AMQP/read_worker.py'] )


subprocess.Popen(["/usr/bin/time", "-v", sys.executable, './AMQP/write_worker.py'] )



proc = subprocess.Popen([sys.executable, './tests.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# wait() because popen is non blocking
proc.wait()
for line in proc.stderr:  # ls output
    print line

