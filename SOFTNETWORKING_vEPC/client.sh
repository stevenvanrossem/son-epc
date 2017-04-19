#!/bin/bash

#hss_mgmt=`sudo docker inspect hss_pp | jq '.[0].NetworkSettings.Networks.pratiksatapathyvepc_default.IPAddress' | sed 's/"//g'`
hss_mgmt="172.17.0.5"
hss_data=$hss_mgmt
#mme_mgmt=`sudo docker inspect mme_pp | jq '.[0].NetworkSettings.Networks.pratiksatapathyvepc_default.IPAddress' | sed 's/"//g'`
mme_mgmt="172.17.0.2"
mme_data=$mme_mgmt
#pgw_mgmt=`sudo docker inspect pgw_pp | jq '.[0].NetworkSettings.Networks.pratiksatapathyvepc_default.IPAddress' | sed 's/"//g'`
pgw_mgmt="172.17.0.3"
#sgw_mgmt=`sudo docker inspect sgw_pp | jq '.[0].NetworkSettings.Networks.pratiksatapathyvepc_default.IPAddress' | sed 's/"//g'`
sgw_mgmt="172.17.0.4"
sgw_data=$sgw_mgmt
#hss_host=`sudo docker inspect hss_pp | jq '.[0].Config.Hostname' | sed 's/"//g'`
#mme_host=`sudo docker inspect mme_pp | jq '.[0].Config.Hostname' | sed 's/"//g'`
#pgw_host=`sudo docker inspect pgw_pp | jq '.[0].Config.Hostname' | sed 's/"//g'`
#sgw_host=`sudo docker inspect sgw_pp | jq '.[0].Config.Hostname' | sed 's/"//g'`

hss_host="hss1"
mme_host="mme1"
pgw_host="pgw1"
sgw_host="sgw1"

ds_ip="172.17.0.5:8090"

sgw_s5_ip="10.30.1.2"
pgw_s5_ip="10.30.1.1"
mme_s1_ip="10.10.2.0"
sgw_s1_ip="10.10.1.2"
pgw_sgi_ip="10.30.3.1"
sink_ip="10.30.3.2"

echo "$hss_host: $hss_mgmt ($hss_data)"
echo "$mme_host: $mme_mgmt ($mme_data)"
echo "$sgw_host: $sgw_mgmt ($spgw_data)"
echo "$pgw_host: $pgw_mgmt ($spgw_data)"


args="--hss_mgmt $hss_mgmt --hss_data $hss_data"
args+=" --mme_mgmt $mme_mgmt --mme_data $mme_data"
args+=" --spgw_mgmt $sgw_mgmt --spgw_data $sgw_data"
args+=" --pgw_mgmt $pgw_mgmt --sgw_s5_ip $sgw_s5_ip --pgw_s5_ip $pgw_s5_ip --sink_ip $sink_ip --pp"
args+=" --hss_host $hss_host --mme_host $mme_host --spgw_host $sgw_host"
args+=" --mme_s1_ip $mme_s1_ip"
args+=" --spgw_s1_ip $sgw_s1_ip --spgw_sgi_ip $pgw_sgi_ip"
args+=" --ds_ip $ds_ip"
son-vm-client $args $@
