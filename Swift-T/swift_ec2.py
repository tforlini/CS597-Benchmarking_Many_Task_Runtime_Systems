import boto.ec2
import sys
from boto.manage.cmdshell import *
import logging
import os


class Swift_EC2:
    def __init__(self, aws_access_key=None, aws_secret_key=None, region='us-west-2', log_level=logging.INFO):
        """
        :param aws_access_key: access key in the AWS credentials
        :type aws_access_key: str or None
        :param aws_secret_key: secret key in the AWS credentials
        :type aws_access_key: str or None
        :param region: AWS region in which instances will be launched
        :type region: str
        :param log_level: level of logging messages to display
        """
        # Load the AWS credentials from environment variables if not given.
        if aws_access_key is None:
            aws_access_key = os.environ.get('AWS_ACCESS_KEY')
        if aws_secret_key is None:
            aws_secret_key = os.environ.get('AWS_SECRET_KEY')
        if aws_access_key is None or aws_secret_key is None:
            raise Exception('Define the environment variables AWS_ACCESS_KEY '
                            'and AWS_SECRET_KEY before running this program.')
        self.aws_access_key = aws_access_key
        self.aws_secret_key = aws_secret_key
        self.region = region
        self.log = logging.getLogger("ec2_cli")
        self.log.setLevel(log_level)
        hdl = logging.StreamHandler()
        hdl.setFormatter(logging.Formatter('[%(levelname)-s-%(name)s] - %(asctime)s - %(message)s'))
        self.log.addHandler(hdl)
        self.conn = self.connect()
        self.inst_running = {}
        self.ami_id = None
        self.instance_type = None
        self.instance_name_base = None
        self.key_name = None
        self.security_groups = None
        self.username = None
        self.master_flag = None
        self.max_i = 0

    def connect(self):
        """
        Create a connection to the EC2 service.
        :return: a boto object to handle the connection
        """
        self.log.debug("Connecting to AWS")
        conn = boto.ec2.connect_to_region(self.region,
                                          aws_access_key_id=self.aws_access_key,
                                          aws_secret_access_key=self.aws_secret_key)
        return conn

    def launch_n_instances(self, ami_id, n, instance_type=None, master_flag=None, name=None,
                           key_path=None, security_groups=None):
        """
        Launch n new EC2 instances with the given parameters and tag them with an unique and simple name.
        :param ami_id: id of the AMI to launch
        :type ami_id: str
        :param instance_type: type of the EC2 instance
        :type instance_type: str
        :param n: number of workers to launch
        :type n: int
        :param master_flag: launch one additional node dedicated to be the master if this flag is set to True
        :type master_flag: bool
        :param name: base name of every worker
        :type name: str
        :param key_path: path to the key to use for SSH connections
        :type key_path: str
        :param security_groups: name of the security groups
        :type security_groups: list
        """
        self.ami_id = ami_id
        if instance_type is not None:
            self.instance_type = instance_type
        if name is not None:
            self.instance_name_base = name
        if key_path is not None:
            self.key_path = key_path
            self.key_name = os.path.split(key_path)[1]
            self.key_basename = self.key_name.split('.')[0]
        if security_groups is not None:
            self.security_groups = security_groups
        if master_flag is not None and self.master_flag is None:
            self.master_flag = master_flag

        self.log.debug("Launching %d instances" % n)
        if self.master_flag:
        	n += 1
        reservation = self.conn.run_instances(self.ami_id, key_name=self.key_basename, max_count=n,
                                              instance_type=instance_type, security_groups=security_groups)
        time.sleep(1.*n/5.) # empirical value to wait when running n instances
        self.__tag_instances(reservation.instances)

    def __tag_instances(self, instances):
        """
        Tag given instances with a simple and unique name.
        :param instances: instances to tag
        :type instances: list
        """
        self.log.debug("Tagging instances")
        for inst in instances:
            if self.master_flag and 'master' not in self.inst_running.values():
                tags = {'Name': 'master'}
                self.master_flag = False
            else:
                tags = {'Name': "%s%d" % (self.instance_name_base, self.max_i)}
                self.max_i += 1
            self.conn.create_tags(inst.id, tags)
            self.inst_running[inst.id] = tags['Name']

    def __wait_running(self):
        """
        Wait for all the launched instances to be in a running state.
        """
        instances = self.conn.get_only_instances()
        self.log.debug("Waiting for all the instances to be running")
        for inst in instances:
            inst.update()
            if inst.state == 'pending':
                self.log.debug("    - %s not running" % inst.tags['Name'])
                while inst.state != 'running':
                    self.log.debug("    - %s not running, let's wait 10 more seconds" % inst.tags['Name'])
                    time.sleep(10)
                    inst.update()
                self.log.debug("    - %s  running" % inst.tags['Name'])
            elif inst.state == 'running':
                self.log.debug("    - %s  running" % inst.tags['Name'])

    def __wait_ssh(self, username):
        """
        Wait for all the launched instances to accept SSH connection with the given username.
        :param username: user name to use to connect to each instance
        :type username: str
        """
        self.log.debug("Waiting for all the instances to accept SSH connection")
        self.username = username
        instances = self.conn.get_only_instances()
        for inst in instances:
            if inst.state != 'running':
                continue
            self.log.debug("    - %s not ready for SSH" % inst.tags['Name'])
            while True:
                try:
                    ssh = paramiko.SSHClient()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    ssh.connect(inst.ip_address, username=username,
                                key_filename=os.path.abspath(self.key_path))
                    break
                except Exception:
                    self.log.debug("    - %s not ready for SSH, let's wait 10 more seconds" % inst.tags['Name'])
                    time.sleep(10)
                    inst.update()
            self.log.debug("    - %s ready for SSH" % inst.tags['Name'])

    def __create_ip_list(self):
        """
        Creates and returns a list containing all the private IP addresses of
        the running instances.
        """
        self.log.debug("Creating list of IP addresses")
        instances = self.conn.get_only_instances()
        ip_list = []
        for inst in instances:
            if inst.state != 'running':
                continue
            master_flag = False
            if 'Name' in inst.tags:
                if inst.tags['Name'] == 'master':
                    master_flag = True
            ip_list.append(inst.private_ip_address)
        return ip_list

    def activate_nokey_ssh(self, username='ec2-user'):
        """
        Allow communication between workers without login by copying hosts
        file and ssh config file.
        :param username: user name to use to connect to each instance
        :type username: str
        """
        self.__wait_running()
        self.__wait_ssh(username)
        ip_list = self.__create_ip_list()

        # Write the hosts file to local disk
        with open('hosts.txt', 'w+') as hosts_file:
            hosts_file.write("\n".join(ip_list))
        with open('config', 'w+') as config_file:
            config_file.write("Host *\n\tIdentityFile ~/%s\n\tUser %s\n\tStrictHostKeyChecking no" % (self.key_name, username))

        instances = self.conn.get_only_instances()
        for inst in instances:
            if inst.state != 'running':
                continue
            self.log.debug("Copying files to %s [%s]" % (inst.tags['Name'], inst.ip_address))
            # Copy hosts file
            cp_hosts = "scp -oStrictHostKeyChecking=no -q -i %s hosts.txt %s@%s:~/hosts.txt" % (
                self.key_path, username, inst.ip_address)
            # Copy private key
            cp_key = "scp -oStrictHostKeyChecking=no -q -i %s %s %s@%s:~/%s" % (
                self.key_path, self.key_name, username, inst.ip_address, self.key_name)
            # Copy ssh config
            cp_config = "scp -oStrictHostKeyChecking=no -q -i %s config %s@%s:~/.ssh/config" % (
                self.key_path, username, inst.ip_address)
            subprocess.call(cp_hosts, shell=True)
            subprocess.call(cp_key, shell=True)
            subprocess.call(cp_config, shell=True)

    def deploy_app(self, program, n_workers, adlb_servers=1, args=None, copy_to_all=None, copy_to_master=None, copy_to_workers=None):
        """
        :param program: path to the Swift script to deploy
        :type program: str
        :param n_workers: total number of Turbine MPI processes
        :type n_workers: int
        :param adlb_servers: number of ADLB servers
        :type adlb_servers: int
        :param args: arguments to give to the Swift script (e.g "-f=~/myarg.txt -d=1000")
        :type args: str
        :param copy_to_all: paths to files to copy on every running instances
        :type copy_to_all: list
        :param copy_to_master: paths to files to copy on the master instance
        :type copy_to_master: list
        :param copy_to_workers: paths to files to copy on the worker instances
        :type copy_to_workers: list
        """
        if not args:
            args = ''
        if not copy_to_all:
            copy_to_all = []
        if not copy_to_master:
            copy_to_master = []
        if not copy_to_workers:
            copy_to_workers = []

        inst_master = None
        instances = self.conn.get_only_instances()
        for inst in instances:
            if inst.state != 'running':
                continue

            self.log.debug('Pushing the program and additional files to %s.' % (inst.tags['Name']))

            if inst.tags['Name'] == 'master':
                inst_master = inst
                # copy files specific to master
                for file in copy_to_master:
                    cp_script = "scp -oStrictHostKeyChecking=no -q -i %s %s %s@%s:~" % (
                        self.key_path, file, self.username, inst.ip_address)
                    subprocess.call(cp_script, shell=True)
            else: # worker instances
                # copy files specific to workers
                for file in copy_to_workers:
                    cp_script = "scp -oStrictHostKeyChecking=no -q -i %s %s %s@%s:~" % (
                        self.key_path, file, self.username, inst.ip_address)
                    subprocess.call(cp_script, shell=True)

            # copy given files to all instances
            for file in copy_to_all:
                cp_script = "scp -oStrictHostKeyChecking=no -q -i %s %s %s@%s:~" % (
                    self.key_path, file, self.username, inst.ip_address)
                subprocess.call(cp_script, shell=True)

            # copy application script
            cp_script = "scp -oStrictHostKeyChecking=no -q -i %s %s %s@%s:~" % (
                self.key_path, program, self.username, inst.ip_address)
            subprocess.call(cp_script, shell=True)
            last_inst = inst

        if inst_master is None:
            inst_master = last_inst

        # Run Swift script from master
        ssh_client = sshclient_from_instance(inst_master, self.key_path, user_name=self.username)
        cmd = '''
        export ADLB_SERVERS=%d
        export ADLB_PRINT_TIME=1
        export ADLB_PERF_COUNTERS=1
        export TURBINE_LAUNCHER_OPTIONS='-f=hosts.txt'
        export TURBINE_LOG=0
        swift-t -n %d %s %s
        '''
        args_str = " ".join(["-A %s" % a for a in args.split()])
        stdin, stdout, stderr = ssh_client.run(cmd % (adlb_servers, n_workers, args_str, program))
        return stdin, stdout, stderr

    def terminate_workers(self):
        """
        Terminate all EC2 running instances.
        """
        instances = self.conn.get_only_instances()
        to_terminate = []
        for inst in instances:
            if inst.state != 'terminated':
                name = "[" + inst.tags['Name'] + "] " if inst.tags['Name'] != '' else ''
                self.log.debug("Add instance %s %sto the list of instances to terminate." % (inst.id, name))
                to_terminate.append(inst.id)
                self.inst_running.pop(inst.id)
        self.conn.terminate_instances(to_terminate)
