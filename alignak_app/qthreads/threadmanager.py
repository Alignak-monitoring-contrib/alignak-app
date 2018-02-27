#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015-2018:
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
    Thread Manager
    ++++++++++++++
    Thread Manager manage creation of QObject for launched threads
"""

from logging import getLogger

from PyQt5.Qt import QTimer, QObject

from alignak_app.qthreads.thread import BackendQThread

logger = getLogger(__name__)


class ThreadManager(QObject):
    """
        Class who create BackendQThreads periodically, to request on Alignak Backend endpoints
    """

    def __init__(self, parent=None):
        super(ThreadManager, self).__init__(parent)
        self.current_thread = None
        self.threads_to_launch = self.get_threads_to_launch()
        self.timer = QTimer()

    def get_threads_to_launch(self):
        """
        Return the threads_to_launch to run in BackendQRunnable

        :return: threads_to_launch to run
        :rtype: list
        """

        threads_to_launch = []

        # Add BackendQThread only if they are not already running
        for cur_thread in ['livesynthesis', 'host', 'service', 'user',
                           'alignakdaemon', 'notifications', 'history']:
            if self.current_thread:
                if cur_thread != self.current_thread.thread_name:
                    threads_to_launch.append(cur_thread)
            else:
                threads_to_launch.append(cur_thread)

        logger.debug('Get new threads to launch %s', threads_to_launch)

        return threads_to_launch

    def add_thread(self, thread_name, data):
        """
        Add a thread, actually used for new history

        :param thread_name: name of thread
        :type thread_name: str
        :param data: data to give to thread for request
        :type data: dict
        """

        if not self.current_thread:
            backend_thread = BackendQThread(thread_name, data)
            backend_thread.start()
            self.current_thread = backend_thread

    def stop_threads(self):
        """
        Stop ThreadManager and close all running BackendQThreads

        """

        self.timer.stop()

        if self.current_thread:
            logger.debug('Try to quit current thread: %s', self.current_thread.thread_name)
            self.current_thread.quit()
            # del self.current_thread
            self.current_thread = None
            logger.info("The backend threads were stopped !")


thread_manager = ThreadManager()
