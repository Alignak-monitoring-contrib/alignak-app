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

from PyQt5.Qt import QApplication, QThreadPool  # pylint: disable=no-name-in-module
from PyQt5.Qt import QTimer, QObject  # pylint: disable=no-name-in-module

from alignak_app.core.locales import init_localization
from alignak_app.core.utils import init_config
from alignak_app.core.backend import app_backend
from alignak_app.core.data_manager import data_manager
from alignak_app.threads.backend_thread import BackendQThread
from alignak_app.threads.backend_runnable import BackendQRunnable


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
        self.backend_thread = BackendQRunnable(self)
        self.pool = QThreadPool.globalInstance()
        self.tasks = []

    def start(self):
        """
        Start ThreadManager

        """

        logger.info("Start backend Manager...")
        self.create_task()

        timer = QTimer(self)
        timer.setInterval(10000)
        timer.start()
        timer.timeout.connect(self.create_task)

    @staticmethod
    def get_tasks():
        """
        TODO
        :return
        """

        return [
            'notifications', 'livesynthesis', 'alignakdaemon', 'history', 'service', 'host', 'user',
        ]

    def create_task(self):
        """
        TODO
        :return:
        """

        if not self.tasks:
            self.tasks = self.get_tasks()

        # cur_task = self.tasks.pop()
        for cur_task in self.tasks:

            backend_thread = BackendQRunnable(cur_task)

            self.pool.start(backend_thread)

        self.see_database()

    @staticmethod
    def see_database():
        """
        Update data stored in DataManager. TODO see if later this function will be kept !

        """

        print("User: %s" % data_manager.database['user'])
        print(
            "Hosts (%d) %s" % (
                len(data_manager.database['host']),
                data_manager.database['host']
            )
        )
        print(
            "Services (%d) %s " % (
                len(data_manager.database['service']),
                data_manager.database['service']
            )
        )
        print(
            "Daemons (%d) %s " % (
                len(data_manager.database['alignakdaemon']),
                data_manager.database['alignakdaemon']
            )
        )
        print(
            "Livesynthesis (%d) %s " % (
                len(data_manager.database['livesynthesis']),
                data_manager.database['livesynthesis']
            )
        )
        print(
            "History (%d) %s " % (
                len(data_manager.database['history']),
                data_manager.database['history']
            )
        )
        print(
            "Notifications (%d) %s " % (
                len(data_manager.database['notifications']),
                data_manager.database['notifications']
            )
        )


# FOR TESTS
if __name__ == '__main__':

    app = QApplication(sys.argv)

    app_backend.login()

    thread_manager = ThreadManager()
    thread_manager.start()

    sys.exit(app.exec_())
