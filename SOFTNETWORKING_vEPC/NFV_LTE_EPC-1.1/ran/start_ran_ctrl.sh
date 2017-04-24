#!/bin/bash

DURATION=$1

#clear any leftover tunnel from previous run
ip l del dev tun1

#start traffic
cd /home/steven/Documents/SONATA/vEPC/son-epc/SOFTNETWORKING_vEPC/NFV_LTE_EPC-1.1/ran/
./ransim_control.out --threads_count 1 --duration $DURATION --rate 0.1 --ran_ip_addr 10.10.1.1 --trafmon_ip_addr 10.10.1.1 --mme_ip_addr 10.10.0.2 --sgw_s1_ip_addr 10.10.1.2


