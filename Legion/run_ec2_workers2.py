#!/usr/bin/python
'''
Usage: run_ec2_workers.py <ami_id> [--main] [--n-workers=N] [--instance-type=I] [--name=N] [--region=R] [--security-group=S] [--key-name=K] [--runtime-system=A] [--username=U]

Options:
   -i --instance-type=I   type of the instance to run [default: t2.micro]
   -k --key-name=K        name of the private key [default: dataintensive]
   -n --n-workers=N       number of workers to run [default: 1]
   -r --region=R          region in which the instances are launched [default: us-west-2]
   -s --security-group=S  security group [default: all-traffic-allowed]
   --name=N               generic name to give to the workers [default: worker_]
   -a --runtime-system=A  runtime system to use [default: charm]
   -u --username=U        name of the main user to connect to the instances [default: ubuntu]
   --main               flag indicating that a main node must be launched in addition to the worker nodes
'''
from docopt import docopt
import boto.ec2
import os
import subprocess
import re
import sys
import time

def connect(aws_access_key, aws_secret_key, region='us-west-2'):
    print "Connecting to AWS"
    conn = boto.ec2.connect_to_region(region,aws_access_key_id=aws_access_key,aws_secret_access_key=aws_secret_key)
    return conn

def run_ec2_workers(conn, ami_id, instance_type='t2.micro', n_workers=1,main_flag=False, name='worker_',key_name='key_clus',security_group='launch-wizard-39'):
    if conn is None:
        raise Exception('Need to connect to AWS before being able to run instances')

    if main_flag:
        n_workers += 1
    print "Launching %d instances" % n_workers
    reservation = conn.run_instances(ami_id, key_name=key_name,max_count=n_workers,instance_type=instance_type,security_groups=[security_group])
    print "Tagging instances"
    for i, instance in enumerate(reservation.instances):
        tags = {'Name': "%s%d" % (name, i)}
        if i == 0 and main_flag:
            tags['Name'] = 'main'
        conn.create_tags(instance.id, tags)

def gen_hosts(conn, runtime_system='charm', key_name='key_clus',username='ubuntu'):
    if conn is None:
        raise Exception('Need to connect to AWS before being able to run instances')

    reservations = conn.get_all_reservations()

    print "Waiting for all the instances to be running"
    for r in reservations:
        instances = r.instances
        for inst in instances:
            if inst.state != 'pending':
                continue
            while inst.state != 'running':
                time.sleep(10)
                inst.update()
                sys.stdout.write('.')
                sys.stdout.flush()
        for inst in instances:
            if inst.state != 'running':
                continue
            main_flag = False
            if 'Name' in inst.tags:
                if inst.tags['Name'] == 'main':
                    main_flag = True
            hosts['swift'] += "%s\n" % inst.private_ip_address
            if not main_flag:
                hosts['legion'] += inst.private_ip_address+" "
                hosts['charm'] += "\nhost %s" % inst.private_ip_address
            else:
                main = inst.ip_address
                print(main)
    hosts['legion'] += "\'"
    print hosts

    if runtime_system == 'charm':
        with open("nodelist",'a+') as nodelist_file:
            nodelist_file.write(hosts['charm'])
        abspath = os.path.abspath('nodelist')
        print("NODE = %s" % main)
        time.sleep(10)
        cmd = "scp -oStrictHostKeyChecking=no -i %s.pem %s %s@%s:~/.nodelist"% (key_name, abspath, username, main)
        print cmd
        subprocess.call(cmd,shell=True)
    
    elif runtime_system == 'legion':
      time.sleep(10)
      subprocess.call("echo %s | ssh -i %s.pem %s@%s \"cat >> ~/.bashrc\""% (hosts['legion'], key_name, username, main),shell=True)
    

    elif runtime_system == 'swift':
        with open('hosts.txt', 'w+') as hosts_file:
            hosts_file.write(hosts['swift'])
        abspath = os.path.abspath('hosts.txt')
        for r in reservations:
            instances = r.instances
            for inst in instances:
                if inst.state != 'running':
                    continue
                cp_hosts = "scp -oStrictHostKeyChecking=no -i %s.pem %s %s@%s:~/hosts.txt" % (key_name, abspath, username, inst.ip_address)
                cp_key = "scp -oStrictHostKeyChecking=no -i %s.pem %s.pem %s@%s:~/%s.pem" % (key_name, key_name, username, inst.ip_address, key_name)
                cp_config = "scp -oStrictHostKeyChecking=no -i %s.pem config %s@%s:~/.ssh/config" % (key_name, username, inst.ip_address)
                subprocess.call(cp_hosts, shell=True)
                subprocess.call(cp_key, shell=True)
                subprocess.call(cp_config, shell=True)
            
if __name__ == '__main__':
    aws_access_key = os.environ.get('AWS_ACCESS_KEY')
    aws_secret_key = os.environ.get('AWS_SECRET_KEY')
    if aws_access_key is None or aws_secret_key is None:
        raise Exception('Define the environment variables AWS_ACCESS_KEY' \
                        'and AWS_SECRET_KEY before running this program.')

    hosts = {'legion': "export GASNET_SSH_SERVERS='",'charm': "group main ++shell ssh",'swift': ""}
    args = docopt(__doc__)
    launch_main = args['--main'] is not None
    conn = connect(aws_access_key, aws_secret_key, args['--region'])
    run_ec2_workers(conn,args['<ami_id>'], args['--instance-type'],int(args['--n-workers']), launch_main,args['--name'], args['--key-name'],args['--security-group'])
    gen_hosts(conn, args['--runtime-system'], key_name=args['--key-name'],username=args['--username'])
    
