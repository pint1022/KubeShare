#!/bin/bash

command -v nvidia-smi
if [ $? -ne 0 ]; then
    echo "No GPU available, sleep forever"
    sleep infinity
fi

function trap_ctrlc ()
{
    echo "Ctrl-C caught...performing clean up"
    for pid in $pids; do
        kill $pid
    done
    echo "Doing cleanup"
    exit 0
}


trap "trap_ctrlc" 2

port=49901

# def launch_exporter():
#     cmd = "{} -p {} -v 1".format(/alnr-exporter,port)

#     sys.stderr.write("{}\n".format(cmd))    
#     proc = sp.Popen(shlex.split(cmd), universal_newlines=True, bufsize=1)
#     return proc
gpu_list=$(nvidia-smi --format=csv,noheader --query-gpu=uuid)
for gpu in $gpu_list; do
    echo 0 > $1/$gpu
    python3 /launcher.py /gem-schd /gem-pmgr $gpu $1/$gpu $2 --port $port 1>&2 &
    pids="$pids $!"
    port=$(($port+1))
done

# launch_exporter()

wait
