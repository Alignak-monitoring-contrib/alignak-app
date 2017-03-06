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

import unittest2
import sys

from alignak_app.core.action_manager import *
from alignak_app.core.backend import AppBackend

from PyQt5.QtWidgets import QApplication


class TestBanner(unittest2.TestCase):
    """
        This file test methods of ActionManager class.
    """

    test_backend = AppBackend()

    @classmethod
    def setUpClass(cls):
        """Create QApplication"""

        try:
            cls.app = QApplication(sys.argv)
        except:
            pass

    def test_action_manager_creation(self):
        """Create ActionManager"""

        under_test = ActionManager(self.test_backend)

        self.assertEqual('actionacknowledge', ACK)
        self.assertEqual('actiondowntime', DOWNTIME)
        self.assertEqual('processed', PROCESS)

        self.assertIsNotNone(under_test.app_backend)

        self.assertFalse(under_test.acks_to_check['hosts'])
        self.assertFalse(under_test.acks_to_check['services'])
        self.assertFalse(under_test.downtimes_to_check['hosts'])
        self.assertFalse(under_test.downtimes_to_check['services'])
        self.assertFalse(under_test.processed_to_check)

    def test_check_items(self):
        """ActionManager Check Items"""

        under_test = ActionManager(self.test_backend)

        actions_items = under_test.check_items()

        # If no items are added, return all list are empty
        self.assertFalse(actions_items[ACK]['hosts'])
        self.assertFalse(actions_items[ACK]['services'])
        self.assertFalse(actions_items[DOWNTIME]['hosts'])
        self.assertFalse(actions_items[DOWNTIME]['services'])
        self.assertFalse(actions_items[PROCESS])

        # Assure actions VAR are not modified
        self.assertEqual('actionacknowledge', ACK)
        self.assertEqual('actiondowntime', DOWNTIME)
        self.assertEqual('processed', PROCESS)

    def test_add_none_item(self):
        """ActionManager Add None Item"""

        under_test = ActionManager(self.test_backend)

        # test with None item
        under_test.add_item(dict())

        actions_items = under_test.check_items()

        # If no items are added, all list are empty
        self.assertFalse(under_test.acks_to_check['hosts'])
        self.assertFalse(under_test.acks_to_check['services'])
        self.assertFalse(under_test.downtimes_to_check['hosts'])
        self.assertFalse(under_test.downtimes_to_check['services'])
        self.assertFalse(under_test.processed_to_check)

        self.assertFalse(actions_items[ACK]['hosts'])
        self.assertFalse(actions_items[ACK]['services'])
        self.assertFalse(actions_items[DOWNTIME]['hosts'])
        self.assertFalse(actions_items[DOWNTIME]['services'])
        self.assertFalse(actions_items[PROCESS])

    def test_add_ack_item(self):
        """ActionManager Add ACK Item"""

        under_test = ActionManager(self.test_backend)

        self.assertFalse(under_test.acks_to_check['hosts'])
        self.assertFalse(under_test.acks_to_check['services'])

        item_with_host = {
            'action': ACK,
            'host_id': '000',
            'service_id': None
        }

        under_test.add_item(item_with_host)

        # If "service_id" is None, ACK list add to 'hosts'
        self.assertTrue(under_test.acks_to_check['hosts'])
        self.assertFalse(under_test.acks_to_check['services'])

        item_with_service = {
            'action': ACK,
            'host_id': '000',
            'service_id': '111'
        }

        under_test.add_item(item_with_service)

        # If "service_id", ACK list add to 'services'
        self.assertTrue(under_test.acks_to_check['hosts'])
        self.assertTrue(under_test.acks_to_check['services'])

    def test_add_downtime_item(self):
        """ActionManager Add DOWNTIME Item"""

        under_test = ActionManager(self.test_backend)

        self.assertFalse(under_test.downtimes_to_check['hosts'])
        self.assertFalse(under_test.downtimes_to_check['services'])

        item_with_host = {
            'action': DOWNTIME,
            'host_id': '000',
            'service_id': None
        }

        under_test.add_item(item_with_host)

        # If "service_id" is None, ACK list add to 'hosts'
        self.assertTrue(under_test.downtimes_to_check['hosts'])
        self.assertFalse(under_test.downtimes_to_check['services'])

        item_with_service = {
            'action': DOWNTIME,
            'host_id': '000',
            'service_id': '111'
        }

        under_test.add_item(item_with_service)

        # If "service_id", ACK list add to 'services'
        self.assertTrue(under_test.downtimes_to_check['hosts'])
        self.assertTrue(under_test.downtimes_to_check['services'])

    def test_add_processed_item(self):
        """ActionManager Add PROCESS Item"""

        under_test = ActionManager(self.test_backend)

        item_with_host = {
            'action': PROCESS,
            'name': 'my name',
            'post': 'item/000'
        }

        self.assertFalse(under_test.processed_to_check)

        under_test.add_item(item_with_host)

        self.assertTrue(under_test.processed_to_check)