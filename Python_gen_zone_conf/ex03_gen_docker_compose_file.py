#!/usr/bin/env python3

"""
Gennerates docker-compose.yml for ex03
"""

start_oct_3rd = 1
end_oct_3rd = 40

# root, com

root_com = """services:
  bind-root01:
    container_name: bind-root01
    image: docker.io/ubuntu/bind9:latest
    volumes:
      - ./bind_config_ex03/root/config/named.conf:/etc/bind/named.conf:rw
      - ./bind_config_ex03/root/records/:/var/lib/bind:rw
    ports:
    - "172.29.0.60:53:53/udp"
    - "172.29.0.60:53:53/tcp"
  bind-root02:
    container_name: bind-root02
    image: docker.io/ubuntu/bind9:latest
    volumes:
      - ./bind_config_ex03/root/config/named.conf:/etc/bind/named.conf:rw
      - ./bind_config_ex03/root/records/:/var/lib/bind:rw
    ports:
    - "172.29.0.61:53:53/udp"
    - "172.29.0.61:53:53/tcp"
  bind-com01:
    container_name: bind-com01
    image: docker.io/ubuntu/bind9:latest
    volumes:
      - ./bind_config_ex03/com/config/named.conf:/etc/bind/named.conf:rw
      - ./bind_config_ex03/com/records/:/var/lib/bind:rw
    ports:
    - "172.29.0.62:53:53/udp"
    - "172.29.0.62:53:53/tcp"
  bind-com02:
    container_name: bind-com02
    image: docker.io/ubuntu/bind9:latest
    volumes:
      - ./bind_config_ex03/com/config/named.conf:/etc/bind/named.conf:rw
      - ./bind_config_ex03/com/records/:/var/lib/bind:rw
    ports:
    - "172.29.0.63:53:53/udp"
    - "172.29.0.63:53:53/tcp"
"""

# root, com
with open('ex03-docker-compose.yml', 'w') as f:
    f.write(root_com)

# example.com
    example_auth = """  bind-example-01:
    container_name: bind-example-01
    image: docker.io/ubuntu/bind9:latest
    volumes:
    - ./bind_config_ex03/example.com/config/named.conf:/etc/bind/named.conf:rw
    - ./bind_config_ex03/example.com/records/:/var/lib/bind:rw
    ports:
"""
    f.write(example_auth)

    for oct_3rd in range(start_oct_3rd, end_oct_3rd+1):
        for ip_4th in range(0,256):
            example_auth_ip = f"""    - "172.29.{oct_3rd}.{ip_4th}:53:53/udp"
    - "172.29.{oct_3rd}.{ip_4th}:53:53/tcp"
"""
            f.write(example_auth_ip)

# network
    podman_net = """networks:
  bind_internal_dns_ex03:
    driver: bridge
    enable_ipv6: false
    ipam:
      driver: default
      config:
        - subnet: 10.44.0.0/24
          gateway: 10.44.0.1
"""
    f.write(podman_net)