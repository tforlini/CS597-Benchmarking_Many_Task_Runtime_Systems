import subprocess, shlex, string
   
if __name__ == "__main__":

    ips = ["52.11.154.179","52.11.107.126"]
    
    for ip in ips:
        print ip
        dash = string.replace(ip, ".", "-")
        print "scp -i ../python/matrix.pem ubuntu@ec2-"+ dash +".us-west-2.compute.amazonaws.com:~/sparrow/Results* ./"
        subprocess.call(shlex.split("scp -i ../python/matrix.pem ubuntu@ec2-"+ dash +".us-west-2.compute.amazonaws.com:~/sparrow/Results* ./"))
        raw_input("next grab, press enter")
