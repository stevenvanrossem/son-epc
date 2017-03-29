hss_mgmt=`sudo docker inspect hss | jq '.[0].NetworkSettings.Networks.sonepc_default.IPAddress' | sed 's/"//g'`
hss_data=$hss_mgmt/24
mme_mgmt=`sudo docker inspect mme | jq '.[0].NetworkSettings.Networks.sonepc_default.IPAddress' | sed 's/"//g'`
mme_data=$mme_mgmt/24
spgw_mgmt=`sudo docker inspect spgw | jq '.[0].NetworkSettings.Networks.sonepc_default.IPAddress' | sed 's/"//g'`
spgw_data=$spgw_mgmt/24
hss_host=`sudo docker inspect hss | jq '.[0].Config.Hostname' | sed 's/"//g'`
mme_host=`sudo docker inspect mme | jq '.[0].Config.Hostname' | sed 's/"//g'`
spgw_host=`sudo docker inspect spgw | jq '.[0].Config.Hostname' | sed 's/"//g'`

echo "$hss_host: $hss_mgmt ($hss_data)"
echo "$mme_host: $mme_mgmt ($mme_data)"
echo "$spgw_host: $spgw_mgmt ($spgw_data)"

son-vm-client --hss_mgmt $hss_mgmt --hss_data $hss_data --mme_mgmt $mme_mgmt --mme_data $mme_data --spgw_mgmt $spgw_mgmt --spgw_data $spgw_data --hss_host $hss_host --mme_host $mme_host --spgw_host $spgw_host $@
