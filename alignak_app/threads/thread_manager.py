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
    ThreadManager manage QRunnables for each data
"""

import sys

from logging import getLogger

from PyQt5.Qt import QApplication, QThreadPool  # pylint: disable=no-name-in-module
from PyQt5.Qt import QTimer, QObject  # pylint: disable=no-name-in-module

from alignak_app.core.locales import init_localization
from alignak_app.core.utils import init_config
from alignak_app.core.backend import app_backend
from alignak_app.core.data_manager import data_manager
from alignak_app.threads.backend_runnable import BackendQRunnable


init_config()
logger = getLogger(__name__)
init_localization()


class ThreadManager(QObject):
    """
        Class who create BackendQRunnable to periodically request on Alignak Backend
    """

    def __init__(self, parent=None):
        super(ThreadManager, self).__init__(parent)
        self.backend_thread = BackendQRunnable(self)
        self.pool = QThreadPool.globalInstance()
        self.tasks = self.get_tasks()

    def start(self):
        """
        Start ThreadManager

        """

        logger.info("Start backend Manager...")

        # Make a first request
        self.create_tasks()

        # Then request periodically
        timer = QTimer(self)
        timer.setInterval(10000)
        timer.start()
        timer.timeout.connect(self.create_tasks)

    @staticmethod
    def get_tasks():
        """
        Return the tasks to run in BackendQRunnable

        :return: tasks to run
        :rtype: list
        """

        return [
            'notifications', 'livesynthesis', 'alignakdaemon', 'history', 'service', 'host', 'user',
        ]

    def create_tasks(self):
        """
        Create tasks to run

        """

        for cur_task in self.tasks:
            backend_thread = BackendQRunnable(cur_task)

            # Add task to QThreadPool
            self.pool.start(backend_thread)

        # For tests
        self.see_database()

    @staticmethod
    def see_database():
        """
        Display database for tests

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
