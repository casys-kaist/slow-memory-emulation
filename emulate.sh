make
sudo modprobe msr
pkill membw
python3 saturate_membw.py
sudo python3 throttle.py -node 1 -cmd emulate -reg_val $1
