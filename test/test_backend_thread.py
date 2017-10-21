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

import sys

import unittest2

from alignak_app.core.data_manager import data_manager
from alignak_app.core.config import init_config
from alignak_app.core.locales import init_localization
from alignak_app.core.backend import app_backend
from alignak_app.threads.backend_thread import BackendQThread

from PyQt5.Qt import QApplication

init_config()
init_localization()
app_backend.login()


class TestBackendQThread(unittest2.TestCase):
    """
        This file test the BackendQThread classes.
    """

    def test_initialize_backend_thread(self):
        """Initialize BackendQThread"""

        under_test = BackendQThread('user')

        self.assertEqual('user', under_test.task)
