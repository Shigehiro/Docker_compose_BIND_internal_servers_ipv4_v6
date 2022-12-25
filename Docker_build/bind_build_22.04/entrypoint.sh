#!/bin/sh

#/usr/sbin/nft -f /etc/nftables.conf
/usr/sbin/named -g -c /etc/bind/named.conf -u bind -4 -6 -d 1
