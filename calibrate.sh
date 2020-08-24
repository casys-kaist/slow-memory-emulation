if [ $# -eq 0 ]
then
	echo "usage: $0 <target idle latency>"
	exit
fi

make
sudo modprobe msr
pkill membw
python3 saturate_membw.py
pkill mlc
sudo python3 calibrate.py -node 1 -target_idle_latency $1
