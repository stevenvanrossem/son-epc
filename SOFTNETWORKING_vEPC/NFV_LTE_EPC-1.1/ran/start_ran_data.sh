#!/bin/bash
set -e 

RATE=$1

#clear any leftover tunnel from previous run
#ip l del dev tun1

#start traffic
cd /home/steven/Documents/SONATA/vEPC/son-epc/SOFTNETWORKING_vEPC/NFV_LTE_EPC-1.1/ran/
#PING_RATE=$(bc -l <<< "1/$RATE")
PING_RATE=$1
echo $PING_RATE
ping -I 172.16.1.3 172.16.0.2 -i$PING_RATE 



