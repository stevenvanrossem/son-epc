import son.vmmanager.processors.pp.hss_processor as hss_p
from son.vmmanager.processors.utils import CommandConfig
from son.vmmanager.jsonserver import IJsonProcessor as P

from unittest.mock import patch
from unittest.mock import Mock
import unittest
import tempfile
import logging
import os

logging.basicConfig(level=logging.DEBUG)

class HSS_Processor(unittest.TestCase):

    @patch('son.vmmanager.processors.utils.Runner')
    def testProcessIssueCommand(self, RunnerMock):
        RunnerMock.return_value = Mock(wraps = RunnerMock)

        THREADS_COUNT = '10'
        IP = '10.0.0.1'
        DS_IP = '10.0.0.2'
        PORT = '1234'
        COMMAND = 'start'

        config_dict = {
            'threads_count': THREADS_COUNT,
            'ip': IP,
            'ds_ip': DS_IP,
            'port': PORT,
            'command': COMMAND,
            'garbage': {'key1': 1, 'key2': 2}
        }

        processor = hss_p.HSS_Processor()
        processor.process(config_dict)

        RunnerMock.assert_called_once()
        RunnerMock.start.assert_called_once()

        args = '--threads_count %s --hss_ip %s --ds_ip %s --hss_port %s'
        args = args % (THREADS_COUNT, IP, DS_IP, PORT)
        RunnerMock.setArguments.assert_called_once_with(args)


class HSS_MsgParser(unittest.TestCase):
    def testFullConfigWithGarbage(self):
        THREADS_COUNT = '10'
        IP = '10.0.0.1'
        DS_IP = '10.0.0.2'
        PORT = '1234'
        COMMAND = 'start'

        config_dict = {
            'threads_count': THREADS_COUNT,
            'ip': IP,
            'ds_ip': DS_IP,
            'port': PORT,
            'command': COMMAND,
            'garbage': {'key1': 1, 'key2': 2}
        }
        parser = hss_p.HSS_MessageParser(config_dict)
        config = parser.parse()

        self.assertEqual(config.threads_count, THREADS_COUNT)
        self.assertEqual(config.ip, IP)
        self.assertEqual(config.ds_ip, DS_IP)
        self.assertEqual(config.port, PORT)
        self.assertEqual(config.command, CommandConfig.START)
