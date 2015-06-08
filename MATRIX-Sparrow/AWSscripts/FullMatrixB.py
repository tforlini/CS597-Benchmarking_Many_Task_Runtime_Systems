import shlex, subprocess, init_ec2, string, runMatrixB, time
from AWSconf import * 

benchmarks = [#'1.0', '1.1', '1.10','1.100', 
#'1.1000', '2.0', '2.1', 
#'2.10','2.100',
#'2.1000', '4.0', 
#'4.1', 
#'4.10', 
#'4.100', '4.1000', 
#'8.0', '8.1', '8.10', '8.100', '8.1000', '16.0', '16.1', '16.10', '16.100', '16.1000', '32.0', '32.1', '32.10', '32.100', '32.1000', 
#'64.0', '64.1', '64.10', '64.100', '64.1000', 
'128.0', '128.1', '128.10', '128.100', '128.1000']

numberNodes = (#1*[1] + 
#1*[2] + 
#2*[4] + 
#5*[8] + 5*[16] + 5*[32] + 
#5*[64] + 
5*[128])

numberTasks = [1500,1500, 200, 200, 50]
numberBenchmark = -1

##Testing benchmarks
#benchmarks = ['1.1', '2.0', '4.0']
#numberNodes = 1*[1] + 1*[2] + 1*[4]
#benchmarks = ['64.0']
#numberNodes = 1*[64]

#numberNodes = 1*[2] #+ 1*[64]
#benchmarks = ['2.1'#,'64.0'
#
#]

maxInstances = numberNodes[-1]
mainNodeIP= ""
mainNodePIP = ""
mainNodeDNS = ""
pIPS = []
IPS = []
instances = []

mConfigPath = "/home/thomas/workspace/matrix_v2/matrix/src/config"
zhtSrcPath = "/home/thomas/workspace/matrix_v2/ZHT/src/"
matrixPath = "/home/thomas/workspace/matrix_v2/matrix/src/"


def getIps():
    fd = open('host_all', 'r')
    content = fd.readlines()
    ips = [f.replace("\n","") for f in content]
    
    fd.close()
    
    fd = open('privateIps_all', 'r')
    content = fd.readlines()
    pips = [f.replace("\n","") for f in content]
    fd.close()
    
    return(pips, ips)
    
    

def createMatrixConf(nJobs):
    fd = open(mConfigPath,'r')
    content= fd.readlines()
    fd.close()
    
    content[0] = 'NumTaskPerClient	' + str(nJobs) +'\n'
    content[1] = 'NumAllTask	' + str(nJobs) + '\n' 
    
    fp=open(mConfigPath,'w')
    fp.writelines(content)
    fp.close()

def addMatrixIps(ips, port=50000):
    ipsPort = [" ".join((x, str(port))) for x in ips]
    fd = open(zhtSrcPath+"neighbor.conf",'a')
    for ip in ipsPort:
        fd.write(ip + "\n")
    fd.close()

    fd = open(matrixPath+"memlist",'a')
    for ip in ips:
        fd.write(ip + "\n")
    fd.close()
    
def setMatrixIps(ips, port=50000):
    ipsPort = [" ".join((x, str(port))) for x in ips]
    fd = open(zhtSrcPath+"neighbor.conf",'w')
    for ip in ipsPort:
        fd.write(ip + "\n")
    fd.close()

    fd = open(matrixPath+"memlist",'w')
    for ip in ips:
        fd.write(ip + "\n")
    fd.close()

if __name__ == '__main__':

    instancesStored = 0
    firstBenchmark = True
    subprocess.call("rm dns host privateIps",shell = True)
    conn = init_ec2.connect()
    print "Matrix-Benchmark - start\n"
    
    print "Matrix-Benchmark - launching instances\n"
        # all instances are launched at start to avoid connection problem at startup
    #instances, pIps, Ips = init_ec2.run_ec2_workers(instances, conn, n_workers =  maxInstances)
    pIps, Ips = getIps()
    #init_ec2.wait_ssh(conn)
    #init_ec2.wait_init(conn)
    
    ## setting main instance
    mainNodeIP,mainNodePIP = Ips[0], pIps[0]
    mainNodeDNS = "ec2-" + string.replace(mainNodeIP, ".", "-") + AwsDns
    ##
    
    for i in range(0,len(numberNodes)):
        numberBenchmark += 1
        subprocess.call(shlex.split("pnuke -t 0 -x \"-i matrix.pem -o StrictHostKeyChecking=no\" -l ubuntu -h host  zht"))
        print "Matrix-Benchmark - benchmark" + benchmarks[i] + "\n"
        ##Store instances if necessary
        if numberNodes[i] != instancesStored:
            pIps_to_store = pIps[instancesStored:numberNodes[i]]
            Ips_to_store = Ips[instancesStored:numberNodes[i]]
            init_ec2.storeIps(pIps_to_store, Ips_to_store)
            init_ec2.addDnsIps(Ips_to_store)
            #raw_input("Status checks completed000? press enter")
            
            ##push backend/Matrixconfig on all instances.

                #add ips to memlist and neighbor.conf            
            setMatrixIps(pIps[:numberNodes[i]])
                #change config file  
            pushNeighborConf = ("pscp -t 0 -x \"-i matrix.pem -o StrictHostKeyChecking=no\" -l ubuntu -h dns  " 
                                    + zhtSrcPath + 
                                    "neighbor.conf /home/ubuntu/matrix_v2/ZHT/src/")
                                    
            pushMatrixConf = ("pscp -t 0 -x \"-i matrix.pem -o StrictHostKeyChecking=no\" -l ubuntu -h dns  " 
                                    + matrixPath + 
                                    "memlist /home/ubuntu/matrix_v2/matrix/src/")
            
            subprocess.call(shlex.split(pushNeighborConf))
            print pushNeighborConf
            #raw_input("Matrix-Benchmark - pushed neighbor.conf. Press enter to continue\n")
            subprocess.call(shlex.split(pushMatrixConf))
            print pushMatrixConf
            #raw_input("Matrix-Benchmark - pushed memlist,config. Press enter to continue\n")
            print "Matrix-Benchmark - Pushed Backend&Matrix Config\n"             
            instancesStored = numberNodes[i]
            ##
        nTasks = numberTasks[numberBenchmark % 5] * numberNodes[i]
        print 'Matrix-Benchmark - ntask = ' + str(nTasks)
        createMatrixConf(nTasks) 
        pushMatrixConf2 = ("pscp -t 0 -x \"-i matrix.pem -o StrictHostKeyChecking=no\" -l ubuntu -h dns  " 
                                    + matrixPath + 
                                    "config /home/ubuntu/matrix_v2/matrix/src/")
        subprocess.call(shlex.split(pushMatrixConf2))
        print pushMatrixConf2
        ##        

        ##Change workload on main node
        sleepLength = benchmarks[i].split(".")[1]     
        pushFConf = ("pssh -t 0 -x \"-i matrix.pem -o StrictHostKeyChecking=no\" -l ubuntu -H "+ mainNodeDNS +
                                " \" cd /home/ubuntu/matrix_v2/matrix/src; cp  Bworkloads/sleep"
                                + sleepLength +" workload\"")
        subprocess.call(shlex.split(pushFConf))
        print pushFConf
        print "Matrix-Benchmark - Changed workload\n"
        ##

        ##run benchmark
        raw_input("Matrix-Benchmark - Pushed all conf files. Press enter to start benchmark\n")
        runMatrixB.runBenchmark(mainNodeIP, benchmarks[i])   
        time.sleep(10)    
        #raw_input("Matrix-Benchmark - press enter for next benchmark")
        ##
    #raw_input("Matrix-Benchmark - Kill instances? press enter")
    ## Kill instances     
    #init_ec2.terminate_workers(conn)        

