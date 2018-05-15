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
from PyQt5.Qt import QApplication, QWidget, QTimer

from alignak_app.utils.config import settings
from alignak_app.locales.locales import init_localization

from alignak_app.qobjects.common.dialogs import MessageQDialog, EditQDialog, ValidatorQDialog


class TestMessageQDialog(unittest2.TestCase):
    """
        This file test methods of MessageQDialog class object
    """

    settings.init_config()
    init_localization()

    @classmethod
    def setUpClass(cls):
        """Create QApplication"""
        try:
            cls.app = QApplication(sys.argv)
        except:
            pass

    def test_initialize_msg_dialog(self):
        """Initialize MessageQDialog"""

        under_test = MessageQDialog()

        self.assertIsNone(under_test.layout())
        self.assertEqual('dialog', under_test.objectName())

        under_test.initialize(
            'widgettitle',
            'text',
            'title',
            'Text to display'
        )

        self.assertIsNotNone(under_test.layout())
        self.assertEqual('dialog', under_test.objectName())

    def test_get_message_widget(self):
        """Get Message QWidget"""

        msg_dialog_test = MessageQDialog()
        self.assertEqual('dialog', msg_dialog_test.objectName())

        under_test = msg_dialog_test.get_message_widget(
            'text',
            'title',
            'Text to display'
        )

        self.assertIsNotNone(under_test.layout())
        self.assertEqual('dialog', under_test.objectName())
        self.assertIsInstance(under_test, QWidget)

    def test_initialize_edit_dialog(self):
        """Initialize EditQDialog"""

        under_test = EditQDialog()

        self.assertFalse(under_test.old_text)
        self.assertIsNotNone(under_test.text_edit)

        under_test.initialize('title', 'text to edit')

        self.assertEqual('text to edit', under_test.old_text)
        self.assertEqual('text to edit', under_test.text_edit.toPlainText())

    def test_get_text_widget(self):
        """Get Text QWidget"""

        under_test = EditQDialog()

        under_test.old_text = 'old text'

        text_widget_test = under_test.get_text_widget()

        self.assertIsInstance(text_widget_test, QWidget)
        self.assertEqual('old text', under_test.text_edit.toPlainText())

    def test_edit_dialog_accept_text(self):
        """EditQDialog Accept Text"""

        under_test = EditQDialog()
        under_test.initialize('title', 'text to edit')

        under_test.text_edit.setText('text to edit')

        timer = QTimer()
        timer.timeout.connect(under_test.accept_text)
        timer.start(0.5)

        # Text is same so refused
        self.assertEqual(EditQDialog.Rejected, under_test.exec())

        under_test.text_edit.setText('text have been edited')
        timer.start(0.5)

        # Accepted because text have changed
        self.assertEqual(EditQDialog.Accepted, under_test.exec())

        # Reset text to empty and spaces
        under_test.old_text = ''
        under_test.text_edit.setText('    ')

        timer.start(0.5)

        # Rejected because there is nothing to change
        self.assertEqual(EditQDialog.Rejected, under_test.exec())

        under_test.old_text = ''
        under_test.text_edit.setText('New text')

        timer.start(0.5)

        # Accepted even if old text is empty
        self.assertEqual(EditQDialog.Accepted, under_test.exec())

    def test_initialize_validator_dialog(self):
        """Initialize ValidatorQDialog"""

        under_test = ValidatorQDialog()

        self.assertTrue(under_test.line_edit)
        self.assertTrue(under_test.valid_text)
        self.assertTrue(under_test.validator)
        self.assertFalse(under_test.old_text)

        under_test.initialize('title', 'text', '[a-z]')

        self.assertTrue(under_test.line_edit)
        self.assertTrue(under_test.valid_text)
        self.assertTrue(under_test.validator)
        self.assertTrue(under_test.old_text)

    def testvalidator_dialog_check_state(self):
        """Check State ValidatorQDialog"""

        under_test = ValidatorQDialog()

        under_test.initialize(
            'title',
            '',
            r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-]+.+$)"
        )

        self.assertEqual('', under_test.valid_text.text())
        self.assertEqual('', under_test.line_edit.text())
        self.assertEqual('', under_test.old_text)

        under_test.check_text()

        self.assertEqual('Invalid email !', under_test.valid_text.text())
        self.assertEqual('', under_test.line_edit.text())
        self.assertEqual('', under_test.old_text)

        under_test.line_edit.setText('contact@alignak.net')

        under_test.check_text()

        self.assertEqual('Valid email', under_test.valid_text.text())
        self.assertEqual('contact@alignak.net', under_test.line_edit.text())
