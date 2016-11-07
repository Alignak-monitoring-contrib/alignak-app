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
import configparser
import sys

from alignak_app.popup import AppPopup
from alignak_app.utils import get_alignak_home

try:
    __import__('PyQt5')
    from PyQt5.QtWidgets import QApplication  # pylint: disable=no-name-in-module
except ImportError:
    from PyQt4.Qt import QApplication  # pylint: disable=import-error


class TestPopup(unittest2.TestCase):
    """
        This file test methods of `utils.py` file.
    """

    @classmethod
    def setUpClass(cls):
        try:
            cls.app = QApplication(sys.argv)
        except:
            pass

    def test_initialize_notification(self):
        under_test = AppPopup()

        config_file = get_alignak_home() + '/alignak_app/settings.cfg'

        config = configparser.ConfigParser()
        config.read(config_file)

        self.assertIsNone(under_test.config)

        under_test.initialize_notification(config)

        self.assertIsNotNone(under_test.config)
