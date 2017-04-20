#!/bin/sh
cd /root/NFV_LTE_EPC/NFV_LTE_EPC-1.1/scripts/setup_ds/
bash run_server.sh 0.0.0.0:8090 &
sleep 30
cd /root/NFV_LTE_EPC/NFV_LTE_EPC-1.1/scripts/setup_hss/
bash load_data.sh
cd /root
son-vm-server -v -c /root/son-epc/configs/server.conf.hss

