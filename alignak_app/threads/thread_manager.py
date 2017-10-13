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

from logging import getLogger

from PyQt5.Qt import QTimer, QObject  # pylint: disable=no-name-in-module

from alignak_app.core.locales import init_localization
from alignak_app.core.utils import init_config
from alignak_app.threads.backend_thread import BackendQThread


init_config()
logger = getLogger(__name__)
init_localization()


class ThreadManager(QObject):
    """
        Class who create BackendQRunnable to periodically request on Alignak Backend
    """

    def __init__(self, parent=None):
        super(ThreadManager, self).__init__(parent)
        self.tasks = self.get_tasks()
        self.timer = QTimer()
        self.threads = []

    def start(self):
        """
        Start ThreadManager

        """

        logger.info('Start Thread Manager...')

        # Make a first request
        self.create_tasks()

        # Then request periodically
        self.timer.setInterval(15000)
        self.timer.start()
        self.timer.timeout.connect(self.create_tasks)

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

        self.threads = []
        for cur_task in self.tasks:
            backend_thread = BackendQThread(cur_task)
            backend_thread.start()

            # Add task to thread to keep a reference
            self.threads.append(backend_thread)

    def add_task(self, task):
        """
        Add a specific QThreads in list

        :param task: one of the following:
        - 'notifications', 'livesynthesis', 'alignakdaemon', 'history', 'service', 'host', 'user'
        :type task: str
        """

        backend_thread = BackendQThread(task)
        backend_thread.start()
        self.threads.append(backend_thread)

    def stop(self):
        """
        Stop the manager and close all running QThreads

        """

        logger.info("Stop backend threads...")
        self.timer.stop()
        for task in self.threads:
            task.quit_thread.emit()

        logger.info("Backend threads are finished.")


thread_manager = ThreadManager()
