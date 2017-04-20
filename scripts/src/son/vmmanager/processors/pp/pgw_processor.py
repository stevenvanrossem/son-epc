from son.vmmanager.jsonserver import IJsonProcessor as P
from son.vmmanager.processors import utils

import tempfile
import logging

class PGW_MessageParser(object):

    MSG_S5_THREADS_COUNT = 's5_threads_count'
    MSG_SGI_THREADS_COUNT = 'sgi_threads_count'
    MSG_SGW_S5_IP = 'sgw_s5_ip'
    MSG_PGW_S5_IP = 'pgw_s5_ip'
    MSG_PGW_SGI_IP = 'pgw_sgi_ip'
    MSG_SINK_IP_ADDR = 'sink_ip_addr'
    MSG_DS_IP = 'ds_ip'
    MSG_DS_PORT = 'ds_port'
    MSG_SGW_S5_PORT = 'sgw_s5_port'
    MSG_PGW_S5_PORT = 'pgw_s5_port'
    MSG_PGW_SGI_PORT = 'pgw_sgi_port'
    MSG_SINK_PORT = 'sink_port'

    MSG = [MSG_S5_THREADS_COUNT, MSG_SGI_THREADS_COUNT,
           MSG_SGW_S5_IP, MSG_PGW_S5_IP,
           MSG_PGW_SGI_IP, MSG_DS_IP, MSG_DS_PORT,
           MSG_SINK_IP_ADDR, MSG_SGW_S5_PORT,
           MSG_PGW_S5_PORT, MSG_PGW_SGI_PORT,
           MSG_SINK_PORT]

    def __init__(self, json_dict):
        self.logger = logging.getLogger(PGW_MessageParser.__name__)
        self.msg_dict = json_dict
        self.command_parser = utils.CommandMessageParser(json_dict)

    def parse(self):
        arg_dict = {}
        for msg in self.MSG:
            arg_dict[msg] = self.msg_dict.get(msg, None)

        pc = PGW_Config(**arg_dict)
        self.command_parser.parse(pc)
        return pc


class PGW_Config(utils.CommandConfig):

    def __init__(self, s5_threads_count = None, sgi_threads_count = None,
                 sgw_s5_ip = None, pgw_s5_ip = None, pgw_sgi_ip = None,
                 sink_ip_addr = None, ds_ip = None, ds_port = None, sgw_s5_port = None,
                 pgw_s5_port = None, pgw_sgi_port = None, sink_port = None,
                 **kwargs):
        self.s5_threads_count = s5_threads_count
        self.sgi_threads_count = sgi_threads_count
        self.sgw_s5_ip = sgw_s5_ip
        self.pgw_s5_ip = pgw_s5_ip
        self.pgw_sgi_ip = pgw_sgi_ip
        self.sink_ip_addr = sink_ip_addr
        self.ds_ip = ds_ip
        self.ds_port = ds_port
        self.sgw_s5_port = sgw_s5_port
        self.pgw_s5_port = pgw_s5_port
        self.pgw_sgi_port = pgw_sgi_port
        self.sink_port = sink_port

        super(self.__class__, self).__init__(**kwargs)

    def update(self, pgw_config):
        if not isinstance(pgw_config, PGW_Config):
            return

        if pgw_config.s5_threads_count is not None:
            self.s5_threads_count = pgw_config.s5_threads_count
        if pgw_config.sgi_threads_count is not None:
            self.sgi_threads_count = pgw_config.sgi_threads_count
        if pgw_config.sgw_s5_ip is not None:
            self.sgw_s5_ip = pgw_config.sgw_s5_ip
        if pgw_config.pgw_s5_ip is not None:
            self.pgw_s5_ip = pgw_config.pgw_s5_ip
        if pgw_config.pgw_sgi_ip is not None:
            self.pgw_sgi_ip = pgw_config.pgw_sgi_ip
        if pgw_config.sink_ip_addr is not None:
            self.sink_ip_addr = pgw_config.sink_ip_addr
        if pgw_config.ds_ip is not None:
            self.ds_ip = pgw_config.ds_ip
        if pgw_config.ds_port is not None:
            self.ds_port = pgw_config.ds_port
        if pgw_config.sgw_s5_port is not None:
            self.sgw_s5_port = pgw_config.sgw_s5_port
        if pgw_config.pgw_s5_port is not None:
            self.pgw_s5_port = pgw_config.pgw_s5_port
        if pgw_config.pgw_sgi_port is not None:
            self.pgw_sgi_port = pgw_config.pgw_sgi_port
        if pgw_config.sink_port is not None:
            self.sink_port = pgw_config.sink_port


class PGW_Processor(P):

    PGW_EXECUTABLE = '~/NFV_LTE_EPC/NFV_LTE_EPC-1.1/src/pgw.out'

    def __init__(self):
        self.logger = logging.getLogger(PGW_Processor.__name__)

        self._log_dir = tempfile.TemporaryDirectory(prefix='pgw.processor')
        self._log_dir_name = self._log_dir.name
        self._runner = utils.Runner(self.PGW_EXECUTABLE,
                                    log_dir=self._log_dir_name)
        self._pgw_config = PGW_Config()

    def process(self, json_dict):
        parser = PGW_MessageParser(json_dict)
        pgw_config = parser.parse()
        self._pgw_config.update(pgw_config)

        if pgw_config.command == utils.CommandConfig.START:
            argset_res = self._setArguments()
            if argset_res.status is not P.Result.OK:
                return argset_res

            return self._runner.start()
        elif pgw_config.command == utils.CommandConfig.STOP:
            return self._runner.stop()
        elif pgw_config.command == utils.CommandConfig.RESTART:
            argset_res = self._setArguments()
            if argset_res.status is not P.Result.OK:
                return argset_res

            return self._runner.restart()
        elif pgw_config.command == utils.CommandConfig.STATUS:
            status = 'Running' if self._runner.isRunning() else 'Stopped'
            stdout = self._runner.getOutput()
            stderr = self._runner.getOutput(stderr=True)
            return P.Result.ok('Status', task_status = status,
                               stderr = stderr, stdout = stdout)
        elif pgw_config.command is None:
            return P.Result.warn('No command is given')
        else:
            return P.Result.fail('Invalid command is given %s',
                                 pgw_config.command)

    def _setArguments(self):

        nvalid = self._pgw_config.s5_threads_count is None
        nvalid = nvalid or self._pgw_config.sgi_threads_count is None
        nvalid = nvalid or self._pgw_config.sgw_s5_ip is None
        nvalid = nvalid or self._pgw_config.pgw_s5_ip is None
        nvalid = nvalid or self._pgw_config.pgw_sgi_ip is None
        nvalid = nvalid or self._pgw_config.sink_ip_addr is None
        nvalid = nvalid or self._pgw_config.ds_ip is None

        if nvalid:
            return P.Result.fail('IP SGW (S5), PGW (S5, SGI) and sink,'
                                 'and threads count must be provided (SGI, S5)')

        args = ('--s5_threads_count %s --sgi_threads_count %s '
                '--sgw_s5_ip %s --pgw_s5_ip %s '
                '--pgw_sgi_ip %s --sink_ip_addr %s '
                '--ds_ip %s')
        args = args % (self._pgw_config.s5_threads_count,
                       self._pgw_config.sgi_threads_count,
                       self._pgw_config.sgw_s5_ip,
                       self._pgw_config.pgw_s5_ip,
                       self._pgw_config.pgw_sgi_ip,
                       self._pgw_config.sink_ip_addr,
                       self._pgw_config.ds_ip)

        if self._pgw_config.ds_port is not None:
          args += ' --ds_port %s' % self._pgw_config.ds_port
        if self._pgw_config.sgw_s5_port is not None:
          args += ' --sgw_s5_port %s' % self._pgw_config.sgw_s5_port
        if self._pgw_config.pgw_s5_port is not None:
          args += ' --pgw_s5_port %s' % self._pgw_config.pgw_s5_port
        if self._pgw_config.pgw_sgi_port is not None:
          args += ' --pgw_sgi_port %s' % self._pgw_config.pgw_sgi_port
        if self._pgw_config.sink_port is not None:
          args += ' --sink_port %s' % self._pgw_config.sink_port

        self._runner.setArguments(args)

        return P.Result.ok('Arguments are set')
