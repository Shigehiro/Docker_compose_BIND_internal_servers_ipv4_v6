#!/usr/bin/env python3

mac_addr = '52:54:00:96:79:b6'
start_oct_3rd = 1
end_oct_3rd = 40
octet_1st_2nd = '172.29'
target_device = 'eth0'

with open('ex03_ip_neigh_add.sh', 'w') as f:
    f.write("#!/bin/sh\n")
    for octet_3rd in range(start_oct_3rd, end_oct_3rd+1):
        for octet_4th in range(0,256):
            f.write(f"ip neigh add {octet_1st_2nd}.{octet_3rd}.{octet_4th} dev {target_device} lladdr {mac_addr}\n")
