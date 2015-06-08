#!/usr/bin/python

'''
Usage: init_ec2.py launch_workers [-n=N] 
       init_ec2.py terminate_workers
       init_ec2.py copy_files <program>
       init_ec2.py deploy <program> 
Options:
   -n --n-workers=N       number of workers to run [default: 1]
   -s --start=S           start point of instance index [default: 1]
   -p --program=P         program to deploy on every node of the EC2 cluster
'''

import boto.ec2, os, subprocess, paramiko, sys, time, string
from docopt import docopt
from boto.manage.cmdshell import sshclient_from_instance
from AWSconf import *

#paramiko.util.log_to_file("paramiko_ssh.log")

# IP STORAGE
def storeIps(pIps, Ips, host = 'host', privateIps = 'privateIps'):
    hostFile = open(host, 'a')
    for ip in Ips:
        hostFile.write(ip+"\n")
    hostFile.close()
    
    pFile = open(privateIps, 'a')
    for ip in pIps:
        pFile.write(ip+"\n")
    pFile.close()    

def setIps(pIps, ips, host = 'host', privateIps = 'privateIps'):
    hostFile = open(host, 'w')
    for ip in ips:  
        hostFile.write(ip+"\n")
    hostFile.close()
    
    pFile = open(privateIps, 'w')
    for ip in pIps: 
        pFile.write(ip+"\n")
    pFile.close()
#

# IP + DNS STORAGE -for scp commands- 
def addDnsIps(ips, dns = 'dns' ):
    dnsFile = open(dns , 'a')
    for ip in ips:
        scpIp = string.replace(ip, ".", "-")
        dnsFile.write("ec2-" + scpIp + AwsDns +"\n")
    dnsFile.close()

def setDnsIps(ips, dns = 'dns'):   
    dnsFile = open(dns , 'w')
    for ip in ips:
        scpIp = string.replace(ip, ".", "-")
        dnsFile.write("ec2-" + scpIp + AwsDns +"\n")
    dnsFile.close()
    
def connect(aws_access_key_id= AWSAccessKeyId,
            aws_secret_access_key=AWSSecretKey, region='us-west-2'):
            
    conn = boto.ec2.connect_to_region("us-west-2",
                                       aws_access_key_id= aws_access_key_id,
                                       aws_secret_access_key= aws_secret_access_key)
    return conn
#

def run_ec2_workers(instances, conn, n_workers=1, name='worker_', start=1, timeOut = 60):
    reservation = conn.run_instances(image_id= AMI, instance_type = instanceType,
                                             key_name= sshKey, min_count = n_workers,
                                             max_count = n_workers, 
                                             security_group_ids =[securityGroup])
    time.sleep(5)


    notLaunched = range(n_workers)
    ips = []
    privateIps = []
    toLaunch = n_workers
    time.sleep(2)
    startTime = time.time()

    while toLaunch > 0 and (time.time() - startTime) < timeOut:
        print "".join(("init_ec2 - still ", str(toLaunch), " instance(s) to launch")) 
        
        idx = notLaunched.pop(0)
        update = reservation.instances[idx].update()
        if update == "running":
            ips.append(reservation.instances[idx].ip_address)
            privateIps.append(reservation.instances[idx].private_ip_address)
            instances.append(reservation.instances[idx])
            toLaunch -= 1
        else:
            notLaunched.append(idx)
            time.sleep(5)
    
    if toLaunch == 0:
        print "".join(("init_ec2 - ", str(n_workers), " instance(s) launched in ", str(time.time() - startTime), " seconds\n"))
    else:
        print "".join(("init_ec2 - Timeout", str(toLaunch), " instances not launched in time"))
    
    for i, instance in enumerate(reservation.instances):
        tags = {'Name': "%s%d" % (name, i+start)}
        conn.create_tags(instance.id, tags)
    
    return (instances, privateIps, ips)


def wait_ssh(conn):
    print "Waiting for all the instances to accept SSH connection"
    ssh_client = paramiko.SSHClient()
    instances = conn.get_only_instances()
    for inst in instances:
        #print inst.tags
        if inst.state != 'running':
            continue
        if inst.tags['Name'][:7] != "worker_":
            continue 
        sys.stdout.write("    - %s " % inst.tags['Name'])
        sys.stdout.flush()
        while True:
            try:
                sshclient_from_instance(inst, "./%s.pem" % sshKey, user_name=username)
                break
            except paramiko.SSHException:
                time.sleep(10)
                inst.update()
                print '.'
        sys.stdout.write('    ok!\n')

def wait_init(conn):
    ready = False
    while(not(ready)):
        print "init_ec2 - checking status"
        status = conn.get_all_instance_status()
        ready = True
        for s in status:
            if s.system_status.details["reachability"] == "initializing":
                print "init_ec2 - an instance is still initializing"
                ready = False
                time.sleep(10)
                break
    print "init_ec2 - initialization completed\n"

def terminate_workers(conn):
	instances = conn.get_only_instances()
	to_terminate = []
	for inst in instances:
		if inst.state != 'terminated' and inst.tags['Name'][:7] == "worker_":
			name = "[" + inst.tags['Name'] + "] " if inst.tags['Name'] != '' else ''
			print "Add instance %s %sto the list of instances to terminate." % (inst.id, name)
			to_terminate.append(inst.id)
	conn.terminate_instances(to_terminate)


if __name__ == '__main__':
    

    args = docopt(__doc__)
    print args['--n-workers']
    conn = connect(AWSAccessKeyId, AWSSecretKey, "us-west-2")
    if args['launch_workers']:
        if args['--start'] != '':
            start = int(args['--start'])
        else:
            start = 1
        instances, pIps, Ips = run_ec2_workers([],conn, n_workers=int(args['--n-workers']), start=start)
                   
        setIps(pIps, Ips, host = 'host_all', privateIps = 'privateIps_all')
        setDnsIps(Ips, dns = 'dns_all')
    elif args['copy_files']:
        gen_hosts(conn, args['--runtime-system'], args['--key-name'],
                  args['--username'])
    elif args['deploy']:
        deploy(conn, args['<program>'], int(args['--n-workers']),
               args['--runtime-system'], args['--username'], args['--key-name'])
    elif args['terminate_workers']:
    	terminate_workers(conn)
