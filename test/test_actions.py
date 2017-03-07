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

from alignak_app.synthesis.actions import Acknowledge, Downtime, get_logo_widget

from PyQt5.QtWidgets import QApplication, QWidget


class TestActions(unittest2.TestCase):
    """
        This file test the Acknowledge and Downtime classes.
    """

    @classmethod
    def setUpClass(cls):
        """Create QApplication"""
        try:
            cls.app = QApplication(sys.argv)
        except:
            pass

    def test_get_logo_widget(self):
        """Get logo widget"""

        ack_test = Acknowledge()
        under_test = get_logo_widget(ack_test)

        self.assertIsInstance(under_test, QWidget)
        self.assertEqual(45, under_test.height())

    def test_initialize(self):
        """Initialize Acknowledge"""

        under_test = Acknowledge()
        under_test.initialize('host', 'my_host', 'Acknowledge requested by App')

        self.assertTrue(under_test.sticky)
        self.assertFalse(under_test.notify)

        self.assertEqual('Acknowledge requested by App', under_test.ack_comment_edit.toPlainText())
