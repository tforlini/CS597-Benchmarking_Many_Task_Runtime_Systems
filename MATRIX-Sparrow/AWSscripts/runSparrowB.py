import subprocess, os, shlex, time, sys

def runBenchmark (MasterIp, benchmarkId, test = False):


    if test:
        a = shlex.split("pssh -t 5 -v -x \"-i matrix.pem -o StrictHostKeyChecking=no\" -l ubuntu -H " 
        + MasterIp +" \"cd sparrow; python python/SparrowLocal.py -l all -nw 1\"")
    else:
        a = shlex.split("pssh -t 5 -v -x \"-i matrix.pem -o StrictHostKeyChecking=no\" -l ubuntu -h host \"cd sparrow; python python/SparrowLocal.py -l all -nw 1\"")
    
    subprocess.call(a)
    print "runSparrowB - backend&sparrow launched, previous call should return \"failed\" in normal use case\n"


    if test:
        b = shlex.split("pssh -t 0 -vi -x \"-i matrix.pem -o StrictHostKeyChecking=no\" -l ubuntu -H " + MasterIp +" \"cd sparrow; python python/RunSparrowTEST.py\"")
    else:
        b = shlex.split("pssh -t 0 -vi -x \"-i matrix.pem -o StrictHostKeyChecking=no\" -l ubuntu -H " + MasterIp +" \"cd sparrow; python python/RunSparrow.py\"")
    subprocess.call(b)
    print "\nrunSparrowB - Launched Frontend\n"

    if test:
        a2 = shlex.split("pssh -v -x \"-i matrix.pem -o StrictHostKeyChecking=no\" -l ubuntu -H " + MasterIp +" \"cd sparrow; python python/SparrowLocal.py -k all \"")
    else:
        a2 = shlex.split("pssh -v -x \"-i matrix.pem -o StrictHostKeyChecking=no\" -l ubuntu -h host \"cd sparrow; python python/SparrowLocal.py -k all \"")
    subprocess.call(a2)
    print "runSparrowB - Killed backend\n"

    print "runSparrowB - Grabbing Results"
    subprocess.call("cd ~/workspace/AWSscripts/SparrowResults;mkdir Sparrow"+benchmarkId, shell = True)

    if test:
        fd = open("dns", "r")
        #print "runSparrow - DEBUG 1st DNS line = "  
        DNS = fd.readline().replace("\n", "")
        fd.close()
        instanceIdx = 1
        c = shlex.split("scp -i matrix.pem ubuntu@" + DNS + ":/home/ubuntu/sparrow/python/Results.txt /home/thomas/workspace/AWSscripts/SparrowResults/Sparrow"
                                + benchmarkId+"/instance"+ str(instanceIdx)+"/")
        subprocess.call(c)
        c = shlex.split("scp -i matrix.pem ubuntu@" + DNS + 
                            ":/home/ubuntu/sparrow/Results{Backend.txt,Scheduling.txt} /home/thomas/workspace/AWSscripts/SparrowResults/Sparrow"
                            + benchmarkId+"/instance"+ str(instanceIdx))
        subprocess.call(c)
    else:
        fd = open("dns", "r")
        dnsList = [l.replace("\n", "") for l in fd.readlines()]
        fd.close()
        
        instanceIdx = 1
        
        for DNS in dnsList:
            subprocess.call("cd ~/workspace/AWSscripts/SparrowResults;mkdir Sparrow"+benchmarkId+"/instance" + str(instanceIdx), shell = True)
            print "\nrunSparrowB - instance " + str(instanceIdx) + " " + DNS 
            if instanceIdx == 1:
                c = shlex.split("scp -i matrix.pem ubuntu@" + DNS + ":/home/ubuntu/sparrow/python/Results.txt /home/thomas/workspace/AWSscripts/SparrowResults/Sparrow"
                                + benchmarkId+"/instance"+ str(instanceIdx)+"/")
                subprocess.call(c)
            c = shlex.split("scp -i matrix.pem ubuntu@" + DNS + 
                            ":/home/ubuntu/sparrow/Results{Backend.txt,Scheduling.txt} /home/thomas/workspace/AWSscripts/SparrowResults/Sparrow"
                            + benchmarkId+"/instance"+ str(instanceIdx))
            subprocess.call(c)
            instanceIdx += 1
    print "\nrunSparrowB - Results grabbed"

if __name__ == "__main__":
    
    fd = open("host", "r")
    ip = fd.readline().replace("\n", "")
    fd.close()
    
    idx = "test"
    runBenchmark(ip, idx, test = True)
    
