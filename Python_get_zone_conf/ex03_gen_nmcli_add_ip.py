#!/usr/bin/env python3

ip_3rd_start = 1
ip_3rd_end = 40
ip_prefix = '172.29'

with open('ex03_add_ip_nmcli.sh', 'w' ) as f:
  f.write("#!/bin/sh\n")
  # ip addresses for two root, two com servers
  for i in range(60,64):
      f.write(f"nmcli con mod Wired\\ connection\\ 1 +ipv4.addresses {ip_prefix}.0.{i}/16\n")
  # ip addresses for example[n].com
  for octet_3rd in range(ip_3rd_start, ip_3rd_end + 1):          
      for ip_last in range(0,256):
          f.write(f"nmcli con mod Wired\\ connection\\ 1 +ipv4.addresses {ip_prefix}.{octet_3rd}.{ip_last}/16\n")
