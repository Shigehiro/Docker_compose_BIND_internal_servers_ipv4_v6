#!/usr/bin/env python3

zone_prefix = 'example'
zone_suffix = 'com'

start_oct_3rd = 1
end_oct_3rd = 40
octet_1st_2nd = 172.29
com_ns01_ip = '172.29.0.62'
com_ns02_ip = '172.29.0.63'

# zone file for com
with open('com.zone.file.txt', 'w') as f:

    rr_string_head = f"""$TTL 3600
@ IN SOA ns01 ns01 (
2010062303
1h
15m
30d
1h )
  IN NS ns01.com.
  IN NS ns02.com.

ns01 IN A {com_ns01_ip}
ns02 IN A {com_ns02_ip}
"""
    f.write(f"{rr_string_head}")

    for octet_3rd in range(start_oct_3rd, end_oct_3rd+1):
        for octet_4th in range(0,256):
            zone_name = f"{zone_prefix}{octet_3rd}-{octet_4th}.{zone_suffix}"
            rr_string = f"""{zone_name}. IN NS ns01.{zone_name}.
ns01.{zone_name}. IN A {octet_1st_2nd}.{octet_3rd}.{octet_4th}
"""
            f.write(f"{rr_string}")

# name.conf for example[n].com
with open('example.com_named.conf.txt', 'w') as f:
    for octet_3rd in range(start_oct_3rd, end_oct_3rd+1):
        for octet_4th in range(0,256):
            zone_name = f"{zone_prefix}{octet_3rd}-{octet_4th}.{zone_suffix}"
            name_conf_string = f"""
zone "{zone_name}" in {{
  type master;
  file "/var/lib/bind/{zone_name}.template.db";
}};

"""
            f.write(name_conf_string)

# zone file for eample[n].com
    for octet_3rd in range(start_oct_3rd, end_oct_3rd+1):
        for octet_4th in range(0,256):
            zone_name = f"{zone_prefix}{octet_3rd}-{octet_4th}.{zone_suffix}"
            zone_file_name = f"{zone_name}.template.db"
            with open(zone_file_name, 'w') as f:
                rr_string_head = f"""$TTL 3600
@ IN SOA ns01 ns01 (
2010062303
1h
15m
30d
1h )
  IN NS ns01

ns01 IN A 192.168.113.44
* IN 300 A 127.0.0.1
"""
                f.write(rr_string_head)
                for i in range(1,100):
                    f.write(f"* IN 300 A 127.0.0.{i}\n")

print("run the following")
print("$ cp com.zone.file.txt ../bind_config_ex03/com/records/com.db")
print("$ cat example.com.named.conf.orig example.com_named.conf.txt > ../bind_config_ex03/example.com/config/named.conf")
print("$ mv ./*template* ../bind_config_ex03/example.com/records/")
print("$ rm -f ./com.zone.file.txt")
print("$ rm -f ./example.com_named.conf.txt")
print("$ docker compose restart")
