# 1. Set up internal root server, .com, example[N].com DNS(BIND) Servers with Docker Compose

- [1. Set up internal root server, .com, example\[N\].com DNS(BIND) Servers with Docker Compose](#1-set-up-internal-root-server-com-examplencom-dnsbind-servers-with-docker-compose)
- [2. Description](#2-description)
- [3. How to use](#3-how-to-use)
  - [3.1. Enable IPv6 on Docker host](#31-enable-ipv6-on-docker-host)
  - [3.2. Docker comopse IPv6 setting](#32-docker-comopse-ipv6-setting)
  - [3.3. Prepare zone files](#33-prepare-zone-files)
  - [3.4. Launch containers](#34-launch-containers)
  - [3.5. Confirm](#35-confirm)
- [4. Small tips](#4-small-tips)
  - [4.1. How to change containers IP, IP addresses in zone files](#41-how-to-change-containers-ip-ip-addresses-in-zone-files)

# 2. Description

- This compose file launchs two internal root DNS, two .com, four example[N].com BIND containers.
- As for example[N].com zones, you can generate multiple example zones(example0.com, example1.com ..) files with a python script located at Python_get_zone_conf directory.
- This compose launchs a `dig client` container and a `BIND Cache` container as well for the testing

# 3. How to use

## 3.1. Enable IPv6 on Docker host

- Reference
  - [enable IPv6 on docker](https://docs.docker.com/config/daemon/ipv6/)

```text
$ cat /etc/docker/daemon.json
{
  "ipv6": true,
  "fixed-cidr-v6": "2001:ec8:1::/64"
}
```

```text
$ sudo systemctl restart docker.service
```

You will see an IPv6 on docker0.
```
$ ip a s docker0 |grep inet
    inet 172.17.0.1/16 brd 172.17.255.255 scope global docker0
    inet6 2001:ec8:1::1/64 scope global tentative
    inet6 fe80::1/64 scope link tentative
```
    
## 3.2. Docker comopse IPv6 setting

- enable ipv6
```
$ grep ^networks docker-compose.yml -A10
networks:
  bind_internal_dns:
    driver: bridge
    enable_ipv6: true
    ipam:
      driver: default
      config:
        - subnet: 172.20.0.0/24
          gateway: 172.20.0.1
        - subnet: 2001:12a:1::/64
          gateway: 2001:12a:1::1
```

- when you want to expose IPv6, embrace IPv6 addresses with brackets as below.
```
    networks:
      bind_internal_dns:
        ipv4_address: 172.20.0.11
        ipv6_address: 2001:12a:1::11
    ports:
      - '127.0.0.1:5355:53/tcp'
      - '127.0.0.1:5355:53/udp'
      - '[::1]:5355:53/tcp'
      - '[::1]:5355:53/udp'
```

## 3.3. Prepare zone files

```text
$ cd Python_get_zone_conf
```

specify number of zones you would like to generate.
```text
$ grep ^number_of_zone gen_com.py
number_of_zone = 100000
```

run the script
```text
$ ./gen_com.py
run the following
cat com.db.orig com.zone.file.txt > ../bind_config/com/records/com.db
cat example.com.named.conf.orig example.com_named.conf.txt > ../bind_config/example.com/config/named.conf
docker compose restart
```

```text
cat com.db.orig com.zone.file.txt > ../bind_config/com/records/com.db
cat example.com.named.conf.orig example.com_named.conf.txt > ../bind_config/example.com/config/named.conf
```

## 3.4. Launch containers

```text
$ docker compose build
$ docker-compose up -d
```

## 3.5. Confirm

confirm all BIND containers load zone files.
```text
$ docker exec bind-com01 rndc status | grep ^number
number of zones: 2 (0 automatic)

$ docker exec bind-example01 rndc status | grep ^number
number of zones: 100000 (0 automatic)
```

send DNS queris from the dig-client container to Auth servers.
```text
$ docker exec -it dig-client bash
root@72e5f4891c5c:~#

root@72e5f4891c5c:~# ip a s eth0|grep inet|grep -v fe80
    inet 172.20.0.5/24 brd 172.20.0.255 scope global eth0
    inet6 2001:12a:1::5/64 scope global nodad

# dig to the root server
root@72e5f4891c5c:~# dig @172.20.0.30 a.example9999.com +norec

; <<>> DiG 9.18.1-1ubuntu1.2-Ubuntu <<>> @172.20.0.30 a.example9999.com +norec
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 31207
;; flags: qr; QUERY: 1, ANSWER: 0, AUTHORITY: 2, ADDITIONAL: 5

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1232
; COOKIE: af7cc40cb0d6b4ea0100000063a8834dc9020d3836ac42e8 (good)
;; QUESTION SECTION:
;a.example9999.com.             IN      A

;; AUTHORITY SECTION:
com.                    3600    IN      NS      ns02.com.
com.                    3600    IN      NS      ns01.com.

;; ADDITIONAL SECTION:
ns02.com.               3600    IN      A       172.20.0.41
ns01.com.               3600    IN      A       172.20.0.40
ns02.com.               3600    IN      AAAA    2001:12a:1::41
ns01.com.               3600    IN      AAAA    2001:12a:1::40

# dig to com
root@72e5f4891c5c:~# dig @172.20.0.40 a.example9999.com +norec

; <<>> DiG 9.18.1-1ubuntu1.2-Ubuntu <<>> @172.20.0.40 a.example9999.com +norec
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 6867
;; flags: qr; QUERY: 1, ANSWER: 0, AUTHORITY: 4, ADDITIONAL: 9

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1232
; COOKIE: d4515e28a83f2b9b0100000063a8836a95128f9193bf1115 (good)
;; QUESTION SECTION:
;a.example9999.com.             IN      A

;; AUTHORITY SECTION:
example9999.com.        3600    IN      NS      ns02.example9999.com.
example9999.com.        3600    IN      NS      ns01.example9999.com.
example9999.com.        3600    IN      NS      ns04.example9999.com.
example9999.com.        3600    IN      NS      ns03.example9999.com.

;; ADDITIONAL SECTION:
ns04.example9999.com.   3600    IN      A       172.20.0.53
ns03.example9999.com.   3600    IN      A       172.20.0.52
ns02.example9999.com.   3600    IN      A       172.20.0.51
ns01.example9999.com.   3600    IN      A       172.20.0.50
ns04.example9999.com.   3600    IN      AAAA    2001:12a:1::53
ns03.example9999.com.   3600    IN      AAAA    2001:12a:1::53
ns02.example9999.com.   3600    IN      AAAA    2001:12a:1::51
ns01.example9999.com.   3600    IN      AAAA    2001:12a:1::50

# dig to example9999.com
root@95454668710e:~# dig @172.20.0.50 a.example9999.com +norec

; <<>> DiG 9.18.1-1ubuntu1.2-Ubuntu <<>> @172.20.0.50 a.example9999.com +norec
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 7075
;; flags: qr aa; QUERY: 1, ANSWER: 1, AUTHORITY: 4, ADDITIONAL: 9

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1232
; COOKIE: abca25b3d2932cf10100000063a88546112c7d3b7b472a4d (good)
;; QUESTION SECTION:
;a.example9999.com.             IN      A

;; ANSWER SECTION:
a.example9999.com.      300     IN      A       127.0.0.1

;; AUTHORITY SECTION:
example9999.com.        3600    IN      NS      ns02.example9999.com.
example9999.com.        3600    IN      NS      ns01.example9999.com.
example9999.com.        3600    IN      NS      ns04.example9999.com.
example9999.com.        3600    IN      NS      ns03.example9999.com.

;; ADDITIONAL SECTION:
ns01.example9999.com.   3600    IN      A       172.20.0.50
ns02.example9999.com.   3600    IN      A       172.20.0.51
ns03.example9999.com.   3600    IN      A       172.20.0.52
ns04.example9999.com.   3600    IN      A       172.20.0.53
ns01.example9999.com.   3600    IN      AAAA    2001:12a:1::50
ns02.example9999.com.   3600    IN      AAAA    2001:12a:1::51
ns03.example9999.com.   3600    IN      AAAA    2001:12a:1::52
ns04.example9999.com.   3600    IN      AAAA    2001:12a:1::53
```

send DNS queries from the dig-client to the BIND Cache container.
```text
# ipv4
$ docker exec dig-client dig @172.20.0.10 a.example1000.com aaaa +short -4
1111:1111:1111:1111::1111

# ipv6
$ docker exec dig-client dig @2001:12a:1::10 a.example1111.com aaaa +short -6
1111:1111:1111:1111::1111
```

# 4. Small tips

## 4.1. How to change containers IP, IP addresses in zone files

By default, docker containers will use the following IPs.
```text
$ grep ^networks docker-compose.yml -A10
networks:
  bind_internal_dns:
    driver: bridge
    enable_ipv6: true
    ipam:
      driver: default
      config:
        - subnet: 172.20.0.0/24
          gateway: 172.20.0.1
        - subnet: 2001:12a:1::/64
          gateway: 2001:12a:1::1
```

If you would like to change the IPv4 address range from 172.20.0.0/24 to 172.20.30.0/24,
edit the file as below.
```text
$ grep 172.20 -r ./* | awk -F':' '{print $1}' | sort -u |grep -v README
./bind_config/cache/records/named.ca
./bind_config/com/records/com.db
./bind_config/com/records/named.ca
./bind_config/example.com/records/example.com.template.db
./bind_config/example.com/records/named.ca
./bind_config/root/records/root.db
./Docker_build/cacheserve_build/cs.conf
./docker-compose.yml
./Python_get_zone_conf/com.db.orig
./Python_get_zone_conf/gen_com.py
```

```text
$ grep 172.20 -r ./* | awk -F':' '{print $1}' | sort -u |grep -v README | xargs -I{} sed s/172.20.0/172.20.30/g -i {}
```