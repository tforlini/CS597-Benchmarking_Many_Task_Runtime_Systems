
#Frontend configs
taskL = [0,1,10,100,1000]
nodes = [1,2,4,8,16,32,64,128]
numberN = [[50000, 100000, 200000, 400000, 800000, 1600000, 3200000, 6400000],
           [50000, 100000, 200000, 400000, 800000, 1600000, 3200000, 6400000],
           [5000, 10000, 20000, 40000, 80000, 160000, 320000, 640000],
           [500, 1000, 2000, 4000, 8000, 16000, 32000, 64000],
           [50, 100, 200, 400, 800, 1600, 3200, 6400]
           ]
#l = []
for n in range(0,8):
    for t in range(0,5):
#        l.append(str(nodes[n])+"."+str(taskL[t]))
        fd = open('conf.Frontend'+str(nodes[n])+"."+str(taskL[t]), 'w')
        fd.write("experiment_s = "+ str(180) +"\n")
        fd.write("number_tasks = "+ str(numberN[t][n]) +"\n")
        fd.write("task_duration_millis = "+ str(taskL[t]) +"\n")
        fd.write("log_level = off\n")
        fd.close()
print "Frontend config files created"
        
#print l
