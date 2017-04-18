#hss_mgmt=`sudo docker inspect hss | jq '.[0].NetworkSettings.Networks.sonepc_default.IPAddress' | sed 's/"//g'`
hss_mgmt='172.17.0.5'
#hss_mgmt='10.20.0.1'
hss_data=$hss_mgmt/24

#mme_mgmt=`sudo docker inspect mme | jq '.[0].NetworkSettings.Networks.sonepc_default.IPAddress' | sed 's/"//g'`
mme_mgmt='172.17.0.4'
#mme_mgmt='10.20.0.2'
mme_data=$mme_mgmt/24

#spgw_mgmt=`sudo docker inspect spgw | jq '.[0].NetworkSettings.Networks.sonepc_default.IPAddress' | sed 's/"//g'`
spgw_mgmt='172.17.0.6'
#spgw_mgmt='10.20.0.3'
spgw_data=$spgw_mgmt/24

#hss_host=`sudo docker inspect hss | jq '.[0].Config.Hostname' | sed 's/"//g'`
hss_host='hss1'
#mme_host=`sudo docker inspect mme | jq '.[0].Config.Hostname' | sed 's/"//g'`
mme_host='mme1'
#spgw_host=`sudo docker inspect spgw | jq '.[0].Config.Hostname' | sed 's/"//g'`
spgw_host='spgw1'

echo "$hss_host: $hss_mgmt ($hss_data)"
echo "$mme_host: $mme_mgmt ($mme_data)"
echo "$spgw_host: $spgw_mgmt ($spgw_data)"

mme_s1_ip='10.10.0.2/30'
spgw_s1_ip='10.10.1.2/30'
spgw_sgi_ip='10.10.2.2/30'
#mme_s1_ip=$mme_data
#spgw_s1_ip=$spgw_data
#spgw_sgi_ip=$spgw_data

args="--hss_mgmt $hss_mgmt --hss_data $hss_data"
args+=" --mme_mgmt $mme_mgmt --mme_data $mme_data"
args+=" --spgw_mgmt $spgw_mgmt --spgw_data $spgw_data"
args+=" --hss_host $hss_host --mme_host $mme_host --spgw_host $spgw_host"
args+=" --mme_s1_ip $mme_s1_ip"
args+=" --spgw_s1_ip $spgw_s1_ip --spgw_sgi_ip $spgw_sgi_ip"
son-vm-client $args $@
