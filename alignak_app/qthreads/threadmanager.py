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

from alignak_app.utils.config import settings

from alignak_app.qthreads.thread import BackendQThread

logger = getLogger(__name__)


class ThreadManager(QObject):
    """
        Class who create BackendQThreads periodically, to request on Alignak Backend endpoints
    """

    def __init__(self, parent=None):
        super(ThreadManager, self).__init__(parent)
        self.current_threads = []
        self.threads_to_launch = self.get_threads_to_launch()
        self.timer = QTimer()

    def start(self):  # pragma: no cover
        """
        Start ThreadManager

        """

        logger.info('Start Thread Manager...')

        requests_interval = int(settings.get_config('Alignak-app', 'requests_interval')) * 1000
        self.timer.setInterval(requests_interval)
        self.timer.start()
        self.timer.timeout.connect(self.launch_threads)

    def get_threads_to_launch(self):
        """
        Return the threads_to_launch to run in BackendQRunnable

        :return: threads_to_launch to run
        :rtype: list
        """

        threads_to_launch = []

        # Add BackendQThread only if they are not already running
        for cur_thread in ['user', 'host', 'service', 'livesynthesis',
                           'alignakdaemon', 'notifications', 'history']:
            if not any(cur_thread == thread.thread_name for thread in self.current_threads):
                threads_to_launch.append(cur_thread)

        logger.debug('Get new threads to launch %s', threads_to_launch)

        return threads_to_launch

    def launch_threads(self):  # pragma: no cover
        """
        Create threads_to_launch to run

        """

        if not self.threads_to_launch:
            self.threads_to_launch = self.get_threads_to_launch()

        # In case of all threads are not running
        if self.threads_to_launch:
            cur_thread = self.threads_to_launch.pop(0)
            backend_thread = BackendQThread(cur_thread)
            backend_thread.start()

            self.current_threads.append(backend_thread)

        # Cleaning threads who are finished
        for thread in self.current_threads:
            if thread.isFinished():
                logger.debug('Remove finished thread: %s', thread.thread_name)
                thread.quit()
                thread.wait()
                self.current_threads.remove(thread)

    def add_thread(self, thread_name, data):
        """
        Add a thread, actually used for new history

        :param thread_name: name of thread
        :type thread_name: str
        :param data: data to give to thread for request
        :type data: dict
        """

        if not any(data == thread.data for thread in self.current_threads):
            thread = BackendQThread(thread_name, data)
            thread.start()

            self.current_threads.append(thread)

    def stop_threads(self):
        """
        Stop ThreadManager and close all running BackendQThreads

        """

        logger.info("Stop backend threads...")
        self.timer.stop()
        for thread in self.current_threads:
            logger.debug('Try to quit thread: %s', thread.thread_name)
            thread.quit_thread.emit()

        logger.info("The backend threads were stopped !")


thread_manager = ThreadManager()
