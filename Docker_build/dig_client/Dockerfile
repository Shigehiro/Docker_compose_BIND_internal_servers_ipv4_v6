FROM docker.io/ubuntu:24.04

ENV DEBIAN_FRONTEND noninteractive
WORKDIR /root
RUN apt-get update && apt-get install -y iproute2 bind9-dnsutils nftables --no-install-recommends && rm -f /etc/nftables.conf

ADD ./nftables.conf /etc/nftables.conf
ADD ./entrypoint.sh /usr/sbin/entrypoint.sh
RUN chmod u+x /usr/sbin/entrypoint.sh

EXPOSE 53/udp 53/tcp 953/tcp

ENTRYPOINT ["entrypoint.sh"]
