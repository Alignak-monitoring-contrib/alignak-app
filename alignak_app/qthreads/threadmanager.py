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

from PyQt5.Qt import QObject

from alignak_app.qthreads.thread import BackendQThread

logger = getLogger(__name__)


class ThreadManager(QObject):
    """
        Class who create BackendQThreads periodically, to request on Alignak Backend endpoints
    """

    def __init__(self, parent=None):
        super(ThreadManager, self).__init__(parent)
        self.current_thread = None
        self.priority_threads = []
        self.threads_to_launch = self.get_threads_to_launch()

    def get_threads_to_launch(self):
        """
        Return the threads_to_launch to run in BackendQRunnable

        :return: threads_to_launch to run
        :rtype: list
        """

        threads_to_launch = []

        # Add BackendQThread only if they are not already running
        for cur_thread in ['livesynthesis', 'host', 'service', 'user', 'realm', 'timeperiod',
                           'alignakdaemon', 'notifications', 'history']:
            if self.current_thread:
                if cur_thread != self.current_thread.thread_name:
                    threads_to_launch.append(cur_thread)
            else:
                threads_to_launch.append(cur_thread)

        logger.debug('Get new threads to launch %s', threads_to_launch)

        return threads_to_launch

    def launch_threads(self):  # pragma: no cover
        """
        Launch periodically threads

        """

        if not thread_manager.threads_to_launch:
            self.threads_to_launch = self.get_threads_to_launch()

        # In case there is no thread running
        if self.threads_to_launch and not self.current_thread:
            cur_thread = self.threads_to_launch.pop(0)
            backend_thread = BackendQThread(cur_thread)
            backend_thread.start()

            self.current_thread = backend_thread

    def clean_threads(self):  # pragma: no cover
        """
        Clean current BackendQThreads

        """

        if self.current_thread:
            if self.current_thread.isFinished():
                logger.debug('Remove finished thread: %s', self.current_thread.thread_name)
                self.current_thread.quit()
                self.current_thread = None

        if self.priority_threads:
            for thread in self.priority_threads:
                if thread.isFinished():
                    thread.quit()
                    self.priority_threads.remove(thread)
                    logger.debug('Remove finished thread: %s', thread.thread_name)

    def add_priority_thread(self, thread_name, data):  # pragma: no cover
        """
        Launch a thread with higher priority (doesn't wait launch_threads() function)

        :param thread_name: name of priority thread
        :type thread_name: str
        :param data: data to give to thread for request
        :type data: dict
        """

        if len(self.priority_threads) < 3:
            backend_thread = BackendQThread(thread_name, data)
            backend_thread.start()

            self.priority_threads.append(backend_thread)
        else:
            logger.debug('Too many priority thread for the moment...')

    def stop_threads(self):
        """
        Stop ThreadManager and close all running BackendQThreads

        """

        if self.priority_threads or self.current_thread:
            logger.debug("Finished backend threads have been stopped !")
        else:
            logger.debug('No thread to stop.')

        if self.current_thread:
            logger.debug('Try to quit current thread: %s', self.current_thread.thread_name)
            self.current_thread.quit()
            self.current_thread = None

        if self.priority_threads:
            self.stop_priority_threads()

    def stop_priority_threads(self):
        """
        Stop priority threads

        """

        for thread in self.priority_threads:
            logger.debug('Try to quit current priority thread: %s', thread.thread_name)
            thread.quit()

            self.priority_threads.remove(thread)


thread_manager = ThreadManager()
