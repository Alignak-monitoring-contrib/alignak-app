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
from PyQt5.Qt import QApplication, QWidget

from alignak_app.backend.backend import app_backend
from alignak_app.backend.datamanager import data_manager
from alignak_app.utils.config import settings
from alignak_app.locales.locales import init_localization
from alignak_app.items.user import User

from alignak_app.qobjects.alignak.alignak import AlignakQWidget


class TestAlignakQWidget(unittest2.TestCase):
    """
        This file test methods of AlignakQWidget class object
    """

    settings.init_config()
    init_localization()
    app_backend.login()

    # User data test
    user = User()
    user_keys = User.get_request_model('test')['projection']
    user_data_test = {}
    for key in user_keys:
        if 'host_notifications_enabled' in key or 'service_notifications_enabled' in key:
            user_data_test[key] = True
        else:
            user_data_test[key] = 'test'
    user.create('_id', user_data_test, 'admin')

    @classmethod
    def setUpClass(cls):
        """Create QApplication"""
        try:
            cls.app = QApplication(sys.argv)
        except:
            pass

    def test_initialize_status_qwidget(self):
        """Initialize StatusQWidget"""

        under_test = AlignakQWidget()

        self.assertIsNotNone(under_test.backend_connected)
        self.assertIsNotNone(under_test.status_btn)
        self.assertIsNotNone(under_test.status_dialog)
        self.assertIsNotNone(under_test.profile_btn)
        self.assertIsNotNone(under_test.profile_widget)
        self.assertFalse(under_test.refresh_timer.isActive())

        self.assertIsInstance(under_test, QWidget)

        data_manager.update_database('user', self.user)
        under_test.initialize()

        self.assertIsNotNone(under_test.backend_connected)
        self.assertIsNotNone(under_test.status_btn)
        self.assertIsNotNone(under_test.status_dialog)
        self.assertIsNotNone(under_test.profile_btn)
        self.assertIsNotNone(under_test.profile_widget)
        self.assertTrue(under_test.refresh_timer.isActive())