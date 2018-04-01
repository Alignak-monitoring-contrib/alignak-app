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

from PyQt5.Qt import QApplication, Qt

from alignak_app.backend.datamanager import data_manager
from alignak_app.items.host import Host
from alignak_app.items.service import Service

from alignak_app.qobjects.events.item import EventItem
from alignak_app.qobjects.events.events import init_event_widget
from alignak_app.qobjects.events.spy import SpyQWidget
from alignak_app.qobjects.events.spy_list import SpyQListWidget

init_event_widget()


class TestSpyQWidgets(unittest2.TestCase):
    """
        This file test the SpyQWidget class
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
        spy_item_test.initialize('OK', 'Message', host='_id_1')

        # Fill database
        host_test = Host()
        host_test.create(
            '_id_1',
            {
                '_id': '_id_1',
                'ls_downtimed': False,
                'ls_acknowledged': False,
                'active_checks_enabled': True,
                'passive_checks_enabled': True,
                '_overall_state_id': 4,
                'ls_state': 'DOWN'
            },
            'hostname'
        )
        data_manager.update_database('host', [host_test])

        # No item spy, so item is None
        self.assertIsNone(under_test.spy_list_widget.item(1))
        self.assertFalse(under_test.spy_list_widget.spied_hosts)

        # Spy host
        under_test.spy_list_widget.add_spy_host(host_test.item_id)

        # Assert EventItem have same host "_id" that the one added
        self.assertEqual(spy_item_test.host, under_test.spy_list_widget.item(0).host)
        self.assertEqual(['_id_1'], under_test.spy_list_widget.spied_hosts)

        # Set this item to current one and add it to spy list
        under_test.spy_list_widget.setCurrentRow(0)
        under_test.spy_list_widget.setCurrentItem(under_test.spy_list_widget.item(0))

        under_test.remove_event()

        # Event is no more here
        self.assertNotEqual(spy_item_test.host, under_test.spy_list_widget.item(0).host)
        self.assertFalse(under_test.spy_list_widget.spied_hosts)

    def test_send_spy_events(self):
        """Send Spy Events"""

        init_event_widget()
        under_test = SpyQWidget()
        under_test.initialize()

        # Hint item is here
        self.assertEqual(1, under_test.spy_list_widget.count())

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
                '_overall_state_id': 4,
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
                '_overall_state_id': 4,
                'ls_state': 'DOWN'
            },
            'hostname'
        )
        data_manager.update_database('host', [host_test, host_test_2])

        under_test.spy_list_widget.add_spy_host('spy1')
        under_test.spy_list_widget.add_spy_host('spy2')

        # Item hint have been removed, host spied added
        self.assertEqual(2, under_test.spy_list_widget.count())

        under_test.send_spy_events()

        # Sending events does not modify spy list widget count
        self.assertEqual(2, under_test.spy_list_widget.count())

    def test_manage_host_events_with_wrong_row(self):
        """Manage Host Events With Wrong Row"""

        under_test = SpyQWidget()
        under_test.initialize()

        # Hint item in spy list widget, 0 item in host list widget
        self.assertEqual(1, under_test.spy_list_widget.count())
        self.assertEqual(0, under_test.host_list_widget.count())

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
                '_overall_state_id': 4,
                'ls_state': 'DOWN'
            },
            'hostname'
        )
        data_manager.update_database('host', [host_test])

        # Spy this host
        under_test.spy_list_widget.add_spy_host(host_test.item_id)

        # Host have been added in list widget, 0 item in host list widget
        self.assertEqual(1, under_test.spy_list_widget.count())
        self.assertEqual(host_test.item_id, under_test.spy_list_widget.item(0).host)
        self.assertEqual(0, under_test.host_list_widget.count())

        # Manage problems
        under_test.manage_host_events(-1)

        # Host list equal to 0 with row equal to -1
        self.assertEqual(0, under_test.host_list_widget.count())

    def test_manage_host_events_with_valid_rows(self):
        """Manage Host Events With Valid Rows"""

        under_test = SpyQWidget()
        under_test.initialize()

        # Filling "host" database
        host_test = Host()
        host_test.create(
            'spy1',
            {
                '_id': 'spy1',
                'ls_downtimed': False,
                'ls_acknowledged': False,
                'active_checks_enabled': True,
                'passive_checks_enabled': True,
                '_overall_state_id': 4,
                'ls_state': 'DOWN'
            },
            'hostname'
        )
        data_manager.update_database('host', [host_test])

        # Spy this host and set current row
        under_test.spy_list_widget.add_spy_host(host_test.item_id)
        under_test.spy_list_widget.setCurrentRow(0)

        # "(new !)" is added to new spy host
        self.assertEqual(
            'Host Hostname, current state: DOWN (new !)',
            under_test.spy_list_widget.item(0).data(Qt.DisplayRole)
        )

        # Manage problems with a valid row
        under_test.manage_host_events(under_test.spy_list_widget.currentRow())

        # Host list equal to 1, No services are attached to host
        self.assertEqual(1, under_test.host_list_widget.count())
        self.assertEqual(
            'Hostname is DOWN. No services.',
            under_test.host_list_widget.item(0).data(Qt.DisplayRole)
        )
        # "(new !)" is removed
        self.assertEqual(
            'Host Hostname, current state: DOWN ',
            under_test.spy_list_widget.item(0).data(Qt.DisplayRole)
        )

        # Fill "services" database attached to host
        service = Service()
        service.create(
            '_id1',
            {
                'host': 'spy1',
                'ls_state': 'CRITICAL',
                'ls_acknowledged': False,
                'ls_downtimed': False,
            },
            'service_name'
        )
        service_2 = Service()
        service_2.create(
            '_id2',
            {
                'host': 'spy1',
                'ls_state': 'OK',
                'ls_acknowledged': False,
                'ls_downtimed': False,
            },
            'service2_name'
        )
        data_manager.update_database('service', [service, service_2])

        # Manage problems again
        under_test.manage_host_events(under_test.spy_list_widget.currentRow())

        # Host list equal to 1, cause one service is CRITICAL
        self.assertEqual(1, under_test.host_list_widget.count())
        self.assertEqual(
            'Service Service_Name is CRITICAL',
            under_test.host_list_widget.item(0).data(Qt.DisplayRole)
        )

        # If CRITICAL service is removed, text change
        data_manager.remove_item('service', '_id1')

        # Manage problems again
        under_test.manage_host_events(under_test.spy_list_widget.currentRow())

        # Host list equal to 1, cause one service is CRITICAL
        self.assertEqual(1, under_test.host_list_widget.count())
        self.assertEqual(
            'Hostname is DOWN. Services of host seems managed.',
            under_test.host_list_widget.item(0).data(Qt.DisplayRole)
        )
