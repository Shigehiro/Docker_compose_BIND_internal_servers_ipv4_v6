#!/usr/bin/env python3

zone_prefix = 'example'
zone_suffix = 'com'
number_of_zone = 1000

# Generate zone file
with open('com.zone.file.txt', 'w') as f:
    conf_string = """
$TTL 3600
@ IN SOA ns01 ns01 (
2010062303
1h
15m
30d
1h )
  IN NS ns01.com.
  IN NS ns02.com.

ns01 IN A 192.168.55.42
ns01 IN AAAA 2001:db8:1::42
ns02 IN A 192.168.55.43
ns02 IN AAAA 2001:db8:1::43
"""
    f.write(conf_string)

# Generate zone file
with open('com.zone.file.txt', 'a') as f:
    for i in range(0,number_of_zone):
        domain_number = str(f"{i:06}")
        name_conf_string = f"""
{zone_prefix}{domain_number}.{zone_suffix}. IN NS ns01.{zone_prefix}{domain_number}.{zone_suffix}.
{zone_prefix}{domain_number}.{zone_suffix}. IN NS ns02.{zone_prefix}{domain_number}.{zone_suffix}.
{zone_prefix}{domain_number}.{zone_suffix}. IN NS ns03.{zone_prefix}{domain_number}.{zone_suffix}.
{zone_prefix}{domain_number}.{zone_suffix}. IN NS ns04.{zone_prefix}{domain_number}.{zone_suffix}.
ns01.{zone_prefix}{domain_number}.{zone_suffix}. IN A 172.20.0.50
ns01.{zone_prefix}{domain_number}.{zone_suffix}. IN AAAA 2001:12a:1::50
ns02.{zone_prefix}{domain_number}.{zone_suffix}. IN A 172.20.0.51
ns02.{zone_prefix}{domain_number}.{zone_suffix}. IN AAAA 2001:12a:1::51
ns03.{zone_prefix}{domain_number}.{zone_suffix}. IN A 172.20.0.52
ns03.{zone_prefix}{domain_number}.{zone_suffix}. IN AAAA 2001:12a:1::52
ns04.{zone_prefix}{domain_number}.{zone_suffix}. IN A 172.20.0.53
ns04.{zone_prefix}{domain_number}.{zone_suffix}. IN AAAA 2001:12a:1::53

"""
        f.write(name_conf_string)

# Generate named.conf
with open('example.com_named.conf.txt', 'w') as f:
    conf_string = """
options {
  directory "/var/cache/bind";
  dnssec-validation false;
  allow-query { any; };
  recursion no;
  allow-recursion { none; };
  listen-on { any; };
  listen-on-v6 { any; };
  notify no;
};

zone  "." in {
        type hint;
        file "/var/lib/bind/named.ca";
        };

"""
    f.write(conf_string)

# Generate named.conf
with open('example.com_named.conf.txt', 'w') as f:
    for i in range(0,number_of_zone):
        domain_number = str(f"{i:06}")
        name_conf_string = f"""
zone "{zone_prefix}{domain_number}.{zone_suffix}" in {{
  type master;
  file "/var/lib/bind/example.com.template.db";
}};

"""
        f.write(name_conf_string)

print("run the following")
print("$ cp com.zone.file.txt ../bind_config/com/records/com.db")
print("$ cp example.com_named.conf.txt ../bind_config/example.com/config/named.conf")
print("$ docker compose restart")
