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

from PyQt5.Qt import QApplication  # pylint: disable=no-name-in-module
from PyQt5.Qt import QTimer, QObject  # pylint: disable=no-name-in-module

from alignak_app.core.backend import app_backend
from alignak_app.core.data_manager import DataManager
from alignak_app.core.locales import init_localization
from alignak_app.core.utils import init_config
from alignak_app.threads.backend_thread import BackendQThread

init_config()
init_localization()


class ThreadManager(QObject):
    """
        Class who create QThreads to periodically request on Alignak Backend
        Store also data received by requests.
    """

    def __init__(self, parent=None):
        super(ThreadManager, self).__init__(parent)
        self.backend_thread = BackendQThread(self)

    def start(self):
        """
        Start the manager

        """
        print("Start backend Manager")
        timer = QTimer(self)
        timer.setInterval(30000)
        timer.start()
        self.backend_thread.trigger.connect(self.update_data)
        timer.timeout.connect(self.backend_thread.start)

    def update_data(self, data_manager):
        """
        Update data stored.

        :param data_manager: DataManager who store all data, updated by BackendThread
        :type data_manager: DataManager
        """

        test_host = data_manager.get_item('host', '59ca454035d17b9607d66c52')
        print(test_host)
        test_service = data_manager.get_item('service', '59c4e41635d17b8e0a6accdf')
        print(test_service)


# FOR TESTS
if __name__ == '__main__':

    app = QApplication(sys.argv)

    mainwindow = ThreadManager()
    mainwindow.start()

    sys.exit(app.exec_())
