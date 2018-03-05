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

import unittest2

from alignak_app.utils.config import settings
from alignak_app.locales.locales import init_localization

from alignak_app.qthreads.thread import BackendQThread
from alignak_app.qthreads.threadmanager import ThreadManager

settings.init_config()
init_localization()


class TestThreadManager(unittest2.TestCase):
    """
        This file test the ThreadManager classes.
    """

    def test_initialize_thread_manager(self):
        """Initialize ThreadManager"""

        under_test = ThreadManager()

        self.assertFalse(under_test.current_thread)
        self.assertFalse(under_test.priority_threads)
        for thread in ['livesynthesis', 'host', 'service', 'user',
                       'alignakdaemon', 'notifications', 'history']:
            self.assertTrue(thread in under_test.threads_to_launch)

    def test_get_threads_to_launch(self):
        """Get QThreads to Launch"""

        thread_mgr_test = ThreadManager()

        under_test = thread_mgr_test.get_threads_to_launch()

        # If there is no current thread, all threads are added
        self.assertIsNone(thread_mgr_test.current_thread)
        for thread in ['livesynthesis', 'host', 'service', 'user', 'alignakdaemon',
                       'notifications', 'history']:
            self.assertTrue(thread in under_test)

        thread_mgr_test.current_thread = BackendQThread('user')

        under_test = thread_mgr_test.get_threads_to_launch()

        # If there is current thread, ThreadManager add only threads who are necessary
        self.assertNotEqual([], thread_mgr_test.current_thread)
        self.assertTrue('user' not in under_test)

    def test_priority_threads(self):
        """Remove Priority Threads"""

        under_test = ThreadManager()
        under_test.priority_threads.append(BackendQThread('user'))

        self.assertTrue(under_test.priority_threads)

        under_test.stop_priority_threads()

        self.assertFalse(under_test.priority_threads)

        under_test.priority_threads.append(BackendQThread('user'))
        under_test.priority_threads.append(BackendQThread('host'))
        under_test.priority_threads.append(BackendQThread('history'))

        self.assertTrue(len(under_test.priority_threads) == 3)

        under_test.add_priority_thread('user', {})

        self.assertTrue(len(under_test.priority_threads) == 3)


    def test_stop_threads(self):
        """Stop All Threads"""

        under_test = ThreadManager()

        under_test.priority_threads.append(BackendQThread(''))
        under_test.current_thread = BackendQThread('')

        self.assertTrue(under_test.priority_threads)
        self.assertTrue(under_test.current_thread)

        under_test.stop_threads()

        self.assertFalse(under_test.priority_threads)
        self.assertFalse(under_test.current_thread)
