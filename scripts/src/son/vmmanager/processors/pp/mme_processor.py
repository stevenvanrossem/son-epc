from son.vmmanager.jsonserver import IJsonProcessor as P
from son.vmmanager.processors import utils

import tempfile
import logging

class MME_MessageParser(object):

    MSG_THREADS_COUNT = 'threads_count'
    MSG_HSS_IP = 'hss_ip'
    MSG_MME_IP = 'mme_ip'
    MSG_HSS_PORT = 'hss_port'
    MSG_SGW_S1_IP = 'sgw_s1_ip'
    MSG_SGW_S11_IP = 'sgw_s11_ip'
    MSG_SGW_S5_IP = 'sgw_s5_ip'
    MSG_PGW_S5_IP = 'pgw_s5_ip'
    MSG_DS_IP = 'ds_ip'
    MSG_DS_PORT = 'ds_port'
    MSG_TRAFMON_PORT = 'trafmon_port'
    MSG_MME_PORT = 'mme_port'
    MSG_SGW_S11_PORT = 'sgw_s11_port'
    MSG_SGW_S1_PORT = 'sgw_s1_port'
    MSG_SGW_S5_PORT = 'sgw_s5_port'
    MSG_PGW_S5_PORT = 'pgw_s5_port'

    MSG = [MSG_THREADS_COUNT, MSG_HSS_IP, MSG_HSS_PORT,
           MSG_HSS_IP, MSG_SGW_S1_IP, MSG_SGW_S11_IP, MSG_SGW_S5_IP, MSG_MME_IP,
           MSG_PGW_S5_IP, MSG_DS_IP, MSG_DS_PORT, MSG_TRAFMON_PORT, MSG_MME_PORT,
           MSG_SGW_S11_PORT, MSG_SGW_S1_PORT, MSG_SGW_S5_PORT,
           MSG_PGW_S5_PORT]

    def __init__(self, json_dict):
        self.logger = logging.getLogger(MME_MessageParser.__name__)
        self.msg_dict = json_dict
        self.command_parser = utils.CommandMessageParser(json_dict)

    def parse(self):
        arg_dict = {}
        for msg in self.MSG:
            arg_dict[msg] = self.msg_dict.get(msg, None)

        mc = MME_Config(**arg_dict)
        self.command_parser.parse(mc)

        return mc


class MME_Config(utils.CommandConfig):

    def __init__(self, threads_count = None, hss_ip = None, mme_ip = None,
                 hss_port = None, sgw_s1_ip = None, sgw_s11_ip = None,
                 sgw_s5_ip = None, pgw_s5_ip = None, ds_ip = None, ds_port = None,
                 trafmon_port = None, mme_port = None, sgw_s11_port = None,
                 sgw_s1_port = None, sgw_s5_port = None, pgw_s5_port = None,
                 **kwargs):
        self.threads_count = threads_count
        self.hss_ip = hss_ip
        self.mme_ip = mme_ip
        self.hss_port = hss_port
        self.sgw_s1_ip = sgw_s1_ip
        self.sgw_s11_ip = sgw_s11_ip
        self.sgw_s5_ip = sgw_s5_ip
        self.pgw_s5_ip = pgw_s5_ip
        self.ds_ip = ds_ip
        self.ds_port = ds_port
        self.trafmon_port = trafmon_port
        self.mme_port = mme_port
        self.sgw_s11_port = sgw_s11_port
        self.sgw_s1_port = sgw_s1_port
        self.sgw_s5_port = sgw_s5_port
        self.pgw_s5_port = pgw_s5_port

        super(self.__class__, self).__init__(**kwargs)

    def update(self, mme_config):
        if not isinstance(mme_config, MME_Config):
            return

        if mme_config.threads_count is not None:
            self.threads_count = mme_config.threads_count
        if mme_config.hss_ip is not None:
            self.hss_ip = mme_config.hss_ip
        if mme_config.mme_ip is not None:
            self.mme_ip = mme_config.mme_ip
        if mme_config.hss_port is not None:
            self.hss_port = mme_config.hss_port
        if mme_config.sgw_s1_ip is not None:
            self.sgw_s1_ip = mme_config.sgw_s1_ip
        if mme_config.sgw_s11_ip is not None:
            self.sgw_s11_ip = mme_config.sgw_s11_ip
        if mme_config.sgw_s5_ip is not None:
            self.sgw_s5_ip = mme_config.sgw_s5_ip
        if mme_config.pgw_s5_ip is not None:
            self.pgw_s5_ip = mme_config.pgw_s5_ip
        if mme_config.ds_ip is not None:
            self.ds_ip = mme_config.ds_ip
        if mme_config.ds_port is not None:
            self.ds_port = mme_config.ds_port
        if mme_config.trafmon_port is not None:
            self.trafmon_port = mme_config.trafmon_port
        if mme_config.mme_port is not None:
            self.mme_port = mme_config.mme_port
        if mme_config.sgw_s11_port is not None:
            self.sgw_s11_port = mme_config.sgw_s11_port
        if mme_config.sgw_s1_port is not None:
            self.sgw_s1_port = mme_config.sgw_s1_port
        if mme_config.sgw_s5_port is not None:
            self.sgw_s5_port = mme_config.sgw_s5_port
        if mme_config.pgw_s5_port is not None:
            self.pgw_s5_port = mme_config.pgw_s5_port


class MME_Processor(P):

    MME_EXECUTABLE = '~/NFV_LTE_EPC/NFV_LTE_EPC-1.1/src/mme.out'

    def __init__(self):
        self.logger = logging.getLogger(MME_Processor.__name__)

        self._log_dir = tempfile.TemporaryDirectory(prefix='mme.processor')
        self._log_dir_name = self._log_dir.name
        self._runner = utils.Runner(self.MME_EXECUTABLE,
                                    log_dir=self._log_dir_name)
        self._mme_config = MME_Config()

    def process(self, json_dict):
        parser = MME_MessageParser(json_dict)
        mme_config = parser.parse()
        self._mme_config.update(mme_config)

        if mme_config.command == utils.CommandConfig.START:
            argset_res = self._setArguments()
            if argset_res.status is not P.Result.OK:
                return argset_res

            return self._runner.start()
        elif mme_config.command == utils.CommandConfig.STOP:
            return self._runner.stop()
        elif mme_config.command == utils.CommandConfig.RESTART:
            argset_res = self._setArguments()
            if argset_res.status is not P.Result.OK:
                return argset_res

            return self._runner.restart()
        elif mme_config.command == utils.CommandConfig.STATUS:
            status = 'Running' if self._runner.isRunning() else 'Stopped'
            stdout = self._runner.getOutput()
            stderr = self._runner.getOutput(stderr=True)
            return P.Result.ok('Status', task_status = status,
                               stderr = stderr, stdout = stdout)
        elif mme_config.command is None:
            return P.Result.warn('No command is given')
        else:
            return P.Result.fail('Invalid command is given %s',
                                 mme_config.command)

    def _setArguments(self):
        nvalid = self._mme_config.threads_count is None
        nvalid = nvalid or self._mme_config.hss_ip is None
        nvalid = nvalid or self._mme_config.mme_ip is None
        nvalid = nvalid or self._mme_config.sgw_s1_ip is None
        nvalid = nvalid or self._mme_config.sgw_s11_ip is None
        nvalid = nvalid or self._mme_config.sgw_s5_ip is None
        nvalid = nvalid or self._mme_config.pgw_s5_ip is None
        nvalid = nvalid or self._mme_config.ds_ip is None

        if nvalid:
            return P.Result.fail('IP for HSS, SGW (S1,S11,S5) and PGW (S5),'
                                 'and threads count must be provided')

        args = ('--threads_count %s --hss_ip %s '
                '--sgw_s1_ip %s --sgw_s11_ip %s '
                '--sgw_s5_ip %s --pgw_s5_ip %s '
                '--ds_ip %s --mme_ip %s')
        args = args % (self._mme_config.threads_count,
               self._mme_config.hss_ip,
               self._mme_config.sgw_s1_ip,
               self._mme_config.sgw_s11_ip,
               self._mme_config.sgw_s5_ip,
               self._mme_config.pgw_s5_ip,
               self._mme_config.ds_ip,
               self._mme_config.mme_ip)

        if self._mme_config.ds_port is not None:
            args += ' --ds_port %s' % self._mme_config.ds_port
        if self._mme_config.trafmon_port is not None:
            args += ' --trafmon_port %s' % self._mme_config.trafmon_port
        if self._mme_config.hss_port is not None:
            args += ' --hss_port %s' % self._mme_config.hss_port
        if self._mme_config.mme_port is not None:
            args += ' --mme_port %s' % self._mme_config.mme_port
        if self._mme_config.sgw_s11_port is not None:
            args += ' --sgw_s11_port %s' % self._mme_config.sgw_s11_port
        if self._mme_config.sgw_s1_port is not None:
            args += ' --sgw_s1_port %s' % self._mme_config.sgw_s1_port
        if self._mme_config.sgw_s5_port is not None:
            args += ' --sgw_s5_port %s' % self._mme_config.sgw_s5_port
        if self._mme_config.pgw_s5_port is not None:
            args += ' --pgw_s5_port %s' % self._mme_config.pgw_s5_port

        self._runner.setArguments(args)

        return P.Result.ok('Arguments are set')
