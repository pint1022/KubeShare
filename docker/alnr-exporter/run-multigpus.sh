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

_list=$(nvidia-smi --format=csv,noheader --query-gpu=uuid)
count=0
for gpu in $_list; do
    echo 0 > $1/$gpu
    # python3 /launcher.py /gem-schd /gem-pmgr $gpu $1/$gpu $2 --port $port 1>&2 &
    # pids="$pids $!"
    port=$(($port+1))
    gpu_list="$gpu"
done

port=60018

python3 /launcher_alnr.py /alnr $1  $gpu_list --port $port --sampling 1000  1>&2 &


wait
