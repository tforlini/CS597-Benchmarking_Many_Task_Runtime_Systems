import subprocess, os, shlex, time, sys

def runBenchmark (MasterIp, benchmarkId):

    home = "/home/ubuntu"
    zhtSrcPath = home +"/matrix_v2/ZHT/src"
    matrixPath = home +"/matrix_v2/matrix/src"

    zhtCommand = "cd "+ zhtSrcPath +"; ./zhtserver -z zht.conf -n neighbor.conf"
    schedulerCommand = "cd "+ matrixPath +"; ./scheduler config"
    clientCommand = "cd "+ matrixPath +"; ./client config"


    ## Launching of apps
    a0 = shlex.split("pssh -t 0 -p 128 -v -x \"-i matrix.pem -o StrictHostKeyChecking=no\" -l ubuntu -h host \"rm /home/ubuntu/matrix_v2/matrix/src/*0* \"")
    subprocess.call(a0)
    print "runMatrixB - previous results deleted\n"
    a = shlex.split("pssh -t 0 -p 128 -x \"-i matrix.pem -o StrictHostKeyChecking=no\" -l ubuntu -h host \"" + zhtCommand +"\"")
    subprocess.Popen(a)
    print "runMatrixB - ZHT launched\n"
    
    time.sleep(20)
    
    b = shlex.split("pssh -t 0 -p 128 -v -x \"-i matrix.pem -o StrictHostKeyChecking=no\" -l ubuntu -h host \"" + schedulerCommand +"\"")
    subprocess.Popen(b)
    #ab = shlex.split("pssh -t 0 -p 128 -vi -x \"-i matrix.pem -o StrictHostKeyChecking=no\" -l ubuntu -h host \"cd /home/ubuntu/matrix_v2/matrix/src; ./launchMatrixBackend.sh\"")
    #subprocess.Popen(ab)
    print "runMatrixB - Scheduler launched\n"

    time.sleep(20)

    #raw_input("runMatrix-Benchmark DEBUG- before client. Press enter to continue\n")
    c = ("pssh -t 0 -p 128 -vi -x \"-i matrix.pem -o StrictHostKeyChecking=no\" -l ubuntu -H "+  MasterIp   +" \"" + clientCommand +"\"")
    print c
    subprocess.call(shlex.split(c))
    print "runMatrixB - Client launched\n"
    ##

    ## Killing of aps
    d = shlex.split("pnuke -t 0 -p 128 -v -x \"-i matrix.pem -o StrictHostKeyChecking=no\" -l ubuntu -h host \"scheduler\"")
    subprocess.call(d)
    d = shlex.split("pnuke -t 0 -p 128 -v -x \"-i matrix.pem -o StrictHostKeyChecking=no\" -l ubuntu -h host \"zht\"")
    subprocess.call(d)
    print "runMatrixB - ZHT&Scheduler nuked\n"
    ##
    
    print "runMatrixB - Grabbing Results"
    subprocess.call("cd ~/workspace/AWSscripts/MatrixResults;mkdir Matrix"+benchmarkId, shell = True)
    fd = open("dns", "r")
    dnsList = [l.replace("\n", "") for l in fd.readlines()]
    fd.close()

    instanceIdx = 1
    
    for DNS in dnsList:
        subprocess.call("cd ~/workspace/AWSscripts/MatrixResults;mkdir Matrix"+benchmarkId+"/instance" + str(instanceIdx), shell = True)
        print "\nrunMatrixB - instance " + str(instanceIdx) + " " + DNS 
        c = shlex.split("scp -i matrix.pem -o StrictHostKeyChecking=no ubuntu@" + DNS + 
                        ":/home/ubuntu/matrix_v2/matrix/src/*0* /home/thomas/workspace/AWSscripts/MatrixResults/Matrix"
                        + benchmarkId+"/instance"+ str(instanceIdx))
        subprocess.call(c)
        instanceIdx += 1
    print "\nrunMatrixB - Results grabbed"
    
if __name__ == "__main__":
    
    fd = open("host", "r")
    ip = fd.readline().replace("\n", "")
    fd.close()
    
    idx = "test"
    runBenchmark(ip, idx, test = True)
    
