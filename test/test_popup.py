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
    from PyQt5.QtWidgets import QApplication
except ImportError:
    from PyQt4.Qt import QApplication


class TestPopup(unittest2.TestCase):
    """
        This file test the AppPopup class.
    """

    config_file = get_alignak_home() + '/alignak_app/settings.cfg'
    config = configparser.ConfigParser()
    config.read(config_file)

    @classmethod
    def setUpClass(cls):
        """Create QApplication"""
        try:
            cls.app = QApplication(sys.argv)
        except:
            pass

    def test_initialize_notification(self):
        """Inititalize Notification"""

        under_test = AppPopup()

        self.assertIsNone(under_test.config)
        self.assertIsNone(under_test.state)
        self.assertIsNone(under_test.msg_label)

        # Create all the label
        under_test.initialize_notification(TestPopup.config)

        self.assertIsNotNone(under_test.config)
        self.assertEqual('state', under_test.state.objectName())
        self.assertEqual('msg', under_test.msg_label.objectName())


    def test_send_notifications(self):
        """Send Notification"""
        under_test = AppPopup()

        under_test.initialize_notification(TestPopup.config)

        self.assertEqual('', under_test.state.text())
        self.assertEqual('', under_test.msg_label.text())

        # Simulate dicts of states
        hosts_states = dict(
            up= 1,
            down=1,
            unreachable=1
        )
        services_states = dict(
            ok=-1,
            warning=1,
            critical=1,
            unknown=1
        )

        # Send a CRITICAL notification
        under_test.send_notification('CRITICAL', hosts_states, services_states)
        expected_content = 'AlignakApp has something broken... \nPlease Check your logs !'

        self.assertEqual('CRITICAL', under_test.state.text())
        self.assertEqual(expected_content, under_test.msg_label.text())
