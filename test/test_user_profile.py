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

import sys

import unittest2

from alignak_app.core.utils import init_config
from alignak_app.core.backend import app_backend
from alignak_app.core.data_manager import data_manager
from alignak_app.models.item_user import User
from alignak_app.user.user_profile import UserQWidget
from alignak_app.core.locales import init_localization

from PyQt5.QtWidgets import QApplication, QWidget


class TestUserProfile(unittest2.TestCase):
    """
        TODO This file test the UserProfile class.
    """

    init_config()
    init_localization()
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

        options_test = ['d', 'u', 'r', 'f', 's', 'n']

        main_widget_test = under_test.get_main_user_widget()
        info_widget_test = under_test.get_information_widget()
        rights_widget_test = under_test.get_rights_widget()
        notes_widget_test = under_test.get_notes_widget()
        notif_widget_test = under_test.get_notifications_widget()
        host_notif_widget_test = under_test.get_hosts_notif_widget()
        services_notif_widget_test = under_test.get_services_notif_widget()
        options_widget_test = under_test.get_options_widget('hosts', options_test)

        self.assertIsInstance(main_widget_test, QWidget)
        self.assertIsInstance(info_widget_test, QWidget)
        self.assertIsInstance(rights_widget_test, QWidget)
        self.assertIsInstance(notes_widget_test, QWidget)
        self.assertIsInstance(notif_widget_test, QWidget)
        self.assertIsInstance(host_notif_widget_test, QWidget)
        self.assertIsInstance(services_notif_widget_test, QWidget)
        self.assertIsInstance(options_widget_test, QWidget)

    def test_get_realm_name(self):
        """Get Realm Name"""

        under_test = UserQWidget()
        if not app_backend.connected:
            app_backend.login()

        data_manager.database['user'].data['_realm'] = '59c4e38535d17b8dcb0bed42'
        # Realm is right
        realm_test = under_test.get_realm_name()

        # If "user" has a right realm, return is 'All'
        self.assertEqual(realm_test, 'All')

        # Change realm to a false one
        data_manager.database['user'].data['_realm'] = 'no_realm'
        realm_test = under_test.get_realm_name()

        # If "user" has a false realm, return is 'n/a'
        self.assertEqual(realm_test, 'n/a')

    def test_get_role(self):
        """Get User Role"""

        under_test = UserQWidget()

        # Simulate user data
        # Case "user"
        data_manager.database['user'].data['is_admin'] = False
        data_manager.database['user'].data['back_role_super_admin'] = False
        data_manager.database['user'].data['can_submit_commands'] = False

        role_test = under_test.get_role()

        self.assertEqual(role_test, 'user')

        # Case "power"
        data_manager.database['user'].data['can_submit_commands'] = True

        role_test = under_test.get_role()

        self.assertEqual(role_test, 'power')

        # Case "admin"
        data_manager.database['user'].data['can_submit_commands'] = True
        data_manager.database['user'].data['back_role_super_admin'] = True

        role_test = under_test.get_role()

        self.assertEqual(role_test, 'administrator')

        data_manager.database['user'].data['back_role_super_admin'] = False
        data_manager.database['user'].data['is_admin'] = True

        role_test = under_test.get_role()

        self.assertEqual(role_test, 'administrator')

    def test_get_period_name(self):
        """Get User Period Name"""

        under_test = UserQWidget()
        # under_test.get_user_data()

        period_test = under_test.get_period_name('test')

        self.assertEqual(period_test, 'n/a')

        if not app_backend.connected:
            app_backend.login()
        period_test = under_test.get_period_name(self.period_uuid)

        self.assertEqual(period_test, 'All time default 24x7')


