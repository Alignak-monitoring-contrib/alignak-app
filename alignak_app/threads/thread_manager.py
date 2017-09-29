#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015-2017:
#   Matthieu Estrada, ttamalfor@gmail.com
#
# This file is part of (AlignakApp).
#
# (AlignakApp) is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# (AlignakApp) is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with (AlignakApp).  If not, see <http://www.gnu.org/licenses/>.

"""
    BackendManager manage backend data and threads
"""

import sys

from logging import getLogger

from PyQt5.Qt import QApplication  # pylint: disable=no-name-in-module
from PyQt5.Qt import QTimer, QObject  # pylint: disable=no-name-in-module

from alignak_app.core.locales import init_localization
from alignak_app.core.utils import init_config
from alignak_app.core.backend import app_backend
from alignak_app.threads.backend_thread import BackendQThread


init_config()
logger = getLogger(__name__)
init_localization()


class ThreadManager(QObject):
    """
        Class who create BackendQThreads to periodically request on Alignak Backend
        Store also data received by requests.
    """

    def __init__(self, parent=None):
        super(ThreadManager, self).__init__(parent)
        self.backend_thread = BackendQThread(self)

    def start(self):
        """
        Start ThreadManager

        """

        logger.info("Start backend Manager...")

        timer = QTimer(self)
        timer.setInterval(30000)
        timer.start()
        self.backend_thread.update_data.connect(self.update_data_manager)
        timer.timeout.connect(self.backend_thread.start)

    @staticmethod
    def update_data_manager(data_manager):
        """
        Update data stored in DataManager. TODO see if later this function will be kept !

        :param data_manager: DataManager who store all data, updated by BackendQThread
        :type data_manager: alignak_app.core.data_manager.DataManager
        """

        test_host = data_manager.get_item('host', '59ca454035d17b9607d66c52')
        print("Host: %s" % test_host)
        test_service = data_manager.get_item('service', '59c4e41635d17b8e0a6accdf')
        print("Service: %s" % test_service)
        test_daemon = data_manager.get_item('alignakdaemon', '59c4e64335d17b8e0c6ace0f')
        print("Daemon: %s" % test_daemon)
        test_synthesis = data_manager.get_synthesis_count()
        print("Synthesis: %s" % test_synthesis)
        test_user = data_manager.get_item('user', '59c4e3c135d17b8dff6acc5d')
        print("User: %s" % test_user)
        print("History: %s" % data_manager.history_database['history'])


# FOR TESTS
if __name__ == '__main__':

    app = QApplication(sys.argv)

    app_backend.login()

    thread_manager = ThreadManager()
    thread_manager.start()

    sys.exit(app.exec_())
