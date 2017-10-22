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

import unittest2

from alignak_app.threads.thread_manager import ThreadManager

from alignak_app.core.config import init_config
from alignak_app.core.locales import init_localization

from PyQt5.Qt import QTimer

init_config()
init_localization()


class TestThreadManager(unittest2.TestCase):
    """
        This file test the ThreadManager classes.
    """

    def test_initialize_thread_manager(self):
        """Initialize ThreadManager"""

        under_test = ThreadManager()

        self.assertFalse(under_test.current_threads)
        self.assertIsNotNone(under_test.timer)
        self.assertIsInstance(under_test.timer, QTimer)
        self.assertEqual(
            ['notifications', 'livesynthesis', 'alignakdaemon', 'history', 'service', 'host', 'user'],
            under_test.threads_to_launch
        )
