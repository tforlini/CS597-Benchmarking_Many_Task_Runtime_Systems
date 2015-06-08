import os 

#21708
def mProcess(benchmarks):
    fdR = open("MProcessedResults.txt", 'w')
    for b in benchmarks:
        fdR.write("Benchmark "+b+"\n")
        nWorker = b.split(".")[0]
        sumLatency = 0
        tasks = 0
        for i in range(1, int(nWorker)+1):
            path = "MatrixResults/Matrix"+ b + "/instance" + str(i) + "/"
            files = sorted([f for f in os.listdir(path)])
            if i == 1:
                fd = open(path+files[0])
                content = fd.readlines()
                fdR.write(content[-2])
                fd.close()
                fd = open(path+files[3])
            else:
                fd = open(path+files[1])
                
            content = fd.readlines()
            for line in content:
                s = line.split()
                if s[1] == "SubmissionTime":
                    currentTask = s[0]
                    currentTime = s[2]
                elif s[1] == "WaitQueueTime" and currentTask == s[0]:
                    #print s[2] + " " + currentTask
                    sumLatency += int(s[2]) - int(currentTime)
                    tasks += 1
                
            fd.close()
        print sumLatency
        print tasks
        fdR.write("Average latency = " + str(float(sumLatency)/float(tasks)) + "\n\n")
        print "benchmark "+ b +" processed"
    fdR.close()
    
def sProcess(benchmarks):
    fdR = open("SProcessedResults.txt", 'a')
    for b in benchmarks:
        fdR.write("Benchmark "+b+"\n")
        nWorker = b.split(".")[0]
        sumLatency = 0
        tasks = 0
        for i in range(1, int(nWorker)+1):
            path = "SparrowResults/Sparrow"+ b + "/instance" + str(i) + "/"
            files = sorted([f for f in os.listdir(path)])
            print files
            print "\n\n"
            if i == 1:
                fd = open(path+files[0])
                content = fd.readlines()
                fdR.write(content[-1])
                files.pop(0)
                fd.close()
                
            fd = open(path+files[1])
            unsortedContent = fd.readlines()
            
            content = []
            
            for line in unsortedContent:
                content = content + [line.split(",")]
            #print content
            #print "\n\n"
            content.sort(key=lambda x: x[0])
            print content[:10]        
            nlines = len(content)
            l1 = content[0]
            i = 1
            while i < nlines-1:
                if i % 1000 == 1 :
                    print i 
                l2 = content[i]
                if l1[0] == l2[0]:
                    if l1[1] == "Launched":
                        #print "latency = " + str(int(l1[2]) - int(l2[2]))
                        sumLatency += int(l1[2]) - int(l2[2])
                    else:
                        #print "latency = " + str(int(l2[2]) - int(l1[2]))
                        sumLatency += int(l2[2]) - int(l1[2]) 
                    l1 = content[i+1]
                    i += 2
                    tasks += 1
                else:
                    l1 = l2
                    i += 1 
            fd.close()
        fdR.write("Average latency = " + str(float(sumLatency)/float(tasks)) + "\n tasks = " +str(tasks) + "\n\n")
        print "benchmark "+ b +" processed"
    fdR.close()
    
    
if __name__ == "__main__":
    benchmarks = ['1.0', '1.1', '1.10', '1.100', '1.1000', '2.0', '2.1', '2.10', '2.100', '2.1000', '4.0', '4.1', '4.10', '4.100',
     '4.1000', '8.0', '8.1',
'8.10', '8.100', '8.1000', '16.0', '16.1', 
'16.10', '16.100', '16.1000', '32.0', '32.1', 
'32.10', '32.100', '32.1000', '64.0', '64.1', 
'64.10', '64.100', '64.1000', '128.0', '128.1', '128.10', '128.100', '128.1000'
    ]
    
    #mProcess(benchmarks)
    fd = open("MProcessedResults.txt", "r")
    content = fd.readlines()
    fd.close()
    i = 0
    for line in content:
        content[i] = line.replace("\n", "\r\n")
        i += 1
        
    fd = open("WinMProcessedResults.txt", "w")
    for line in content:
        fd.write(line)
    fd.close()
    
    
