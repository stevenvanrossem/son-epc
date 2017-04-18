import son.vmmanager.processors.pp.mme_processor as mme_p
from son.vmmanager.processors.utils import CommandConfig
from son.vmmanager.jsonserver import IJsonProcessor as P

from unittest.mock import patch
from unittest.mock import Mock
import unittest
import tempfile
import logging
import os

logging.basicConfig(level=logging.DEBUG)

class MME_Processor(unittest.TestCase):

    @patch('son.vmmanager.processors.utils.Runner')
    def testProcessIssueCommand(self, RunnerMock):
        RunnerMock.return_value = Mock(wraps = RunnerMock)

        THREADS_COUNT = '10'
        HSS_IP = '10.0.0.1'
        HSS_PORT = '10.0.0.2'
        SGW_S1_IP = '10.0.0.3'
        SGW_S11_IP = '10.0.0.4'
        SGW_S5_IP = '10.0.0.5'
        PGW_S5_IP = '10.0.0.6'
        TRAFMON_PORT = '1001'
        MME_PORT = '1002'
        SGW_S11_PORT = '1003'
        SGW_S1_PORT = '1004'
        SGW_S5_PORT = '1005'
        PGW_S5_PORT = '1006'
        COMMAND = 'start'

        config_dict = {
            "threads_count": THREADS_COUNT,
            "hss_ip": HSS_IP,
            "hss_port": HSS_PORT,
            "sgw_s1_ip": SGW_S1_IP,
            "sgw_s11_ip": SGW_S11_IP,
            "sgw_s5_ip": SGW_S5_IP,
            "pgw_s5_ip": PGW_S5_IP,
            "trafmon_port": TRAFMON_PORT,
            "mme_port": MME_PORT,
            "sgw_s11_port": SGW_S11_PORT,
            "sgw_s1_port": SGW_S1_PORT,
            "sgw_s5_port": SGW_S5_PORT,
            "pgw_s5_port": PGW_S5_PORT,
            'command': COMMAND,
            'garbage': {'key1': 1, 'key2': 2}
        }

        processor = mme_p.MME_Processor()
        processor.process(config_dict)

        RunnerMock.assert_called_once()
        RunnerMock.start.assert_called_once()

        args = ('--threads_count %s --hss_ip %s '
               '--sgw_s1_ip %s --sgw_s11_ip %s '
               '--sgw_s5_ip %s --pgw_s5_ip %s '
               '--trafmon_port %s --hss_port %s '
               '--mme_port %s --sgw_s11_port %s --sgw_s1_port %s '
               '--sgw_s5_port %s --pgw_s5_port %s')
        args = args % (THREADS_COUNT, HSS_IP,
                       SGW_S1_IP, SGW_S11_IP, SGW_S5_IP,
                       PGW_S5_IP, TRAFMON_PORT, HSS_PORT,
                       MME_PORT, SGW_S11_PORT, SGW_S1_PORT,
                       SGW_S5_PORT, PGW_S5_PORT)
        RunnerMock.setArguments.assert_called_once_with(args)


class MME_MsgParser(unittest.TestCase):
    def testFullConfigWithGarbage(self):
        THREADS_COUNT = '10'
        HSS_IP = '10.0.0.1'
        HSS_PORT = '10.0.0.2'
        SGW_S1_IP = '10.0.0.3'
        SGW_S11_IP = '10.0.0.4'
        SGW_S5_IP = '10.0.0.5'
        PGW_S5_IP = '10.0.0.6'
        TRAFMON_PORT = '1001'
        MME_PORT = '1002'
        SGW_S11_PORT = '1003'
        SGW_S1_PORT = '1004'
        SGW_S5_PORT = '1005'
        PGW_S5_PORT = '1006'
        COMMAND = 'start'

        config_dict = {
            "threads_count": THREADS_COUNT,
            "hss_ip": HSS_IP,
            "hss_port": HSS_PORT,
            "sgw_s1_ip": SGW_S1_IP,
            "sgw_s11_ip": SGW_S11_IP,
            "sgw_s5_ip": SGW_S5_IP,
            "pgw_s5_ip": PGW_S5_IP,
            "trafmon_port": TRAFMON_PORT,
            "mme_port": MME_PORT,
            "sgw_s11_port": SGW_S11_PORT,
            "sgw_s1_port": SGW_S1_PORT,
            "sgw_s5_port": SGW_S5_PORT,
            "pgw_s5_port": PGW_S5_PORT,
            'command': COMMAND,
            'garbage': {'key1': 1, 'key2': 2}
        }
        parser = mme_p.MME_MessageParser(config_dict)
        config = parser.parse()

        self.assertEqual(config.threads_count, THREADS_COUNT)
        self.assertEqual(config.hss_ip, HSS_IP)
        self.assertEqual(config.hss_port, HSS_PORT)
        self.assertEqual(config.sgw_s1_ip, SGW_S1_IP)
        self.assertEqual(config.sgw_s11_ip, SGW_S11_IP)
        self.assertEqual(config.sgw_s5_ip, SGW_S5_IP)
        self.assertEqual(config.pgw_s5_ip, PGW_S5_IP)
        self.assertEqual(config.trafmon_port, TRAFMON_PORT)
        self.assertEqual(config.mme_port, MME_PORT)
        self.assertEqual(config.sgw_s11_port, SGW_S11_PORT)
        self.assertEqual(config.sgw_s1_port, SGW_S1_PORT)
        self.assertEqual(config.sgw_s5_port, SGW_S5_PORT)
        self.assertEqual(config.pgw_s5_port, PGW_S5_PORT)
        self.assertEqual(config.command, CommandConfig.START)
