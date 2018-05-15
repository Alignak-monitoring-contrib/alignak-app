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
from PyQt5.Qt import QApplication, QListWidgetItem, Qt

from alignak_app.qobjects.events.item import EventItem


class TestEventItem(unittest2.TestCase):
    """
        This file test the EventItem class and methods
    """

    @classmethod
    def setUpClass(cls):
        """Create QApplication"""
        try:
            cls.app = QApplication(sys.argv)
        except:
            pass

    def test_initialize_event_item(self):
        """Initialize EventItem"""

        under_test = EventItem()

        # Fields are None
        self.assertIsInstance(under_test, QListWidgetItem)
        self.assertIsNone(under_test.host)
        self.assertIsNone(under_test.timer)

        # Qt Data are empty
        self.assertIsNone(under_test.data(Qt.DisplayRole))
        self.assertIsNone(under_test.data(Qt.UserRole))

        under_test.initialize(
            'OK',
            'message'
        )

        # Without host parameter, only "Qt.DisplayRole" is filled
        self.assertEqual('message', under_test.data(Qt.DisplayRole))
        self.assertIsNone(under_test.host)
        self.assertIsNone(under_test.timer)
        self.assertIsNone(under_test.data(Qt.UserRole))

    def test_initialize_event_item_with_timer(self):
        """Initialize EventItem with QTimer"""

        under_test = EventItem()

        self.assertIsNone(under_test.timer)

        under_test.initialize(
            'UNKNOWN',
            'message',
            timer=True
        )

        self.assertIsNotNone(under_test.timer)

        # Timer starts only by EventsQWidget
        self.assertFalse(under_test.timer.isActive())

    def test_initialize_event_item_with_qt_userrole(self):
        """Initialize EventItem with Qt.UserRole"""

        under_test = EventItem()

        self.assertIsNone(under_test.data(Qt.UserRole))

        under_test.initialize(
            'WARNING',
            'message',
            host='_id1'
        )

        self.assertIsNotNone(under_test.data(Qt.UserRole))
        self.assertEqual('_id1', under_test.data(Qt.UserRole))

    def test_get_event_item_icon(self):
        """Get Event Item Icon"""

        # Not found = error
        under_test = EventItem.get_icon(None)
        self.assertEqual('error', under_test)

        # Found not equal to error
        under_test = EventItem.get_icon('UNREACHABLE')
        self.assertNotEqual('error', under_test)

    def test_get_event_type(self):
        """Get Event Type"""

        data_test = {
            'ls_state': 'OK',
            'ls_acknowledged': False,
            'ls_downtimed': False,
        }

        # Return state if not ack or downtimed
        under_test = EventItem.get_event_type(data_test)
        self.assertEqual('OK', under_test)

        # Return "ACK" if acknowledged
        data_test['ls_acknowledged'] = True
        under_test = EventItem.get_event_type(data_test)
        self.assertEqual('ACK', under_test)

        # Return "DOWNTIME" if downtimed
        data_test['ls_downtimed'] = True
        under_test = EventItem.get_event_type(data_test)
        self.assertEqual('DOWNTIME', under_test)
