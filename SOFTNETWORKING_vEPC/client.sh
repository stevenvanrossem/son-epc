#!/bin/bash


mme_host="mme1"
mme_mgmt="172.17.0.2"
mme_s11="10.30.3.2" 
mme_s1="10.10.0.2"

hss_host="hss1"
hss_mgmt="172.17.0.5"
hss_s6a="10.30.1.1" 

sgw_host="sgw1"
sgw_mgmt="172.17.0.4"
sgw_s11="10.30.3.1" 
sgw_s1="10.10.1.2"
sgw_s5="10.30.5.2"

pgw_host="pgw1"
pgw_mgmt="172.17.0.3"
pgw_s5="10.30.5.1"
pgw_sgi="10.30.7.1"

ds_ip="172.17.0.5"

sink_ip="10.30.7.2"

trafmon_ip="10.10.1.1" #SAP ip of the S1-U

args="--hss_mgmt $hss_mgmt --hss_data $hss_s6a"
args+=" --mme_mgmt $mme_mgmt --mme_data $mme_s11 --mme_s1_ip $mme_s1"
args+=" --spgw_mgmt $sgw_mgmt --spgw_data $sgw_s11 --spgw_s1_ip $sgw_s1 --sgw_s5_ip $sgw_s5"
args+=" --pgw_mgmt $pgw_mgmt --spgw_sgi_ip $pgw_sgi --pgw_s5_ip $pgw_s5 "
args+=" --hss_host $hss_host --mme_host $mme_host --spgw_host $sgw_host"
args+=" --ds_ip $ds_ip --sink_ip $sink_ip --pp --trafmon_ip=$trafmon_ip"
son-vm-client $args $@
