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

from alignak_app.core.utils import init_config
from alignak_app.synthesis.services_view import ServicesView
from alignak_app.synthesis.service import Service
from alignak_app.core.action_manager import ActionManager
from alignak_app.core.backend import AppBackend

try:
    __import__('PyQt5')
    from PyQt5.QtWidgets import QApplication
except ImportError:
    from PyQt4.Qt import QApplication


class TestServicesView(unittest2.TestCase):
    """
        This file test the ServicesView class.
    """

    init_config()

    app_backend = AppBackend()
    app_backend.login()

    action_manager = ActionManager(app_backend)

    @classmethod
    def setUpClass(cls):
        """Create QApplication"""
        try:
            cls.app = QApplication(sys.argv)
        except:
            pass

    def test_display_services(self):
        """Inititalize ServicesView"""

        under_test = ServicesView(self.action_manager, self.app_backend)

        self.assertIsNotNone(under_test.layout)

        under_test.display_services(None, {'name': ''})

        self.assertIsNotNone(under_test.layout)

    def test_update_buttons(self):
        """Update Services Buttons"""

        under_test = ServicesView(self.action_manager, self.app_backend)
        under_test.display_services(None, {'name': ''})

        # If service is acknowledged, acknowledge_btn is not enable
        test_service_ack = {
            'name': 'My Service',
            'ls_state': 'WARNING',
            'ls_last_check': 0.0,
            'ls_output': 'Output of the service',
            'ls_acknowledged': True,
            'ls_downtimed': False,
        }

        service_ack = Service()
        service_ack.initialize(test_service_ack)

        under_test.update_service_buttons(service_ack)

        self.assertFalse(service_ack.acknowledge_btn.isEnabled())
        self.assertTrue(service_ack.downtime_btn.isEnabled())

        # If service is downtimed, downtime_btn is not enable
        test_service_down = {
            'name': 'My Service',
            'ls_state': 'WARNING',
            'ls_last_check': 0.0,
            'ls_output': 'Output of the service',
            'ls_acknowledged': False,
            'ls_downtimed': True,
        }

        service_down = Service()
        service_down.initialize(test_service_down)

        under_test.update_service_buttons(service_down)

        self.assertTrue(service_down.acknowledge_btn.isEnabled())
        self.assertFalse(service_down.downtime_btn.isEnabled())

        # If service is not OK, acknowledged and downtimed, buttons are enable
        test_service_not_ok = {
            'name': 'My Service',
            'ls_state': 'WARNING',
            'ls_last_check': 0.0,
            'ls_output': 'Output of the service',
            'ls_acknowledged': False,
            'ls_downtimed': False,
        }

        service_not_ok = Service()
        service_not_ok.initialize(test_service_not_ok)

        under_test.update_service_buttons(service_not_ok)

        self.assertTrue(service_not_ok.acknowledge_btn.isEnabled())
        self.assertTrue(service_not_ok.downtime_btn.isEnabled())
