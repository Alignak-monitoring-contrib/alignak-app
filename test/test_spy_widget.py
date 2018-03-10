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

from PyQt5.Qt import QApplication

from alignak_app.backend.datamanager import data_manager
from alignak_app.items.host import Host

from alignak_app.qobjects.events.spy import SpyQWidget, SpyQListWidget
from alignak_app.qobjects.events.item import EventItem
from alignak_app.qobjects.events.events import init_event_widget

init_event_widget()


class TestDataManager(unittest2.TestCase):
    """
        This file test the SpyQWidget, SpyQListWidget classes.
    """

    @classmethod
    def setUpClass(cls):
        """Create QApplication"""
        try:
            cls.app = QApplication(sys.argv)
        except:
            pass

    def test_initialize(self):
        """Initialize SpyQWidget"""

        under_test = SpyQWidget()

        self.assertIsNotNone(under_test.spy_list_widget)
        self.assertIsInstance(under_test.spy_list_widget, SpyQListWidget)
        self.assertIsNone(under_test.spy_list_widget.item(0))

        under_test.initialize()

        self.assertIsNotNone(under_test.spy_list_widget)
        self.assertIsInstance(under_test.spy_list_widget, SpyQListWidget)
        self.assertIsNotNone(under_test.spy_list_widget.item(0))

    def test_remove_event(self):
        """Remove Spy Event Item"""

        under_test = SpyQWidget()
        under_test.initialize()

        spy_item_test = EventItem()
        spy_item_test.initialize('OK', 'Message', spied_on=True, host='_id_1')

        self.assertIsNone(under_test.spy_list_widget.item(1))

        under_test.spy_list_widget.addItem(spy_item_test)

        # Assert EventItem is same that the one added
        self.assertEqual(spy_item_test, under_test.spy_list_widget.item(1))

        # Set this item to current one and add it to spy list
        under_test.spy_list_widget.setCurrentItem(under_test.spy_list_widget.item(1))
        under_test.spy_list_widget.spied_hosts.append('_id_1')

        under_test.remove_event()

        # Event is no more here
        self.assertIsNone(under_test.spy_list_widget.item(1))

    def test_send_spy_events(self):
        """Send Spy Events"""

        under_test = SpyQWidget()
        under_test.initialize()

        # Hint item is here
        self.assertEqual(1, under_test.spy_list_widget.count())
        self.assertFalse(under_test.spied_to_send)

        # Filling database
        host_test = Host()
        host_test.create(
            'spy1',
            {
                '_id': 'spy1',
                'ls_downtimed': False,
                'ls_acknowledged': False,
                'active_checks_enabled': True,
                'passive_checks_enabled': True,
                'ls_state': 'DOWN'
            },
            'hostname'
        )
        host_test_2 = Host()
        host_test_2.create(
            'spy2',
            {
                '_id': 'spy2',
                'ls_downtimed': False,
                'ls_acknowledged': False,
                'active_checks_enabled': True,
                'passive_checks_enabled': True,
                'ls_state': 'DOWN'
            },
            'hostname'
        )
        data_manager.update_database('host', [host_test, host_test_2])

        under_test.spy_list_widget.add_spy_host('spy1')
        under_test.spy_list_widget.add_spy_host('spy2')

        # Item hint have been removed, host spied added
        self.assertEqual(2, under_test.spy_list_widget.count())
        self.assertFalse(under_test.spied_to_send)

        under_test.send_spy_events()

        # Spy event to send has been filled, left only 'spy2'
        self.assertEqual(2, under_test.spy_list_widget.count())
        self.assertTrue(under_test.spied_to_send)
        self.assertEqual(1, len(under_test.spied_to_send))
        self.assertTrue('spy2' in under_test.spied_to_send)
