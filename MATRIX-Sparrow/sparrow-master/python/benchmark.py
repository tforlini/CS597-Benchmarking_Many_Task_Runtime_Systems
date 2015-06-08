import subprocess, os, shlex, time

os.chdir("/home/thomas/workspace/sparrow-master/python")
subprocess.call(shlex.split("echo \"\" > Finish.txt"), shell = True)
a = shlex.split("pssh -iv -x \"-i matrix.pem -o StrictHostKeyChecking=no\" -l ubuntu -h host \"cd sparrow/python; echo \"Hello world\"\"")
commandFrontend = "java -cp ../target/sparrow-1.0-SNAPSHOT.jar edu.berkeley.sparrow.examples.BFrontend -c ../Conf/conf.Frontend1"
sparrowFrontend = subprocess.Popen(shlex.split(commandFrontend))

startTime = time.time()
run = True
while run and time.time() - startTime < 600:
    #wait for front end to finish
    time.sleep(5)
    print "Benchmark - check Finish.txt"
    fd = open("Finish.txt", "r")
    if fd.readline() == "Experience finished\n":
        run = False
        break
    fd.close()

sparrowFrontend.kill()

print "Experience ended?" + str(not(run))

