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

from alignak_app.qobjects.threads.thread import BackendQThread
from alignak_app.qobjects.threads.threadmanager import ThreadManager

settings.init_config()
init_localization()


class TestThreadManager(unittest2.TestCase):
    """
        This file test the ThreadManager classes.
    """

    def test_initialize_thread_manager(self):
        """Initialize ThreadManager"""

        under_test = ThreadManager()

        for t_type in under_test.threads_to_launch:
            self.assertFalse(under_test.threads_to_launch[t_type])
        self.assertFalse(under_test.high_threads)

    def test_fill_threads(self):
        """Add Low / Normal Threads"""

        under_test = ThreadManager()

        self.assertFalse(under_test.threads_to_launch['low'])
        self.assertFalse(under_test.threads_to_launch['normal'])

        under_test.fill_threads('low')

        self.assertTrue(under_test.threads_to_launch['low'])
        self.assertFalse(under_test.threads_to_launch['normal'])

        under_test.fill_threads('normal')

        self.assertTrue(under_test.threads_to_launch['low'])
        self.assertTrue(under_test.threads_to_launch['normal'])

    def test_is_launched(self):
        """Thread Is Launched"""

        under_test = ThreadManager()

        test_launched = under_test.is_launched('low', 'user')

        self.assertFalse(test_launched)

        under_test.launched_threads['low'].append(BackendQThread('user'))

        test_launched = under_test.is_launched('low', 'user')
        self.assertTrue(test_launched)

    def test_priority_threads(self):
        """Add / Remove Priority Threads"""

        under_test = ThreadManager()
        under_test.high_threads.append(BackendQThread('user'))

        self.assertTrue(under_test.high_threads)

        under_test.stop_high_priority_threads()

        # Priority thread is removed
        self.assertFalse(under_test.high_threads)

        # Add 3 priority threads
        under_test.high_threads.append(BackendQThread('user'))
        under_test.high_threads.append(BackendQThread('host'))
        under_test.high_threads.append(BackendQThread('history'))

        self.assertTrue(len(under_test.high_threads) == 3)

        under_test.add_high_priority_thread('user', {})

        # When already 3 priority threads, next priority htread is not add
        self.assertTrue(len(under_test.high_threads) == 3)

    def test_stop_threads(self):
        """Stop All Threads"""

        under_test = ThreadManager()

        under_test.high_threads.append(BackendQThread(''))
        under_test.launched_threads['low'].append(BackendQThread(''))
        under_test.launched_threads['normal'].append(BackendQThread(''))

        self.assertTrue(under_test.high_threads)
        self.assertTrue(under_test.launched_threads['low'])
        self.assertTrue(under_test.launched_threads['normal'])

        under_test.stop_threads()

        self.assertFalse(under_test.high_threads)
        self.assertFalse(under_test.launched_threads['low'])
        self.assertFalse(under_test.launched_threads['normal'])
