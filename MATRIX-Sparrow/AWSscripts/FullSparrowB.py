import shlex, subprocess, init_ec2, string, runSparrowB, time
from AWSconf2 import * 

benchmarks = [
#'1.0', '1.1', '1.10', '1.100', '1.1000', 
#'2.0', '2.1', '2.10', '2.100', '2.1000', '4.0', '4.1', '4.10', '4.100', '4.1000', 
#'8.0', '8.1', 
#'8.10', '8.100', '8.1000', 
#'16.0', '16.1', 
#'16.10', '16.100', '16.1000', 
#'32.0', '32.1', 
#'32.10', '32.100', '32.1000',
#'64.0', '64.1', 
#'64.10', '64.100', '64.1000', 
#'128.0', '128.1', 
'128.10', '128.100', '128.1000'
]

numberNodes = (#5*[1] + 
#5*[2] + 5*[4] + 2*[8] +
#3*[8] + 
#3*[16] + 3*[32] + 3*[64] +
3*[128]
)

##Testing benchmarks
#benchmarks = ['1.1', '2.0', '4.0']
#numberNodes = 1*[1] + 1*[2] + 1*[4]
#benchmarks = ['1.1','64.0']
#numberNodes = 1*[1] + 1*[64]

maxInstances = numberNodes[-1]
mainNodeIP= ""
mainNodePIP = ""
mainNodeDNS = ""
pIPS = []
IPS = []
instances = []

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
    
confFilePath = "/home/thomas/workspace/sparrow-master/Conf/"
sparrowPath = "/home/thomas/workspace/sparrow-master/"

def createBackendConf(ip):
    fd = open(confFilePath + 'conf.Backend1', 'w')
    fd.write("app_client_ip = "+ ip +"\n")
    fd.write("worker_threads = 2\nlog_level = off\n")
    fd.close()

if __name__ == '__main__':

    instancesStored = 0
    firstBenchmark = True
    subprocess.call("rm dns host privateIps",shell = True)
    conn = init_ec2.connect()
    print "Sparrow-Benchmark - start\n"
    
    print "Sparrow-Benchmark - launching instances\n"
    # all instances are launched at start to avoid connection problem at startup
    #instances, pIps, Ips = init_ec2.run_ec2_workers(instances, conn, n_workers =  maxInstances)
    pIps, Ips = getIps()
    #init_ec2.wait_ssh(conn)
    #init_ec2.wait_init(conn)
    ## setting main instance
    mainNodeIP,mainNodePIP = Ips[0], pIps[0]
    mainNodeDNS = "ec2-" + string.replace(mainNodeIP, ".", "-") + AwsDns
    createBackendConf(mainNodePIP)
    ##
    
    for i in range(0,len(numberNodes)):
        print "Sparrow-Benchmark - benchmark" + benchmarks[i] + "\n"
        ##Store instances if necessary
        if numberNodes[i] != instancesStored:
            pIps_to_store = pIps[instancesStored:numberNodes[i]]
            Ips_to_store = Ips[instancesStored:numberNodes[i]]
            print pIps_to_store
            print Ips_to_store
            init_ec2.storeIps(pIps_to_store, Ips_to_store)
            init_ec2.addDnsIps(Ips_to_store)
            #raw_input("Status checks completed000? press enter")
            
            ##push backend/sparrowconfig on all instances.
            #print "Sparrow-Benchmark - DEBUG\n    pIPS set in sparrow- conf = "+ str(pIps[:numberNodes[i]]) +"\n" 
            #raw_input("GO CHECK DNS FILE? press enter")
            subprocess.call("cd ~/workspace/sparrow-master/python; python SparrowConfigC.py set " 
                            + " ".join(pIps[:numberNodes[i]]), shell = True)
            pushSConf = "pscp -t 0 -v -x \"-i matrix.pem -o StrictHostKeyChecking=no\" -l ubuntu -h dns  " + sparrowPath + "sparrow.conf /home/ubuntu/sparrow/"
                                    
            pushBConf = "pscp -t 0 -v -x \"-i matrix.pem -o StrictHostKeyChecking=no\" -l ubuntu -h dns  " + confFilePath + "conf.Backend1 /home/ubuntu/sparrow/Conf/"
                                    
            subprocess.call(shlex.split(pushSConf))
            print pushSConf
            raw_input("Sparrow-Benchmark - pushed sparrow.conf. Press enter to continue")
            subprocess.call(shlex.split(pushBConf))
            print pushBConf
            raw_input("Sparrow-Benchmark - pushed Backend.conf.\nIf pscp failed for n<" 
                      + str(instancesStored)+ " it should be fine.\nPress enter to continue")
            #print "Sparrow-Benchmark - Pushed Backend&Sparrow Config\n"             
            instancesStored = numberNodes[i]
            ##
        ##        

        ##Push frontend to main node
        subprocess.call("cd ~/workspace/sparrow-master/Conf; cp conf.Frontend"+ benchmarks[i] 
                        +" conf.Frontend1 ", shell = True)
        
        pushFConf = ("pscp -t 0 -v -x \"-i matrix.pem -o StrictHostKeyChecking=no\" -l ubuntu -H "+ mainNodeDNS 
                                + " " + confFilePath + "conf.Frontend1" + " /home/ubuntu/sparrow/Conf/")
        subprocess.call(shlex.split(pushFConf))
        print pushFConf
        print "Sparrow-Benchmark - Pushed Frontend Config\n"
        ##
        
        if firstBenchmark:
            raw_input("Sparrow-Benchmark - Pushed all conf files.\n    TEST FOR CONNECTION WITH runSparrowB.py.\n    Press enter to start benchmark")
            firstBenchmark = False
        else:
            raw_input("Sparrow-Benchmark - Pushed all conf files. Press enter to start benchmark")
        ##run benchmark
        runSparrowB.runBenchmark(mainNodeIP, benchmarks[i])       
        ##
    #raw_input("Sparrow-Benchmark - Kill instances? press enter")
    ## Kill instances     
    #init_ec2.terminate_workers(conn)        
