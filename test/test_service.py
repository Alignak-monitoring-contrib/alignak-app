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

import sys

import unittest2

from alignak_app.synthesis.service import Service

try:
    __import__('PyQt5')
    from PyQt5.QtWidgets import QApplication, QPushButton
    from PyQt5.QtWidgets import QWidget, QLabel
except ImportError:
    from PyQt4.Qt import QApplication, QPushButton
    from PyQt4.Qt import QWidget, QLabel


class TestServicesView(unittest2.TestCase):
    """
        This file test the Service class.
    """

    service = {
        'name': 'My Service',
        'ls_state': 'OK',
        'ls_last_check': 0.0,
        'ls_output': 'Output of the service'
    }

    @classmethod
    def setUpClass(cls):
        """Create QApplication"""
        try:
            cls.app = QApplication(sys.argv)
            cls.widget = QWidget()
        except:
            pass

    def test_init_view(self):
        """Initialize Service"""

        under_test = Service()

        self.assertIsNotNone(under_test.acknowledged)
        self.assertIsNotNone(under_test.downtimed)

        self.assertIsNone(under_test.service)
        self.assertIsNone(under_test.acknowledge_btn)
        self.assertIsNone(under_test.downtime_btn)

        under_test.initialize(self.service)

        self.assertIsNotNone(under_test.service)
        self.assertIsNotNone(under_test.acknowledge_btn)
        self.assertIsNotNone(under_test.downtime_btn)
