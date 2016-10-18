#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015-2016:
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
import configparser as cfg

from alignak_app.app import AlignakApp, QIcon
from alignak_app.alignak_data import AlignakData

import os


class TestApp(unittest2.TestCase):
    """
        This file test methods of AlignakApp class.
    """

    dir_path = os.path.dirname(os.path.realpath(__file__))
    config = cfg.ConfigParser()
    config.read(dir_path + '/etc/settings.cfg')

    def test_app_main(self):
        under_test = AlignakApp()

        self.assertIsNone(under_test.app)
        self.assertIsNone(under_test.alignak_data)
        self.assertIsNone(under_test.config)
        self.assertIsNone(under_test.tray_icon)

        under_test.config = TestApp.config

        under_test.main()

        self.assertIsNotNone(under_test.app)
        self.assertIsNotNone(under_test.tray_icon)

    def test_set_icon(self):
        under_test = AlignakApp()

        under_test.config = TestApp.config

        icon = under_test.get_icon()

        self.assertIsInstance(icon, QIcon, 'This is a test for QIcon')
