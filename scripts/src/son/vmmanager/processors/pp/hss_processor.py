from son.vmmanager.jsonserver import IJsonProcessor as P
from son.vmmanager.processors import utils

import tempfile
import logging

class HSS_MessageParser(object):

    MSG_THREADS_COUNT = 'threads_count'
    MSG_IP = 'ip'
    MSG_PORT = 'port'

    def __init__(self, json_dict):
        self.logger = logging.getLogger(HSS_MessageParser.__name__)
        self.msg_dict = json_dict
        self.command_parser = utils.CommandMessageParser(json_dict)

    def parse(self):
        tc = self.msg_dict.get(self.MSG_THREADS_COUNT, None)
        ip = self.msg_dict.get(self.MSG_IP, None)
        port = self.msg_dict.get(self.MSG_PORT, None)
        self.logger.info('Got arguments: ip=%s; port=%s; thread counts=%s',
                         ip, port, tc)

        hc = HSS_Config(tc, ip , port)
        self.command_parser.parse(hc)
        return hc


class HSS_Config(utils.CommandConfig):

    def __init__(self, threads_count = None, ip = None, port = None, **kwargs):
        self.threads_count = threads_count
        self.ip = ip
        self.port = port
        super(self.__class__, self).__init__(**kwargs)

    def update(self, hss_config):
        if not isinstance(hss_config, HSS_Config):
            return

        if hss_config.ip is not None:
            self.ip = hss_config.ip
        if hss_config.port is not None:
            self.port = hss_config.port
        if hss_config.threads_count is not None:
            self.threads_count = hss_config.threads_count


class HSS_Processor(P):

    HSS_EXECUTABLE = '~/NFV_LTE_EPC/NFV_LTE_EPC-1.1/src/hss.out'

    def __init__(self):
        self.logger = logging.getLogger(HSS_Processor.__name__)

        self._log_dir = tempfile.TemporaryDirectory(prefix='hss.processor')
        self._log_dir_name = self._log_dir.name
        self._runner = utils.Runner(self.HSS_EXECUTABLE,
                                    log_dir=self._log_dir_name)
        self._hss_config = HSS_Config()

    def process(self, json_dict):
        parser = HSS_MessageParser(json_dict)
        hss_config = parser.parse()
        self._hss_config.update(hss_config)

        if hss_config.command == utils.CommandConfig.START:
            argset_res = self._setArguments()
            if argset_res.status is not P.Result.OK:
                return argset_res

            return self._runner.start()
        elif hss_config.command == utils.CommandConfig.STOP:
            return self._runner.stop()
        elif hss_config.command == utils.CommandConfig.RESTART:
            argset_res = self._setArguments()
            if argset_res.status is not P.Result.OK:
                return argset_res

            return self._runner.restart()
        elif hss_config.command == utils.CommandConfig.STATUS:
            status = 'Running' if self._runner.isRunning() else 'Stopped'
            stdout = self._runner.getOutput()
            stderr = self._runner.getOutput(stderr=True)
            return P.Result.ok('Status', task_status = status,
                               stderr = stderr, stdout = stdout)
        elif hss_config.command is None:
            return P.Result.warn('No command is given')
        else:
            return P.Result.fail('Invalid command is given %s',
                                 hss_config.command)

    def _setArguments(self):
        if self._hss_config.ip is None or \
                self._hss_config.threads_count is None:
            return P.Result.fail('IP and thread count must be provided')

        if  self._hss_config.port is not None:
            self._runner.setArguments("--threads_count %s "
                                    "--hss_ip %s --hss_port %s" % (
                                        self._hss_config.threads_count,
                                        self._hss_config.ip,
                                        self._hss_config.port))
        else:
            self._runner.setArguments("--threads_count %s --hss_ip %s " % (
                                        self._hss_config.threads_count,
                                        self._hss_config.ip))

        return P.Result.ok('Arguments are set')
