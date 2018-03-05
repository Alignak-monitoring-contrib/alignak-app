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

import sys

import unittest2
from PyQt5.QtWidgets import QApplication, QTimeEdit, QDateTimeEdit

from alignak_app.utils.config import settings
from alignak_app.locales.locales import init_localization

from alignak_app.qobjects.common.actions import AckQDialog, DownQDialog

settings.init_config()
init_localization()


class TestActionsQDialogs(unittest2.TestCase):
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

    def test_initialize_acknowledge(self):
        """Initialize Acknowledge"""

        under_test = AckQDialog()
        under_test.initialize('host', 'my_host', 'Acknowledge requested by App')

        self.assertTrue(under_test.sticky)
        self.assertFalse(under_test.notify)

        self.assertEqual('Acknowledge requested by App', under_test.ack_comment_edit.toPlainText())

    def test_initialize_downtime(self):
        """Initialize Downtime"""

        under_test = DownQDialog()
        under_test.initialize('host', 'my_host', 'Downtime requested by App')

        self.assertTrue(under_test.fixed)
        self.assertTrue(under_test.duration)
        self.assertIsInstance(under_test.duration, QTimeEdit)
        self.assertEqual(under_test.duration_to_seconds(), 14400)
        self.assertTrue(under_test.start_time)
        self.assertIsInstance(under_test.start_time, QDateTimeEdit)
        self.assertTrue(under_test.end_time)
        self.assertIsInstance(under_test.end_time, QDateTimeEdit)
        self.assertEqual(
            under_test.end_time.dateTime().toTime_t() - under_test.start_time.dateTime().toTime_t(),
            7200
        )

        self.assertEqual('Downtime requested by App', under_test.comment_edit.toPlainText())
