#!/usr/bin/env python3

"""
   saturate_membw.py

    Created on: Feb. 7, 2019
        Author: Taekyung Heo <tkheo@casys.kaist.ac.kr>
"""

import argparse
import numa
import os
import sys

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-membw", default="./membw/membw")
    parser.add_argument("-bandwidth", type=int, default=9999)
    parser.add_argument("-operation", default="nt-write")
    args = parser.parse_args()

    max_nid = numa.get_max_node()
    if max_nid != 1:
        print("This tool requires two sockets at least")
        sys.exit()

    cpus = numa.node_to_cpus(max_nid)
    for cpuid in cpus:
        cmd = "%s -c %d -b %d --%s &" % (args.membw, cpuid, args.bandwidth, args.operation)
        print(cmd)
        os.system(cmd)

if __name__ == '__main__':
    main()
