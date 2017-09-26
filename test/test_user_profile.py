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
from alignak_app.core.backend import AppBackend
from alignak_app.user.user_profile import UserProfile
from alignak_app.core.locales import init_localization

from PyQt5.QtWidgets import QApplication, QWidget


class TestUserProfile(unittest2.TestCase):
    """
        This file test the UserProfile class.
    """

    init_config()
    init_localization()

    @classmethod
    def setUpClass(cls):
        """Create QApplication"""
        try:
            cls.app = QApplication(sys.argv)
            cls.period_uuid = '59c4e38535d17b8dcb0bed46'
            cls.app_backend = AppBackend()
            cls.app_backend.login()
        except:
            pass

    def test_initialize(self):
        """Initialize UserProfile"""

        under_test = UserProfile(self.app_backend)

        self.assertTrue(under_test.app_backend)
        self.assertFalse(under_test.user)
        self.assertIsNone(under_test.app_widget)
        self.assertIsNone(under_test.layout())

        under_test.initialize()

        self.assertTrue(under_test.app_backend)
        self.assertTrue(under_test.user)
        self.assertIsNotNone(under_test.app_widget)
        self.assertIsNotNone(under_test.layout())

    def test_get_user_data(self):
        """Get user data"""

        under_test = UserProfile(self.app_backend)

        self.assertTrue(under_test.app_backend)
        self.assertFalse(under_test.user)

        under_test.get_user_data()

        self.assertTrue(under_test.app_backend)
        self.assertTrue(under_test.user)

    def test_user_qwidgets(self):
        """User QWidgets Creation"""

        under_test = UserProfile(self.app_backend)
        under_test.get_user_data()

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

        under_test = UserProfile(self.app_backend)
        if not under_test.app_backend.connected:
            under_test.app_backend.login()
        self.assertIsNotNone(under_test.app_backend)

        realm_test = under_test.get_realm_name()

        # If "user" is False, return "n/a"
        self.assertEqual(realm_test, 'n/a')

        under_test.get_user_data()
        self.assertTrue(under_test.user)
        realm_test = under_test.get_realm_name()

        # If "user" is True, Realm is return
        self.assertEqual(realm_test, 'All')

    def test_get_role(self):
        """Get User Role"""

        under_test = UserProfile(self.app_backend)

        # Simulate user data
        # Case "user"
        under_test.user = {
            'is_admin': False,
            'back_role_super_admin': False,
            'can_submit_commands': False
        }

        role_test = under_test.get_role()

        self.assertEqual(role_test, 'user')

        # Case "power"
        under_test.user['can_submit_commands'] = True

        role_test = under_test.get_role()

        self.assertEqual(role_test, 'power')

        # Case "admin"
        under_test.user['can_submit_commands'] = True
        under_test.user['back_role_super_admin'] = True

        role_test = under_test.get_role()

        self.assertEqual(role_test, 'administrator')

        under_test.user['back_role_super_admin'] = False
        under_test.user['is_admin'] = True

        role_test = under_test.get_role()

        self.assertEqual(role_test, 'administrator')

    def test_get_period_name(self):
        """Get User Period Name"""

        under_test = UserProfile(self.app_backend)
        under_test.get_user_data()

        period_test = under_test.get_period_name('test')

        self.assertEqual(period_test, 'n/a')

        if not under_test.app_backend.connected:
            under_test.app_backend.login()
        period_test = under_test.get_period_name(self.period_uuid)

        self.assertEqual(period_test, 'All time default 24x7')


