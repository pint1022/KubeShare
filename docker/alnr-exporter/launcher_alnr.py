import argparse
import os
import sys
import signal
import shlex
import subprocess as sp
import time

args = None
alnr_pid = 0
# def prepare_env(name, alnr_port, sampling):
#     client_env = os.environ.copy()
#     client_env['SAMPLE_IP'] = '127.0.0.1'
#     client_env['SAMPLE_PORT'] = str(alnr_port)
#     client_env['SER_NAME'] = name
#     client_env['SAMPLING_RATE'] = str(sampling)

#     return client_env

def launch_alnr():
    cmd = "{} -d {} -P {} -G {} -s {} -v 1 ".format(
        args.alnr,  args.dir, args.port,  args.gpu_list, args.sampling)
    sys.stderr.write("{}\n".format(cmd))    
    proc = sp.Popen(shlex.split(cmd), universal_newlines=True, bufsize=1, stdout=sp.PIPE)
    while True:
        line = proc.stdout.readline() # returns bytes
        if "ready_string" in line:
           break  
    return proc


def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument('alnr', help='path to alnair server')
    parser.add_argument('dir', help='path to sample file dir')
    parser.add_argument('gpu_list', help='list of uuids')
    parser.add_argument('--port', type=int, default=60018, help='base port of the server')
    parser.add_argument('--sampling', type=int, default=1000, help='sampling rate (ms)')
    args = parser.parse_args()
    sys.stderr.write(f"[launcher] alnair server started on 0.0.0.0:{args.port}\n")
    alnr_pid = launch_alnr()

    sys.stderr.flush()

if __name__ == '__main__':
    os.setpgrp()
    try:
        main()
    except:
        sys.stderr.write("Launcher catch exception: {}\n".format(sys.exc_info()))
        sys.stderr.flush()
    finally:
        os.killpg(0, signal.SIGKILL)
