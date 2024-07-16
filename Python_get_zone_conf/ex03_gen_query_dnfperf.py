#!/usr/bin/env python3

"""
Generate a query list for dnsperf/kxdpgun
"""

zone_prefix = 'example'
zone_suffix = 'com'

start_oct_3rd = 1
end_oct_3rd = 40
octet_1st_2nd = 172.29

zone_list = list()

for octet_3rd in range(start_oct_3rd, end_oct_3rd+1):
    for octet_4th in range(0,256):
        zone_list.append(f"{zone_prefix}{octet_3rd}-{octet_4th}.{zone_suffix}")

with open('query_list.txt', 'w') as f:
    for i in range(0,1000):
        for zone in zone_list:
            f.write(f"a{i}.{zone} a\n")
