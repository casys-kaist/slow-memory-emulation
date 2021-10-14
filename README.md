# Slow Memory Emulation
* This tool lets you emulate slow memory with memory bandwidth saturation and throttling.
* By slowing down the memory performance of one node in a two-socket system, it emulates
a heterogeneous memory system. Therefore, this tool assumes a two-socket system.
Otherwise, it will not work as expected.
* Memory bandwidth throttling is a widely used technique to lower the performance
of a memory system. However, throttling memory bandwidth may not slowdown a workload's
performance if the memory bandwidth usage of the workload is lower than the throttled
memory bandwidth. Therefore, in addition to memory bandwidth throttling, memory bandwidth
saturation is used.
* We borrow the core mechanism of memory bandwidth throttling from [Quartz](https://github.com/HewlettPackard/quartz).
Quartz writes a specific to a designated address (0x190 in the example below)
to throttle the memory bandwidth.

## How to Use
* First, choose the target idle latency that you want (300ns).
* Second, find the proper memory bandwidth throttling value to emulate the idle latency.
```
$ ./calibrate.sh 300
for dir in membw/ ; do \
        make -C  $dir ; \
done
make[1]: Entering directory '/home/tkheo/slow-memory-emulation-/membw'
cc -Wall -Winline -msse4.2 -O3 -g -mtune=native -march=native    membw.c   -o membw
make[1]: Leaving directory '/home/tkheo/slow-memory-emulation/membw'
./membw/membw -c 10 -b 9999 --nt-write &
./membw/membw -c 11 -b 9999 --nt-write &
- THREAD logical core id: 10,  memory bandwidth [MB]: 9999, starting...
./membw/membw -c 12 -b 9999 --nt-write &
- THREAD logical core id: 11,  memory bandwidth [MB]: 9999, starting...
./membw/membw -c 13 -b 9999 --nt-write &
- THREAD logical core id: 12,  memory bandwidth [MB]: 9999, starting...
./membw/membw -c 14 -b 9999 --nt-write &
- THREAD logical core id: 13,  memory bandwidth [MB]: 9999, starting...
./membw/membw -c 15 -b 9999 --nt-write &
- THREAD logical core id: 14,  memory bandwidth [MB]: 9999, starting...
./membw/membw -c 16 -b 9999 --nt-write &
- THREAD logical core id: 15,  memory bandwidth [MB]: 9999, starting...
./membw/membw -c 17 -b 9999 --nt-write &
- THREAD logical core id: 16,  memory bandwidth [MB]: 9999, starting...
./membw/membw -c 18 -b 9999 --nt-write &
- THREAD logical core id: 17,  memory bandwidth [MB]: 9999, starting...
./membw/membw -c 19 -b 9999 --nt-write &
- THREAD logical core id: 18,  memory bandwidth [MB]: 9999, starting...
- THREAD logical core id: 19,  memory bandwidth [MB]: 9999, starting...
sudo setpci -s ff:14.0 0x190.l=0x38339
sudo setpci -s ff:14.1 0x190.l=0x38339
sudo setpci -s ff:15.0 0x190.l=0x38339
sudo setpci -s ff:15.1 0x190.l=0x38339
latency=193.100000
...
sudo setpci -s ff:14.0 0x190.l=0x38186
sudo setpci -s ff:14.1 0x190.l=0x38186
sudo setpci -s ff:15.0 0x190.l=0x38186
sudo setpci -s ff:15.1 0x190.l=0x38186
latency=298.700000
sudo setpci -s ff:14.0 0x190.l=0x38177
sudo setpci -s ff:14.1 0x190.l=0x38177
sudo setpci -s ff:15.0 0x190.l=0x38177
sudo setpci -s ff:15.1 0x190.l=0x38177
latency=313.000000
idle_latency=313.000000,reg=0x38177
```
* Third, emulate slow memory.
```
$ ./emulate.sh 0x38186
```
* You can reset slow memory emulation with the following command.
```
$ ./reset.sh
```

## References
* [Intel® Xeon® Processor E5 v4 Product Family Datasheet, Volume Two: Registers](https://en.wikichip.org/w/images/2/24/Intel_Xeon_Processor_E5_v4_Product_Family_Datasheet_Volume_2-_Registers.pdf)
* [Quartz: A DRAM-based performance emulator for NVM](https://github.com/HewlettPackard/quartz)
* [intel/intel-cmt-cat: membw](https://github.com/intel/intel-cmt-cat/tree/master/tools/membw)
