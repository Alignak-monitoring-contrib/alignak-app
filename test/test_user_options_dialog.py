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
from PyQt5.Qt import QDialog
from PyQt5.QtWidgets import QApplication, QWidget

from alignak_app.utils.config import settings
from alignak_app.locales.locales import init_localization

from alignak_app.qobjects.dock.user_options import UserOptionsQDialog

settings.init_config()
init_localization()


class TestUserOptionsQDialog(unittest2.TestCase):
    """
        This file test the UserQWidget class.
    """

    host_options_test = ['d', 'u', 'r', 'f', 's']
    service_options_test = ['w', 'u', 'c', 'r', 'f', 's']

    @classmethod
    def setUpClass(cls):
        """Create QApplication"""
        try:
            cls.app = QApplication(sys.argv)
        except:
            pass

    def test_user_options_initialize(self):
        """Initialize User Options QDialog"""

        under_test = UserOptionsQDialog()

        self.assertIsNone(under_test.layout())
        self.assertEqual('dialog', under_test.objectName())
        self.assertIsInstance(under_test, QDialog)

        self.assertIsNotNone(under_test.options_labels)
        self.assertTrue('host' in under_test.options_labels)
        self.assertTrue('service' in under_test.options_labels)
        self.assertIsNotNone(under_test.titles_labels)
        self.assertTrue('host' in under_test.titles_labels)
        self.assertTrue('service' in under_test.titles_labels)

        under_test.initialize('host', self.host_options_test)

        self.assertIsNotNone(under_test.layout())

    def test_get_notifications_widget(self):
        """Get Notifications QWidget"""

        user_options_test = UserOptionsQDialog()

        under_test = user_options_test.get_notifications_widget(
            'service', self.service_options_test
        )

        self.assertIsInstance(under_test, QWidget)
        self.assertIsNotNone(under_test.layout())

        self.assertIsNotNone(user_options_test.options_labels)
        self.assertIsNotNone(user_options_test.titles_labels)

    def test_get_selected_options(self):
        """Get Selected Options"""

        under_test = UserOptionsQDialog.get_selected_options('host', self.host_options_test)

        self.assertTrue(under_test['d'])
        self.assertTrue(under_test['u'])
        self.assertTrue(under_test['r'])
        self.assertTrue(under_test['f'])
        self.assertTrue(under_test['s'])
        self.assertFalse(under_test['n'])
        self.assertTrue('c' not in under_test)
        self.assertTrue('w' not in under_test)

        under_test = UserOptionsQDialog.get_selected_options('service', self.service_options_test)

        self.assertTrue(under_test['w'])
        self.assertTrue(under_test['u'])
        self.assertTrue(under_test['c'])
        self.assertTrue(under_test['r'])
        self.assertTrue(under_test['f'])
        self.assertTrue(under_test['s'])
        self.assertFalse(under_test['n'])