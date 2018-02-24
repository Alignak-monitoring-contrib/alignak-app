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
from alignak_app.items.user import User
from alignak_app.utils.config import settings
from alignak_app.locales.locales import init_localization

from alignak_app.qobjects.dock.token import TokenQDialog


class TestTokenQDialog(unittest2.TestCase):
    """
        This file test methods of TokenQDialog class object
    """

    settings.init_config()
    init_localization()
    app_backend.login()

    user = User()
    user.create('_id', {'token': 'long_token'}, 'name')

    @classmethod
    def setUpClass(cls):
        """Create QApplication"""
        try:
            cls.app = QApplication(sys.argv)
        except:
            pass

    def test_initialize(self):
        """Iniatialize TokenQDialog"""

        under_test = TokenQDialog()

        self.assertIsNone(under_test.layout())
        self.assertEqual('dialog', under_test.objectName())

        data_manager.database['user'] = self.user
        under_test.initialize()

        self.assertIsNotNone(under_test.layout())
        self.assertEqual('dialog', under_test.objectName())

    def test_get_token_widget(self):
        """Get Token Qwidget"""

        token_dialog_test = TokenQDialog()
        self.assertEqual('dialog', token_dialog_test.objectName())
        data_manager.database['user'] = self.user

        under_test = token_dialog_test.get_token_widget()

        self.assertIsNotNone(under_test.layout())
        self.assertEqual('dialog', under_test.objectName())
        self.assertIsInstance(under_test, QWidget)
