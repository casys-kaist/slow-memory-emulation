#!/usr/bin/env python3

"""
   throttle.py

    Created on: Feb. 20, 2019
        Author: Taekyung Heo <tkheo@casys.kaist.ac.kr>
"""

import argparse
import os

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

def throttle(node, reg_val):
    for pci_id in pci_id_dict[node]:
        cmd = "setpci -s %s %s.l=%s" % (pci_id, hex(REG_OFFSET), hex(reg_val))
        print(cmd)
        os.system(cmd)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-node", type=int, required=True)
    parser.add_argument("-cmd", default="emulate")
    parser.add_argument("-reg_val")
    args = parser.parse_args()

    if args.cmd == "emulate":
        reg_val = int(args.reg_val, 0)
    elif args.cmd == "reset":
        reg_val = 0x38fff

    throttle(args.node, reg_val)

if __name__ == '__main__':
    main()
