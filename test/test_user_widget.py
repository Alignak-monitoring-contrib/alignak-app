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
from PyQt5.QtWidgets import QApplication, QWidget

from alignak_app.utils.config import settings
from alignak_app.locales.locales import init_localization

settings.init_config()
init_localization()
app = QApplication(sys.argv)

from alignak_app.backend.datamanager import data_manager
from alignak_app.items.user import User

from alignak_app.qobjects.dock.user import UserQWidget


class TestUserQWidget(unittest2.TestCase):
    """
        This file test the UserQWidget class.
    """

    data_manager.database['user'] = User()
    data_manager.database['user'].data = {}

    @classmethod
    def setUpClass(cls):
        """Create QApplication"""
        try:
            cls.app = QApplication(sys.argv)
            cls.period_uuid = '59c4e38535d17b8dcb0bed46'
        except:
            pass

    def test_initialize(self):
        """Initialize UserProfile"""

        under_test = UserQWidget()

        data_manager.database['user'].data['email'] = 'mail@test'
        data_manager.database['user'].data['alias'] = 'alias'
        data_manager.database['user'].data['token'] = 'token'
        data_manager.database['user'].data['notes'] = 'notes'
        data_manager.database['user'].data['host_notifications_enabled'] = True
        data_manager.database['user'].data['service_notifications_enabled'] = True
        data_manager.database['user'].data['host_notification_period'] = 'period'
        data_manager.database['user'].data['service_notification_period'] = 'period'
        data_manager.database['user'].data['host_notification_options'] = []
        data_manager.database['user'].data['service_notification_options'] = []
        data_manager.database['user'].data['is_admin'] = True
        data_manager.database['user'].data['can_submit_commands'] = True

        self.assertIsNone(under_test.app_widget)
        self.assertIsNone(under_test.layout())

        under_test.initialize()

        self.assertIsNotNone(under_test.app_widget)
        self.assertIsNotNone(under_test.layout())

    def test_user_qwidgets(self):
        """User QWidgets Creation"""

        under_test = UserQWidget()

        main_widget_test = under_test.get_informations_widget()
        notif_widget_test = under_test.get_notifications_widget()
        host_notif_widget_test = under_test.get_hosts_notif_widget()
        services_notif_widget_test = under_test.get_services_notif_widget()

        self.assertIsInstance(main_widget_test, QWidget)
        self.assertIsInstance(notif_widget_test, QWidget)
        self.assertIsInstance(host_notif_widget_test, QWidget)
        self.assertIsInstance(services_notif_widget_test, QWidget)
