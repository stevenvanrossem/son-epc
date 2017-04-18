from son.client.protocol import ClientFactory
from twisted.internet import reactor

import argparse
import logging
import sys

class Client(object):

    def __init__(self, hss_mgmt, mme_mgmt, spgw_mgmt,
                 hss_data, mme_data, spgw_data,
                 hss_host, mme_host, spgw_host,
                 mme_s1_ip, spgw_s1_ip, spgw_sgi_ip,
                 pgw_s5_ip = None, sgw_s5_ip = None,
                 sink_ip = None, pgw_mgmt = None,
                 isPp = False):
        self.hss_mgmt = hss_mgmt
        self.mme_mgmt = mme_mgmt
        self.spgw_mgmt = spgw_mgmt
        self.hss_data = hss_data
        self.mme_data = mme_data
        self.spgw_data = spgw_data
        self.hss_host = hss_host
        self.mme_host = mme_host
        self.spgw_host = spgw_host
        self.mme_s1_ip = mme_s1_ip
        self.spgw_s1_ip = spgw_s1_ip
        self.spgw_sgi_ip = spgw_sgi_ip
        self.pgw_s5_ip = pgw_s5_ip
        self.sgw_s5_ip = sgw_s5_ip
        self.sink_ip = sink_ip
        self.pgw_mgmt = pgw_mgmt
        self.isPp = isPp
        self._init_configs()

    def _init_connection(self, isStopping = False):
        if self.isPp:
            self.factory = ClientFactory([
                (self.hss_mgmt, self.hss_config),
                (self.mme_mgmt, self.mme_config),
                (self.spgw_mgmt, self.sgw_config),
                (self.pgw_mgmt, self.pgw_config)
            ], isStopping = isStopping)
        else:
            self.factory = ClientFactory([
                (self.hss_mgmt, self.hss_config),
                (self.mme_mgmt, self.mme_config),
                (self.spgw_mgmt, self.spgw_config)
            ], isStopping = isStopping)

    def _init_configs(self):
        self.hosts = {
            'hss': {
                'host_name': '%s.openair4G.eur' % self.hss_host,
                'ip': self.hss_data
            },
            'mme': {
                'host_name': '%s.openair4G.eur' % self.mme_host,
                'ip': self.mme_data
            },
            'spgw': {
                'host_name': '%s.openair4G.eur' % self.spgw_host,
                'ip': self.spgw_data
            }
        }
        self._init_hss_config()
        self._init_mme_config()
        self._init_spgw_config()

    def _init_hss_config(self):
        if self.isPp:
            self.hss_config = {
                'threads_count': '2',
                'ip': self.hss_data,
            }
        else:
            self.hss_config = {
                'hosts': self.hosts,
                'mysql': {
                    'user': 'root',
                    'pass': 'hurka'
                }
            }

    def _init_mme_config(self):
        if self.isPp:
            self.mme_config = {
                'threads_count': '2',
                'hss_ip': self.hss_data,
                'sgw_s1_ip': self.spgw_s1_ip,
                'sgw_s11_ip': self.spgw_data,
                'sgw_s5_ip': self.sgw_s5_ip,
                'pgw_s5_ip': self.pgw_s5_ip
            }
        else:
            self.mme_config = {
                'hosts': self.hosts,
                's1_ip': self.mme_s1_ip
            }

    def _init_spgw_config(self):
        if self.isPp:
            self.pgw_config = {
                's5_threads_count': '2',
                'sgi_threads_count': '2',
                'sgw_s5_ip': self.sgw_s5_ip,
                'pgw_s5_ip': self.pgw_s5_ip,
                'pgw_sgi_ip': self.spgw_sgi_ip,
                'sink_ip_addr': self.sink_ip
            }
            self.sgw_config = {
                's11_threads_count': '2',
                's1_threads_count': '2',
                's5_threads_count': '2',
                'sgw_s11_ip_addr': self.spgw_data,
                'sgw_s1_ip_addr': self.spgw_s1_ip,
                'sgw_s5_ip_addr': self.sgw_s5_ip,
                'pgw_s5_ip_addr': self.pgw_s5_ip
            }
        else:
            self.spgw_config = {
                'hosts': self.hosts,
                'sgi_ip': self.spgw_sgi_ip,
                's1u_ip': self.spgw_s1_ip
            }

    def start(self):
        self._init_connection()
        reactor.run()

    def stop(self):
        self._init_connection(isStopping = True)
        reactor.run()


def parseConfigArgs(argv):
    configArguments = argparse.ArgumentParser()
    configArguments.add_argument('--hss_mgmt', required=True,
                                 help='Management address for HSS')
    configArguments.add_argument('--hss_data', required=True,
                                 help='Data plane address for HSS')
    configArguments.add_argument('--hss_host', required=True,
                                 help='Hostname for HSS')
    configArguments.add_argument('--mme_mgmt', required=True,
                                 help='Management address for MME')
    configArguments.add_argument('--mme_data', required=True,
                                 help='Data plane address for MME')
    configArguments.add_argument('--mme_host', required=True,
                                 help='Hostname for MME')
    configArguments.add_argument('--spgw_mgmt', required=True,
                                 help='Management address for SPGW')
    configArguments.add_argument('--spgw_data', required=True,
                                 help='Data plane address for SPGW')
    configArguments.add_argument('--spgw_host', required=True,
                                 help='Hostname for SPGW')
    return configArguments.parse_args(argv)

def parseNetworkArgs(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--mme_s1_ip', required=True,
                                 help='Public IP of MME')
    parser.add_argument('--spgw_s1_ip', required=True,
                                 help='Public IP of SPGW')
    parser.add_argument('--spgw_sgi_ip', required=True,
                                 help='External IP of SPGW')
    return parser.parse_known_args(argv)

def parseScenarioSelection(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--oai', action='store_true', dest='oai',
                        default=False, help='OpenAirInterface')
    parser.add_argument('--pp', action='store_true', dest='pp',
                        default=False, help='Pratik Satapathy')
    parser.add_argument('--sgw_s5_ip', required=False,
                        help='S5 IP of SGW')
    parser.add_argument('--pgw_s5_ip', required=False,
                        help='S5 IP of PGW')
    parser.add_argument('--sink_ip', required=False,
                        help='IP of sink')
    parser.add_argument('--pgw_mgmt', required=False,
                        help='Management IP of PGW')
    return parser.parse_known_args(argv)

def parseGeneralArgs(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose','-v', action='store_true', dest='verbose',
                        default=False, help='Verbose')
    parser.add_argument('--stop','-s', action='store_true', dest='stop',
                        default=False, help='Verbose')
    return parser.parse_known_args(argv)


def main(argv = sys.argv[1:]):
    generalArgs, remaining_argv = parseGeneralArgs(argv)
    networkArgs, remaining_argv = parseNetworkArgs(remaining_argv)
    scenarioArgs, remaining_argv = parseScenarioSelection(remaining_argv)
    configArgs = parseConfigArgs(remaining_argv)

    if generalArgs.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    logger.info('Got cli parameters:')
    configDict = vars(configArgs)
    for param in configDict:
        logger.info('%s -> %s', param, configDict[param])

    if scenarioArgs.oai:
        c = Client(hss_mgmt = configArgs.hss_mgmt, hss_data = configArgs.hss_data,
                mme_mgmt = configArgs.mme_mgmt, mme_data = configArgs.mme_data,
                spgw_mgmt = configArgs.spgw_mgmt, spgw_data = configArgs.spgw_data,
                hss_host = configArgs.hss_host, mme_host = configArgs.mme_host,
                spgw_host = configArgs.spgw_host,
                mme_s1_ip = networkArgs.mme_s1_ip,
                spgw_s1_ip = networkArgs.spgw_s1_ip,
                spgw_sgi_ip = networkArgs.spgw_sgi_ip)
    elif scenarioArgs.pp and \
        scenarioArgs.sgw_s5_ip is not None and \
        scenarioArgs.pgw_s5_ip is not None and \
        scenarioArgs.pgw_mgmt is not None and \
        scenarioArgs.sink_ip is not None:
        c = Client(hss_mgmt = configArgs.hss_mgmt, hss_data = configArgs.hss_data,
                mme_mgmt = configArgs.mme_mgmt, mme_data = configArgs.mme_data,
                spgw_mgmt = configArgs.spgw_mgmt, spgw_data = configArgs.spgw_data,
                hss_host = configArgs.hss_host, mme_host = configArgs.mme_host,
                spgw_host = configArgs.spgw_host,
                mme_s1_ip = networkArgs.mme_s1_ip,
                spgw_s1_ip = networkArgs.spgw_s1_ip,
                spgw_sgi_ip = networkArgs.spgw_sgi_ip,
                sgw_s5_ip = scenarioArgs.sgw_s5_ip,
                pgw_s5_ip = scenarioArgs.pgw_s5_ip,
                sink_ip = scenarioArgs.sink_ip,
                pgw_mgmt = scenarioArgs.pgw_mgmt,
                isPp = True)
    else:
        logger.error('--oai or --pp must be specified to select EPC implementation')
        logger.error('--pp needs the IPs of S5 interfaces,'
                     'the IP of the PGW\'s mgmt and the IP of sink'
                     '(--sgw_s5_ip, --pgw_s5_ip, --pgw_mgmt and --sink_ip)')
        return


    if generalArgs.stop:
        c.stop()
    else:
        c.start()
