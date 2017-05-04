#!/bin/bash

pkill -f ransim_wait.out
ip l del dev tun1
cd /home/steven/Documents/SONATA/vEPC/son-epc/SOFTNETWORKING_vEPC/
bash client.sh --stop > /dev/null
#sleep 1
bash client.sh > /dev/null
cd /home/steven/Documents/SONATA/vEPC/son-epc/SOFTNETWORKING_vEPC/NFV_LTE_EPC-1.1/ran/
./ransim_wait.out --threads_count 1 --duration 100 --rate 0.1 --ran_ip_addr 10.10.1.1 --trafmon_ip_addr 10.10.1.1 --mme_ip_addr 10.10.0.2 --sgw_s1_ip_addr 10.10.1.2&
#cpulimit -l80 -p$!
sleep 5

