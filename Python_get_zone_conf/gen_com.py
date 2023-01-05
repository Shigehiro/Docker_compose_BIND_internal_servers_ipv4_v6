#!/usr/bin/env python3

zone_prefix = 'example'
zone_suffix = 'com'
number_of_zone = 100000

with open('com.zone.file.txt', 'w') as f:
    for i in range(0,number_of_zone-1):
        name_conf_string = f"""
{zone_prefix}{i}.{zone_suffix}. IN NS ns01.{zone_prefix}{i}.{zone_suffix}.
{zone_prefix}{i}.{zone_suffix}. IN NS ns02.{zone_prefix}{i}.{zone_suffix}.
{zone_prefix}{i}.{zone_suffix}. IN NS ns03.{zone_prefix}{i}.{zone_suffix}.
{zone_prefix}{i}.{zone_suffix}. IN NS ns04.{zone_prefix}{i}.{zone_suffix}.
ns01.{zone_prefix}{i}.{zone_suffix}. IN A 172.20.0.50
ns01.{zone_prefix}{i}.{zone_suffix}. IN AAAA 2001:12a:1::50
ns02.{zone_prefix}{i}.{zone_suffix}. IN A 172.20.0.51
ns02.{zone_prefix}{i}.{zone_suffix}. IN AAAA 2001:12a:1::51
ns03.{zone_prefix}{i}.{zone_suffix}. IN A 172.20.0.52
ns03.{zone_prefix}{i}.{zone_suffix}. IN AAAA 2001:12a:1::52
ns04.{zone_prefix}{i}.{zone_suffix}. IN A 172.20.0.53
ns04.{zone_prefix}{i}.{zone_suffix}. IN AAAA 2001:12a:1::53
"""
        f.write(name_conf_string)

with open('example.com_named.conf.txt', 'w') as f:
    for i in range(0,number_of_zone-1):
        name_conf_string = f"""
zone "{zone_prefix}{i}.{zone_suffix}" in {{
  type master;
  file "/var/lib/bind/example.com.template.db";
}};

"""
        f.write(name_conf_string)

print("run the following")
print("$ cat com.db.orig com.zone.file.txt > ../bind_config/com/records/com.db")
print("$ cat example.com.named.conf.orig example.com_named.conf.txt > ../bind_config/example.com/config/named.conf")
print("$ docker compose restart")
