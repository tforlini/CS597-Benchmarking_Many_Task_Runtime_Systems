import subprocess
if __name__ == "__main__":
    benchmarks = ['1.0', '1.1', '1.10', '1.100', '1.1000', '2.0', '2.1', '2.10', '2.100', '2.1000', '4.0', '4.1', '4.10', '4.100',
     '4.1000', '8.0', '8.1',
'8.10', '8.100', '8.1000', '16.0', '16.1', 
'16.10', '16.100', '16.1000', '32.0', '32.1', 
'32.10', '32.100', '32.1000', '64.0', '64.1', 
'64.10', '64.100', '64.1000', '128.0', '128.1', '128.10', '128.100', '128.1000'
    ]

    for b in benchmarks:
        maxNumNode, numTask = b.split(".")
        for i in range(0, int(maxNumNode)):
            subprocess.call("java SchedulingLatency MatrixResults" + b+ "/instance" + str(i+1) + " " + str(i) + " " + numTask)
