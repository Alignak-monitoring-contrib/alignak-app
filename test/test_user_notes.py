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
from PyQt5.Qt import QSize, QDialog
from PyQt5.QtWidgets import QApplication, QWidget

from alignak_app.utils.config import settings
from alignak_app.locales.locales import init_localization

from alignak_app.qobjects.dock.user_notes import UserNotesQDialog

settings.init_config()
init_localization()


class TestUserNotesQDialog(unittest2.TestCase):
    """
        This file test the UserQWidget class.
    """

    @classmethod
    def setUpClass(cls):
        """Create QApplication"""
        try:
            cls.app = QApplication(sys.argv)
        except:
            pass

    def test_initialize(self):
        """INitialize UserNotes QDialog"""

        under_test = UserNotesQDialog()

        self.assertIsNotNone(under_test.notes_edit)
        self.assertEqual(QSize(300, 300), under_test.size())
        self.assertIsNone(under_test.layout())
        self.assertIsInstance(under_test, QDialog)
        self.assertEqual('dialog', under_test.objectName())

        under_test.initialize('User notes')

        self.assertIsNotNone(under_test.layout())
        self.assertEqual('User notes', under_test.notes_edit.toPlainText())

    def test_get_user_notes_widget(self):
        """Get User Notes QWidget"""

        user_notes_test = UserNotesQDialog()

        under_test = user_notes_test.get_user_notes_widget()

        self.assertIsNotNone(under_test)
        self.assertIsInstance(under_test, QWidget)
        self.assertEqual('', user_notes_test.notes_edit.toPlainText())