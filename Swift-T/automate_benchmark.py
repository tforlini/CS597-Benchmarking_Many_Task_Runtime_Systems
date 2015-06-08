'''
Usage: automate_benchmark.py <benchmark_params.json>
'''
import subprocess
import json
import sys
from swift_ec2 import Swift_EC2
import logging
from collections import defaultdict
import math

def run_job(j, out):
    if j['type'] == "homogeneous":
        sleep_time = j['duration']
        quantity = n_workers * j['quantity']
        log.debug("Run benchmark on %d nodes (%d workers, %d adlb servers): %d sleeps of %f seconds" % (n_nodes, n_workers, n_adlb_servers, quantity, sleep_time))
        stdin, stdout, stderr = api.deploy_app(j['program'], max(2,n_cores), args="t=%f n=%d" % (sleep_time, quantity))
        out.write("%d, %d, %d, %d, %f, %s\n" % (n_nodes, n_cores, n_workers, quantity, sleep_time, stdout.strip()))
        out.flush()
    elif j['type'] == "heterogeneous":
        log.debug("Run benchmark on %d nodes (%d workers, %d adlb servers): %d sleeps of %f seconds" % (n_nodes, n_workers, n_adlb_servers, quantity, sleep_time))
        stdin, stdout, stderr = api.deploy_app(j['program'], max(2,n_cores), args="f=%s" % (j['data']), copy_to_all=[j['data']])
        out.write("%d, %d, %d, %s, %s\n" % (n_nodes, n_cores, n_workers, j['data'], stdout.strip()))
        out.flush()
    elif j['type'] == "dag":
        raise NotImplementedError;
    else:
        raise NotImplementedError;

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise Exception(__doc__)

    with open(sys.argv[1]) as params_fd:
        params = json.load(params_fd)

    # Set logger
    log = logging.getLogger("auto_bench")
    log_levels = {"ERROR": logging.ERROR,
                  "WARNING": logging.WARNING,
                  "WARN": logging.WARN,
                  "DEBUG": logging.DEBUG,
                  "INFO":logging.INFO,
                  "FATAL":logging.FATAL,
                  "CRITICAL": logging.CRITICAL
    }
    log.setLevel(log_levels[params['log-level']])
    hdl = logging.StreamHandler()
    hdl.setFormatter(logging.Formatter('[%(levelname)-s-%(name)s] - %(asctime)s - %(message)s'))
    log.addHandler(hdl)

    # Open results file
    out = open(params['output-file'], "w")
    try:
        api = Swift_EC2(log_level=params['log-level'])
        log.debug("Parsing jobs...")
        scale = set()
        n_jobs = 0
        benchmarks = defaultdict(list)
        header = ""

        for j in params['jobs']:
            scale |= set(j['scale'])
            n_jobs += len(j['scale'])
            benchmarks[j['type']].append(j)
        sorted_scale = sorted(list(scale))
        log.debug("%d jobs to execute with scale up to %d nodes." % (n_jobs, sorted_scale[-1]))
        last_n_nodes = 0
        for n_nodes in sorted_scale:
            n_cores = params['cores-per-node'] * n_nodes
            if params['scale-adlb']:
                n_adlb_servers = max(1, int(math.ceil(.2*n_cores)))
            else:
                n_adlb_servers = 1
            n_workers = max(1, n_cores - n_adlb_servers)
            n_mpi_proc = max(2, n_cores)
            n_new_nodes = n_nodes-last_n_nodes
            log.debug("Launching %d new node%s. Total nodes: %d" % (n_new_nodes, 's' if n_new_nodes > 1 else '',n_nodes))
            api.launch_n_instances(params['ami-id'], n_new_nodes, params['instance-type'], True, "worker",
                                   params['key-path'], params['security-groups'])
            last_n_nodes += n_new_nodes
            api.activate_nokey_ssh(params['username'])

            for type_job, jobs_list in benchmarks.iteritems():
                jobs_at_scale = [j for j in jobs_list if n_nodes in j['scale']]
                for j in jobs_at_scale:
                    new_header = params['header'][type_job]
                    if new_header != header:
                        header = new_header
                        out.write(header + "\n")
                    run_job(j, out)
    except Exception as e:
        log.error(repr(e))
    finally:
        if len(api.inst_running) > 0:
            api.terminate_workers()
        out.close()
