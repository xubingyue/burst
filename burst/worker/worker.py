# -*- coding: utf-8 -*-

import signal
from .connection import Connection
from ..log import logger
from .request import Request
from .. import constants
import setproctitle


class Worker(object):

    type = constants.PROC_TYPE_WORKER

    request_class = Request
    connection_class = Connection
    group_id = None

    # 是否有效(父进程中代表程序有效，子进程中代表worker是否有效)
    enable = True

    def __init__(self, app):
        """
        构造函数
        :return:
        """
        self.app = app

    def run(self, group_id):
        self.group_id = group_id

        setproctitle.setproctitle(self.app.make_proc_name(self.type))

        self._handle_proc_signals()
        self._before_worker_run()

        try:
            address = self.app.worker_address_tpl % self.group_id
            conn = self.connection_class(self, address, self.app.conn_timeout)
            conn.run()
        except KeyboardInterrupt:
            pass
        except:
            logger.error('exc occur.', exc_info=True)

    def _before_worker_run(self):
        self.app.events.create_worker()
        for bp in self.app.blueprints:
            bp.events.create_app_worker()

    def _handle_proc_signals(self):
        def exit_handler(signum, frame):
            # 防止重复处理KeyboardInterrupt，导致抛出异常
            if self.enable:
                self.enable = False
                raise KeyboardInterrupt

        def safe_stop_handler(signum, frame):
            self.enable = False

        # 强制结束，抛出异常终止程序进行
        signal.signal(signal.SIGINT, exit_handler)
        signal.signal(signal.SIGQUIT, exit_handler)
        # 安全停止
        signal.signal(signal.SIGTERM, safe_stop_handler)
        signal.signal(signal.SIGHUP, safe_stop_handler)
