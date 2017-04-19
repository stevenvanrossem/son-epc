/root/NFV_LTE_EPC/NFV_LTE_EPC-1.1/scripts/setup_ds/run_server.sh 0.0.0.0:8090&
pushd /root/NFV_LTE_EPC/NFV_LTE_EPC-1.1/scripts/setup_hss/
/root/NFV_LTE_EPC/NFV_LTE_EPC-1.1/scripts/setup_hss/load_data.sh
popd
son-vm-server -v -c /root/son-epc/pratiksatapathy_vEPC/server.conf.hss
