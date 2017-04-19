import son.vmmanager.processors.pp.pgw_processor as pgw_p
from son.vmmanager.processors.utils import CommandConfig
from son.vmmanager.jsonserver import IJsonProcessor as P

from unittest.mock import patch
from unittest.mock import Mock
import unittest
import tempfile
import logging
import os

logging.basicConfig(level=logging.DEBUG)

class PGW_Processor(unittest.TestCase):

    @patch('son.vmmanager.processors.utils.Runner')
    def testProcessIssueCommand(self, RunnerMock):
        RunnerMock.return_value = Mock(wraps = RunnerMock)

        S5_THREADS_COUNT = '10'
        SGI_THREADS_COUNT = '20'
        SGW_S5_IP = '10.0.0.1'
        PGW_S5_IP = '10.0.0.2'
        PGW_SGI_IP = '10.0.0.3'
        SINK_IP_ADDR = '10.0.0.4'
        DS_IP = '10.0.0.5'
        DS_PORT = '1234'
        SGW_S5_PORT = '1001'
        PGW_S5_PORT = '1002'
        PGW_SGI_PORT = '1003'
        SINK_PORT = '1004'
        COMMAND = 'start'

        config_dict = {
            's5_threads_count': S5_THREADS_COUNT,
            'sgi_threads_count': SGI_THREADS_COUNT,
            'sgw_s5_ip': SGW_S5_IP,
            'pgw_s5_ip': PGW_S5_IP,
            'pgw_sgi_ip': PGW_SGI_IP,
            'sink_ip_addr': SINK_IP_ADDR,
            'ds_ip': DS_IP,
            'ds_port': DS_PORT,
            'sgw_s5_port': SGW_S5_PORT,
            'pgw_s5_port': PGW_S5_PORT,
            'pgw_sgi_port': PGW_SGI_PORT,
            'sink_port': SINK_PORT,
            'command': COMMAND,
            'garbage': {'key1': 1, 'key2': 2}
        }

        processor = pgw_p.PGW_Processor()
        processor.process(config_dict)

        RunnerMock.assert_called_once()
        RunnerMock.start.assert_called_once()

        args = ('--s5_threads_count %s '
                '--sgi_threads_count %s '
                '--sgw_s5_ip %s '
                '--pgw_s5_ip %s '
                '--pgw_sgi_ip %s '
                '--sink_ip_addr %s '
                '--ds_ip %s '
                '--ds_port %s '
                '--sgw_s5_port %s '
                '--pgw_s5_port %s '
                '--pgw_sgi_port %s '
                '--sink_port %s')
        args = args % (S5_THREADS_COUNT, SGI_THREADS_COUNT,
                       SGW_S5_IP, PGW_S5_IP, PGW_SGI_IP,
                       SINK_IP_ADDR, DS_IP, DS_PORT,
                       SGW_S5_PORT, PGW_S5_PORT,
                       PGW_SGI_PORT, SINK_PORT)
        RunnerMock.setArguments.assert_called_once_with(args)


class PGW_MsgParser(unittest.TestCase):
    def testFullConfigWithGarbage(self):
        S5_THREADS_COUNT = '10'
        SGI_THREADS_COUNT = '20'
        SGW_S5_IP = '10.0.0.1'
        PGW_S5_IP = '10.0.0.2'
        PGW_SGI_IP = '10.0.0.3'
        DS_IP = '10.0.0.4'
        DS_PORT = '1234'
        SINK_IP_ADDR = '10.0.0.4'
        SGW_S5_PORT = '1001'
        PGW_S5_PORT = '1002'
        PGW_SGI_PORT = '1003'
        SINK_PORT = '1004'
        COMMAND = 'start'

        config_dict = {
            's5_threads_count': S5_THREADS_COUNT,
            'sgi_threads_count': SGI_THREADS_COUNT,
            'sgw_s5_ip': SGW_S5_IP,
            'pgw_s5_ip': PGW_S5_IP,
            'pgw_sgi_ip': PGW_SGI_IP,
            'sink_ip_addr': SINK_IP_ADDR,
            'ds_ip': DS_IP,
            'ds_port': DS_PORT,
            'sgw_s5_port': SGW_S5_PORT,
            'pgw_s5_port': PGW_S5_PORT,
            'pgw_sgi_port': PGW_SGI_PORT,
            'sink_port': SINK_PORT,
            'command': COMMAND,
            'garbage': {'key1': 1, 'key2': 2}
        }

        parser = pgw_p.PGW_MessageParser(config_dict)
        config = parser.parse()

        self.assertEqual(config.s5_threads_count, S5_THREADS_COUNT)
        self.assertEqual(config.sgi_threads_count, SGI_THREADS_COUNT)
        self.assertEqual(config.sgw_s5_ip, SGW_S5_IP)
        self.assertEqual(config.pgw_s5_ip, PGW_S5_IP)
        self.assertEqual(config.pgw_sgi_ip, PGW_SGI_IP)
        self.assertEqual(config.sink_ip_addr, SINK_IP_ADDR)
        self.assertEqual(config.ds_ip, DS_IP)
        self.assertEqual(config.ds_port, DS_PORT)
        self.assertEqual(config.sgw_s5_port, SGW_S5_PORT)
        self.assertEqual(config.pgw_s5_port, PGW_S5_PORT)
        self.assertEqual(config.pgw_sgi_port, PGW_SGI_PORT)
        self.assertEqual(config.sink_port, SINK_PORT)
        self.assertEqual(config.command, CommandConfig.START)
