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
    User Notes
    ++++++++++
    User Notes manage creation of QDialog for user notes
"""

from logging import getLogger

from PyQt5.Qt import Qt, QIcon, QLabel, QTextEdit, QWidget, QDialog, QPushButton, QVBoxLayout

from alignak_app.utils.config import settings

from alignak_app.qobjects.common.widgets import center_widget, get_logo_widget

logger = getLogger(__name__)


class UserNotesQDialog(QDialog):
    """
        Class who create UserNotes QDialog
    """

    def __init__(self, parent=None):
        super(UserNotesQDialog, self).__init__(parent)
        self.setWindowTitle('User Notes')
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet(settings.css_style)
        self.setWindowIcon(QIcon(settings.get_image('icon')))
        self.setObjectName('dialog')
        self.setFixedSize(300, 300)
        # Fields
        self.notes_edit = QTextEdit()
        self.old_notes = ''

    def initialize(self, notes):
        """
        Initialize QDialog for UserNotesQDialog

        """

        self.old_notes = notes
        center_widget(self)

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

        main_layout.addWidget(get_logo_widget(self, _('Edit User Notes')))

        notes_title = QLabel(_("Please modify your notes:"))
        notes_title.setObjectName('subtitle')
        main_layout.addWidget(notes_title)
        main_layout.setAlignment(notes_title, Qt.AlignCenter)

        main_layout.addWidget(self.get_user_notes_widget())

    def get_user_notes_widget(self):
        """
        Return notes QWidget

        :param notes: notes of the user
        :type notes: str
        :return: notes QWidget
        :rtype: QWidget
        """

        notes_widget = QWidget()
        notes_widget.setObjectName('dialog')
        notes_layout = QVBoxLayout()
        notes_widget.setLayout(notes_layout)

        self.notes_edit.setPlaceholderText(_('type your notes'))
        self.notes_edit.setText(self.old_notes)
        notes_layout.addWidget(self.notes_edit)

        # Accept button
        accept_btn = QPushButton(_('Confirm'), self)
        accept_btn.clicked.connect(self.accept_notes)
        accept_btn.setObjectName('valid')
        accept_btn.setMinimumHeight(30)
        notes_layout.addWidget(accept_btn)

        return notes_widget

    def accept_notes(self):  # pragma: no cover
        """
        Set QDialog notes to Rejected or Accepted (prevent to patch for nothing)

        """

        if self.old_notes == self.notes_edit.toPlainText():
            self.reject()
        elif not self.old_notes or self.old_notes.isspace():
            if not self.notes_edit.toPlainText() or self.notes_edit.toPlainText().isspace():
                self.reject()
            else:
                self.accept()
        else:
            self.accept()
