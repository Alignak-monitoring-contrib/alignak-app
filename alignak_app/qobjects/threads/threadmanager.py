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
    Thread Manager manage BackendQThreads creations and their priority:

    * low : threads that group the queries about the elements that change little
    * normal: threads that group the queries on items that change often
    * high: threads that group the queries made on the fly
"""

from logging import getLogger

from PyQt5.Qt import QObject

from alignak_app.qobjects.threads.thread import BackendQThread

logger = getLogger(__name__)


class ThreadManager(QObject):
    """
        Class who create BackendQThreads periodically, to request on Alignak Backend endpoints
    """

    thread_names = {
        'low': ['user', 'realm', 'timeperiod', 'notifications'],
        'normal': ['host', 'alignakdaemon', 'livesynthesis', 'CRITICAL', 'WARNING', 'UNKNOWN']
    }

    def __init__(self, parent=None):
        super(ThreadManager, self).__init__(parent)
        self.threads_to_launch = {'low': [], 'normal': []}
        self.launched_threads = {'low': [], 'normal': []}
        self.high_threads = []

    def fill_threads(self, thread_type):
        """
        Fill threads to launch for a specific thread type

        :param thread_type: type of thread to fill
        :type thread_type: str
        """

        for t_name in self.thread_names[thread_type]:
            if not self.is_launched(thread_type, t_name):
                self.threads_to_launch[thread_type].append(t_name)

    def is_launched(self, thread_type, thread_name):
        """
        Returns if the thread name is already in the started threads type

        :param thread_type: type of thread
        :type thread_type: str
        :param thread_name: name of thread
        :type thread_name: str
        :return: if thread is launched or not
        :rtype: bool
        """

        for thread in self.launched_threads[thread_type]:
            if thread.name == thread_name:
                return True

        return False

    def launch_threads(self, thread_type=None):  # pragma: no cover
        """
        Launch the next thread of the given type or launch all the next threads for each type

        :param thread_type: type of thread to launch
        :type thread_type: str
        """

        if thread_type:
            if not self.threads_to_launch[thread_type]:
                self.fill_threads(thread_type)
            else:
                thread_name = self.threads_to_launch[thread_type].pop(0)
                thread = BackendQThread(thread_name)
                thread.start()

                self.launched_threads[thread_type].append(
                    thread
                )
        else:
            for t_type in self.threads_to_launch:
                if not self.threads_to_launch[t_type]:
                    self.fill_threads(t_type)
                else:
                    thread_name = self.threads_to_launch[t_type].pop(0)
                    thread = BackendQThread(thread_name)
                    thread.start()

                    self.launched_threads[t_type].append(
                        thread
                    )

    def add_high_priority_thread(self, thread_name, data):
        """
        Launch a thread with higher priority (doesn't wait launch_threads() function)

        :param thread_name: name of priority thread
        :type thread_name: str
        :param data: data to give to thread for request
        :type data: dict
        """

        if len(self.high_threads) < 3:
            backend_thread = BackendQThread(thread_name, data)
            backend_thread.start()

            self.high_threads.append(backend_thread)
        else:
            logger.debug('Too many priority threads for the moment...')

    def clean_threads(self):  # pragma: no cover
        """
        Clean current BackendQThreads

        """

        for t_thread in self.launched_threads:
            for thread in self.launched_threads[t_thread]:
                if thread.isFinished():
                    logger.debug('Quit %s thread: %s', t_thread, thread.name)
                    thread.quit()
                    self.launched_threads[t_thread].remove(thread)

        if self.high_threads:
            for thread in self.high_threads:
                if thread.isFinished():
                    thread.quit()
                    self.high_threads.remove(thread)
                    logger.debug('Remove finished thread: %s', thread.name)

    def stop_threads(self):
        """
        Stop all running BackendQThreads

        """

        if not self.high_threads and not self.launched_threads['low'] and \
                not self.launched_threads['normal']:
            logger.debug('No thread to stop.')

        for t_thread in self.launched_threads:
            for thread in self.launched_threads[t_thread]:
                logger.debug('Quit %s thread: %s', t_thread, thread.name)
                thread.quit()
                self.launched_threads[t_thread].remove(thread)

        if self.high_threads:
            self.stop_high_priority_threads()

    def stop_high_priority_threads(self):
        """
        Stop threads with high priority

        """

        for thread in self.high_threads:
            logger.debug('Quit priority thread: %s', thread.name)
            thread.quit()

            self.high_threads.remove(thread)


thread_manager = ThreadManager()
