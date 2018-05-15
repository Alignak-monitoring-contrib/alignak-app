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

"""
    Dialogs
    +++++++
    Dialogs manage global QDialogs
"""

from logging import getLogger

from PyQt5.Qt import QTextEdit, Qt, QIcon, QDialog, QVBoxLayout, QWidget, QLabel, QPushButton
from PyQt5.Qt import QLineEdit, QRegExpValidator, QRegExp

from alignak_app.utils.config import settings

from alignak_app.qobjects.common.widgets import center_widget, get_logo_widget

logger = getLogger(__name__)


class EditQDialog(QDialog):
    """
        Class who create Edit QDialog to edit text in Alignak-app
    """

    def __init__(self, parent=None):
        super(EditQDialog, self).__init__(parent)
        self.setWindowTitle('Edit Dialog')
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet(settings.css_style)
        self.setWindowIcon(QIcon(settings.get_image('icon')))
        self.setObjectName('dialog')
        self.setFixedSize(300, 300)
        # Fields
        self.text_edit = QTextEdit()
        self.old_text = ''

    def initialize(self, title, text):
        """
        Initialize QDialog for UserNotesQDialog

        :param title: title of the QDialog
        :type title: str
        :param text: text to edit
        :type text: str
        """

        self.old_text = text
        center_widget(self)

        # Main status_layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

        main_layout.addWidget(get_logo_widget(self, title))

        text_title = QLabel(_("Edit your text:"))
        text_title.setObjectName('subtitle')
        main_layout.addWidget(text_title)
        main_layout.setAlignment(text_title, Qt.AlignCenter)

        main_layout.addWidget(self.get_text_widget())

    def get_text_widget(self):
        """
        Return text QWidget with QTextEdit

        :return: text QWidget
        :rtype: QWidget
        """

        text_widget = QWidget()
        text_widget.setObjectName('dialog')
        text_layout = QVBoxLayout()
        text_widget.setLayout(text_layout)

        self.text_edit.setPlaceholderText(_('type your text...'))
        self.text_edit.setText(self.old_text)
        text_layout.addWidget(self.text_edit)

        # Accept button
        accept_btn = QPushButton(_('Confirm'), self)
        accept_btn.clicked.connect(self.accept_text)
        accept_btn.setObjectName('valid')
        accept_btn.setMinimumHeight(30)
        text_layout.addWidget(accept_btn)

        return text_widget

    def accept_text(self):
        """
        Set Edit QDialog to Rejected or Accepted (prevent to patch for nothing)

        """

        if self.old_text == self.text_edit.toPlainText():
            self.reject()
        elif not self.old_text or self.old_text.isspace():
            if not self.text_edit.toPlainText() or self.text_edit.toPlainText().isspace():
                self.reject()
            else:
                self.accept()
        else:
            self.accept()


class MessageQDialog(QDialog):
    """
        Class who create a Message QDialog to display texts in Alignak-app
    """

    def __init__(self, parent=None):
        super(MessageQDialog, self).__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet(settings.css_style)
        self.setWindowIcon(QIcon(settings.get_image('icon')))
        self.setFixedSize(500, 200)
        self.setObjectName('dialog')

    def initialize(self, widgettitle, dialog, title, text):
        """
        Initialize QDialog for PasswordDialog

        :param widgettitle: title of the QDialog
        :type widgettitle: str
        :param dialog: type of dialog ('text' or 'error')
        :type dialog: str
        :param title: title of text to display
        :type title: str
        :param text: text to display
        :type text: str
        """

        center_widget(self)

        # Main status_layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

        main_layout.addWidget(get_logo_widget(self, widgettitle))
        main_layout.addWidget(self.get_message_widget(dialog, title, text))

    def get_message_widget(self, dialog, title, text):
        """
        Return colored message QWidget

        :param dialog: type of dialog ('text' or 'error')
        :type dialog: str
        :param title: title of text to display
        :type title: str
        :param text: text to display
        :type text: str
        :return: message QWidget
        :rtype: QWidget
        """

        # Token QWidget
        token_widget = QWidget()
        token_widget.setObjectName('dialog')
        token_layout = QVBoxLayout()
        token_widget.setLayout(token_layout)

        token_title = QLabel(title)
        token_title.setObjectName('itemtitle')
        token_layout.addWidget(token_title)
        token_layout.setAlignment(token_title, Qt.AlignCenter)

        token_label = QLabel(text)
        token_label.setObjectName(dialog)
        token_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        token_label.setWordWrap(True)
        token_layout.addWidget(token_label)

        # Login button
        accept_btn = QPushButton('OK', self)
        accept_btn.clicked.connect(self.accept)
        accept_btn.setObjectName('ok')
        accept_btn.setMinimumHeight(30)
        token_layout.addWidget(accept_btn)

        return token_widget


class ValidatorQDialog(QDialog):
    """
        Class who create Validator QDialog to edit text in Alignak-app with regexp to validate
    """

    def __init__(self, parent=None):
        super(ValidatorQDialog, self).__init__(parent)
        self.setWindowTitle('Edit Dialog')
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet(settings.css_style)
        self.setWindowIcon(QIcon(settings.get_image('icon')))
        self.setObjectName('dialog')
        self.setFixedSize(250, 200)
        # Fields
        self.line_edit = QLineEdit()
        self.valid_text = QLabel()
        self.validator = QRegExpValidator()
        self.old_text = ''

    def initialize(self, title, text, regexp):
        """
        Initialize QDialog for ValidatorQDialog

        :param title: title of the QDialog
        :type title: str
        :param text: text to edit
        :type text: str
        :param regexp: regular expression to validate
        :type regexp: str
        """

        self.old_text = text
        center_widget(self)

        # Main status_layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

        main_layout.addWidget(get_logo_widget(self, title))

        text_title = QLabel(_("Edit your text:"))
        text_title.setObjectName('subtitle')
        main_layout.addWidget(text_title)
        main_layout.setAlignment(text_title, Qt.AlignCenter)

        main_layout.addWidget(self.get_text_widget(regexp))

    def get_text_widget(self, regexp):
        """
        Return text QWidget with QTextEdit

        :return: text QWidget
        :rtype: QWidget
        """

        text_widget = QWidget()
        text_widget.setObjectName('dialog')
        text_layout = QVBoxLayout()
        text_widget.setLayout(text_layout)

        text_layout.addWidget(self.valid_text)

        qreg_exp = QRegExp(regexp)
        self.validator.setRegExp(qreg_exp)
        self.line_edit.setPlaceholderText(_('type your text...'))
        self.line_edit.setText(self.old_text)
        self.line_edit.setValidator(self.validator)
        self.line_edit.setFixedHeight(25)
        self.line_edit.textChanged.connect(self.check_text)
        text_layout.addWidget(self.line_edit)

        # Accept button
        accept_btn = QPushButton(_('Confirm'), self)
        accept_btn.clicked.connect(self.accept_text)
        accept_btn.setObjectName('valid')
        accept_btn.setMinimumHeight(30)
        text_layout.addWidget(accept_btn)

        return text_widget

    def check_text(self):
        """
        Valid email with ``QRegExpValidator`` and inform user

        """

        state = self.validator.validate(self.line_edit.text(), 0)[0]
        if state == QRegExpValidator.Acceptable:
            text = 'Valid email'
            color = '#27ae60'  # green
        else:
            text = 'Invalid email !'
            color = '#e67e22'  # orange

        self.valid_text.setStyleSheet('QLabel { color: %s; }' % color)
        self.valid_text.setText(text)

    def accept_text(self):  # pragma: no cover
        """
        Set Edit QDialog to Rejected or Accepted (prevent to patch for nothing)

        """

        state = self.validator.validate(self.line_edit.text(), 0)[0]
        if self.old_text == self.line_edit.text():
            self.reject()
        elif not self.old_text or self.old_text.isspace():
            if not self.line_edit.text() or self.line_edit.text().isspace():
                self.reject()
            else:
                if state == QRegExpValidator.Acceptable:
                    self.accept()
                else:
                    self.reject()
        elif not self.line_edit.text() or self.line_edit.text().isspace():
            self.line_edit.setText('')
            self.accept()
        else:
            if state == QRegExpValidator.Acceptable:
                self.accept()
            else:
                self.reject()
