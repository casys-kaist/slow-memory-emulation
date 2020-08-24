#!/usr/bin/env python3

"""
   calibrate.py

    Created on: Feb. 20, 2019
        Author: Taekyung Heo <tkheo@casys.kaist.ac.kr>
"""

import argparse
import os
import subprocess

REG_OFFSET = 0x190 # DRAM power throttling register offset for Xeon E5 2630 v4
# It seems that 7f:17.0 and ff:17.0 are hidden from the extended PCIe configuration space
pci_id_dict = {
        0: [
                "7f:14.0", #System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Memory Controller 0 - Channel 0 Thermal Control (rev 01)
                "7f:14.1", #System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Memory Controller 0 - Channel 1 Thermal Control (rev 01)
                "7f:15.0", #System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Memory Controller 0 - Channel 2 Thermal Control (rev 01)
                "7f:15.1", #System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Memory Controller 0 - Channel 3 Thermal Control (rev 01)
                #"7f:17.0", #System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Memory Controller 1 - Channel 0 Thermal Control (rev 01)
            ],
        1: [
                "ff:14.0", #System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Memory Controller 0 - Channel 0 Thermal Control (rev 01)
                "ff:14.1", #System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Memory Controller 0 - Channel 1 Thermal Control (rev 01)
                "ff:15.0", #System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Memory Controller 0 - Channel 2 Thermal Control (rev 01)
                "ff:15.1", #System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Memory Controller 0 - Channel 3 Thermal Control (rev 01)
                #"ff:17.0", #System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Memory Controller 1 - Channel 0 Thermal Control (rev 01)
            ]
        }
MLC = "./mlc"

reg_val_li = [
                32783, 32798, 32813, 32828, 32843, 32858, 32873, 32888, 32903, 32918,
                32933, 32948, 32963, 32978, 32993, 33008, 33023, 33038, 33053, 33068,
                33083, 33098, 33113, 33128, 33143, 33158, 33173, 33188, 33203, 33218,
                33233, 33248, 33263, 33278, 33293, 33308, 33323, 33338, 33353, 33368,
                33383, 33398, 33413, 33428, 33443, 33458, 33473, 33488, 33503, 33518,
                33533, 33548, 33563, 33578, 33593
             ]

def throttle(node, reg_val):
    for pci_id in pci_id_dict[node]:
        cmd = "sudo setpci -s %s %s.l=%s" % (pci_id, hex(REG_OFFSET), hex(reg_val))
        print(cmd)
        os.system(cmd)

def get_idle_latency(nid):
    p = subprocess.Popen(MLC, stdout=subprocess.PIPE)
    stdout = ""
    while True:
        output = p.stdout.readline()
        if output == '' and p.poll() is not None:
            break
        if "Measuring Peak Injection Memory Bandwidths for the system" in output.decode("utf-8"):
            p.kill()
            break
        if output:
            stdout += output.decode("utf-8")
    splitted_stdout = stdout.split("\n")
    idle_latency = float(splitted_stdout[3+nid].split()[nid+1])
    return idle_latency

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-node", type=int, required=True)
    parser.add_argument("-target_idle_latency", type=float, required=True)
    args = parser.parse_args()

    # find the register value that meets the target idle latency
    for reg_val in reversed(reg_val_li):
        reg_val = reg_val + 0x30000 # base value
        throttle(args.node, reg_val)
        idle_latency = get_idle_latency(args.node)
        print("latency=%f" % (idle_latency))
        if idle_latency > args.target_idle_latency:
            result = "idle_latency=%f,reg=0x%x" % (idle_latency, reg_val)
            print(result)
            break

if __name__ == '__main__':
    main()
