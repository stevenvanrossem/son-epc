import son.vmmanager.processors.pp.sgw_processor as sgw_p
from son.vmmanager.processors.utils import CommandConfig
from son.vmmanager.jsonserver import IJsonProcessor as P

from unittest.mock import patch
from unittest.mock import Mock
import unittest
import tempfile
import logging
import os

logging.basicConfig(level=logging.DEBUG)

class SGW_Processor(unittest.TestCase):

    @patch('son.vmmanager.processors.utils.Runner')
    def testProcessIssueCommand(self, RunnerMock):
        RunnerMock.return_value = Mock(wraps = RunnerMock)
        S11_THREADS_COUNT = '10'
        S1_THREADS_COUNT = '11'
        S5_THREADS_COUNT = '12'
        SGW_S11_IP_ADDR = '10.0.0.1'
        SGW_S1_IP_ADDR = '10.0.0.2'
        SGW_S5_IP_ADDR = '10.0.0.3'
        PGW_S5_IP_ADDR = '10.0.0.4'
        DS_IP = '10.0.0.5'
        DS_PORT = '1234'
        SGW_S11_PORT = '1001'
        SGW_S1_PORT = '1002'
        SGW_S5_PORT = '1003'
        PGW_S5_PORT  = '1004'
        COMMAND = 'start'

        config_dict = {
            's11_threads_count': S11_THREADS_COUNT,
            's1_threads_count': S1_THREADS_COUNT,
            's5_threads_count': S5_THREADS_COUNT,
            'sgw_s11_ip_addr': SGW_S11_IP_ADDR,
            'sgw_s1_ip_addr': SGW_S1_IP_ADDR,
            'sgw_s5_ip_addr': SGW_S5_IP_ADDR,
            'pgw_s5_ip_addr': PGW_S5_IP_ADDR,
            'ds_ip': DS_IP,
            'ds_port': DS_PORT,
            'sgw_s11_port': SGW_S11_PORT,
            'sgw_s1_port': SGW_S1_PORT,
            'sgw_s5_port': SGW_S5_PORT,
            'pgw_s5_port': PGW_S5_PORT,
            'command': COMMAND,
            'garbage': {'key1': 1, 'key2': 2}
        }

        processor = sgw_p.SGW_Processor()
        processor.process(config_dict)

        RunnerMock.assert_called_once()
        RunnerMock.start.assert_called_once()

        args = ('--s11_threads_count %s '
                '--s1_threads_count %s '
                '--s5_threads_count %s '
                '--sgw_s11_ip_addr %s '
                '--sgw_s1_ip_addr %s '
                '--sgw_s5_ip_addr %s '
                '--pgw_s5_ip_addr %s '
                '--ds_ip %s '
                '--ds_port %s '
                '--sgw_s11_port %s '
                '--sgw_s1_port %s '
                '--sgw_s5_port %s '
                '--pgw_s5_port %s')
        args = args % (S11_THREADS_COUNT, S1_THREADS_COUNT, S5_THREADS_COUNT,
                       SGW_S11_IP_ADDR, SGW_S1_IP_ADDR, SGW_S5_IP_ADDR,
                       PGW_S5_IP_ADDR, DS_IP, DS_PORT, SGW_S11_PORT, SGW_S1_PORT,
                       SGW_S5_PORT, PGW_S5_PORT)
        RunnerMock.setArguments.assert_called_once_with(args)


class SGW_MsgParser(unittest.TestCase):
    def testFullConfigWithGarbage(self):
        S11_THREADS_COUNT = '10'
        S1_THREADS_COUNT = '11'
        S5_THREADS_COUNT = '12'
        SGW_S11_IP_ADDR = '10.0.0.1'
        SGW_S1_IP_ADDR = '10.0.0.2'
        SGW_S5_IP_ADDR = '10.0.0.3'
        PGW_S5_IP_ADDR = '10.0.0.4'
        DS_IP = '10.0.0.5'
        DS_PORT = '1234'
        SGW_S11_PORT = '1001'
        SGW_S1_PORT = '1002'
        SGW_S5_PORT = '1003'
        PGW_S5_PORT = '1004'
        COMMAND = 'start'

        config_dict = {
            's11_threads_count': S11_THREADS_COUNT,
            's1_threads_count': S1_THREADS_COUNT,
            's5_threads_count': S5_THREADS_COUNT,
            'sgw_s11_ip_addr': SGW_S11_IP_ADDR,
            'sgw_s1_ip_addr': SGW_S1_IP_ADDR,
            'sgw_s5_ip_addr': SGW_S5_IP_ADDR,
            'pgw_s5_ip_addr': PGW_S5_IP_ADDR,
            'ds_ip': DS_IP,
            'ds_port': DS_PORT,
            'sgw_s11_port': SGW_S11_PORT,
            'sgw_s1_port': SGW_S1_PORT,
            'sgw_s5_port': SGW_S5_PORT,
            'pgw_s5_port': PGW_S5_PORT,
            'command': COMMAND,
            'garbage': {'key1': 1, 'key2': 2}
        }

        parser = sgw_p.SGW_MessageParser(config_dict)
        config = parser.parse()

        self.assertEqual(config.s11_threads_count, S11_THREADS_COUNT)
        self.assertEqual(config.s1_threads_count, S1_THREADS_COUNT)
        self.assertEqual(config.s5_threads_count, S5_THREADS_COUNT)
        self.assertEqual(config.sgw_s11_ip_addr, SGW_S11_IP_ADDR)
        self.assertEqual(config.sgw_s1_ip_addr, SGW_S1_IP_ADDR)
        self.assertEqual(config.sgw_s5_ip_addr, SGW_S5_IP_ADDR)
        self.assertEqual(config.pgw_s5_ip_addr, PGW_S5_IP_ADDR)
        self.assertEqual(config.ds_ip, DS_IP)
        self.assertEqual(config.ds_port, DS_PORT)
        self.assertEqual(config.sgw_s11_port, SGW_S11_PORT)
        self.assertEqual(config.sgw_s1_port, SGW_S1_PORT)
        self.assertEqual(config.sgw_s5_port, SGW_S5_PORT)
        self.assertEqual(config.pgw_s5_port, PGW_S5_PORT)
        self.assertEqual(config.command, CommandConfig.START)
