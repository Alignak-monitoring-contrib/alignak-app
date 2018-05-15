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
from PyQt5.Qt import QApplication, QListWidget

from alignak_app.backend.datamanager import data_manager
from alignak_app.items.event import Event

from alignak_app.qobjects.events.item import EventItem
from alignak_app.qobjects.events.events import EventsQWidget, get_events_widget, send_event
from alignak_app.qobjects.events.events import init_event_widget


class TestEventsQWidget(unittest2.TestCase):
    """
        This file test the EventsQWidget class and methods
    """

    @classmethod
    def setUpClass(cls):
        """Create QApplication"""
        try:
            cls.app = QApplication(sys.argv)
        except:
            pass

    def test_initialize_events_widget(self):
        """Initialize EventsQWidget"""

        under_test = EventsQWidget()

        self.assertFalse(under_test.events_list)
        self.assertTrue(under_test.timer)

        under_test.initialize()

        self.assertTrue(under_test.events_list)
        self.assertIsInstance(under_test.events_list, QListWidget)
        self.assertTrue(under_test.timer)

    def test_send_datamanager_events(self):
        """Send Data Manager Events"""

        under_test = EventsQWidget()
        under_test.initialize()

        self.assertEqual(1, under_test.events_list.count())

        under_test.send_datamanager_events()

        # No events in datamanager
        self.assertEqual(1, under_test.events_list.count())

        # Fill datamanager with events
        event = Event()
        event.create(
            '_id1',
            {
                'event_type': 'OK',
                'message': 'HOST;host_one;UP;imported_admin;output of host one',
                'host': '_id1',
                '_updated': 'Thu, 22 Mar 2018 12:30:41 GMT'
            },
            '_id1'
        )
        event_2 = Event()
        event_2.create(
            '_id2',
            {
                'event_type': 'OK',
                'message': 'HOST;host_two;DOWN;imported_admin;output of host two',
                'host': '_id1',
                '_updated': 'Thu, 22 Mar 2018 12:30:41 GMT'
            },
            '_id2'
        )
        data_manager.update_database('notifications', [event, event_2])

        under_test.send_datamanager_events()

        # Events are sent
        self.assertEqual(3, under_test.events_list.count())

    def test_add_event(self):
        """Add Event"""

        under_test = EventsQWidget()
        under_test.initialize()

        # Equal to one because of Welcome message
        self.assertEqual(1, under_test.events_list.count())

        under_test.add_event('OK', 'message')

        # Message is added
        self.assertEqual(2, under_test.events_list.count())

    def test_event_exist(self):
        """Check Event Exist"""

        under_test = EventsQWidget()
        under_test.initialize()

        # Add a event with Qt.UserRole
        under_test.add_event(
            'CRITICAL',
            'Service is CRITICAL',
            host='_id1'
        )
        self.assertEqual(2, under_test.events_list.count())

        exist_test = under_test.event_exist('Service is OK')

        # Event with message "Service is OK" does not exist
        self.assertFalse(exist_test)

        exist_test = under_test.event_exist('Service is CRITICAL')

        # Event with message "Service is CRITICAL" does not exist
        self.assertTrue(exist_test)

    def test_remove_timer_event(self):
        """Remove Timer EventItem"""

        under_test = EventsQWidget()
        under_test.initialize()

        # Add EventItem to QListWidget
        event = EventItem()
        event.initialize(
            'OK', 'message', timer=True
        )
        under_test.events_list.insertItem(0, event)
        self.assertEqual(2, under_test.events_list.count())

        under_test.remove_timer_event(event)

        # Event is removed
        self.assertEqual(1, under_test.events_list.count())

    def test_remove_event(self):
        """Remove EventItem"""

        under_test = EventsQWidget()
        under_test.initialize()

        # Welcome message is here
        self.assertEqual(1, under_test.events_list.count())

        # Set current Row and remove item
        under_test.events_list.setCurrentRow(0)
        under_test.remove_event()

        # Welcome message have been removed
        self.assertEqual(0, under_test.events_list.count())

        # Add EventItem to QListWidget
        event = EventItem()
        event.initialize(
            'OK', 'message', timer=True
        )
        under_test.events_list.insertItem(0, event)
        self.assertEqual(1, under_test.events_list.count())

        under_test.remove_event(event)

        # Event is removed
        self.assertEqual(0, under_test.events_list.count())

    def test_get_events_widget(self):
        """Get Events QWidget"""

        under_test = get_events_widget()

        self.assertIsInstance(under_test, EventsQWidget)

        self.assertIsNotNone(under_test.events_list)
        self.assertIsInstance(under_test.events_list, QListWidget)
        self.assertTrue(under_test.timer)

    def test_send_event(self):
        """Send Event by Access Function"""

        init_event_widget()
        under_test = get_events_widget()

        # Welcome message is here
        self.assertEqual(1, under_test.events_list.count())

        send_event('DOWN', 'message')

        # Event is sent
        self.assertEqual(2, under_test.events_list.count())
