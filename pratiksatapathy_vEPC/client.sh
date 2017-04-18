hss_mgmt=`sudo docker inspect hss_pp | jq '.[0].NetworkSettings.Networks.sonepc_default.IPAddress' | sed 's/"//g'`
hss_data=$hss_mgmt
mme_mgmt=`sudo docker inspect mme_pp | jq '.[0].NetworkSettings.Networks.sonepc_default.IPAddress' | sed 's/"//g'`
mme_data=$mme_mgmt
pgw_mgmt=`sudo docker inspect pgw_pp | jq '.[0].NetworkSettings.Networks.sonepc_default.IPAddress' | sed 's/"//g'`
sgw_mgmt=`sudo docker inspect sgw_pp | jq '.[0].NetworkSettings.Networks.sonepc_default.IPAddress' | sed 's/"//g'`
spgw_data=$spgw_mgmt
hss_host=`sudo docker inspect hss | jq '.[0].Config.Hostname' | sed 's/"//g'`
mme_host=`sudo docker inspect mme | jq '.[0].Config.Hostname' | sed 's/"//g'`
spgw_host=`sudo docker inspect spgw | jq '.[0].Config.Hostname' | sed 's/"//g'`

echo "$hss_host: $hss_mgmt ($hss_data)"
echo "$mme_host: $mme_mgmt ($mme_data)"
echo "$sgw_host: $sgw_mgmt ($sgw_data)"
echo "$pgw_host: $pgw_mgmt ($pgw_data)"

args="--hss_mgmt $hss_mgmt --hss_data $hss_data"
args+=" --mme_mgmt $mme_mgmt --mme_data $mme_data"
args+=" --spgw_mgmt $spgw_mgmt --spgw_data $spgw_data"
args+=" --pgw_mgmt $pgw_mgmt --sgw_s5_ip $spgw_data --pgw_s5_ip $spgw_data --sink_ip $pgw_mgmt"
args+=" --hss_host $hss_host --mme_host $mme_host --spgw_host $spgw_host"
args+=" --mme_s1_ip $mme_data"
args+=" --spgw_s1_ip $spgw_data --spgw_sgi_ip $spgw_data"
son-vm-client $args $@
