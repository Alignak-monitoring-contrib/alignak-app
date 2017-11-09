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

"""
    User Notes manage notes form
"""

from logging import getLogger

from PyQt5.Qt import Qt, QIcon, QLabel, QTextEdit, QWidget, QDialog, QPushButton, QVBoxLayout

from alignak_app.core.utils.config import app_css, get_image
from alignak_app.pyqt.common.widgets import center_widget, get_logo_widget

logger = getLogger(__name__)


class UserNotesQDialog(QDialog):
    """
        Class who create UserNotes QDialog
    """

    def __init__(self, parent=None):
        super(UserNotesQDialog, self).__init__(parent)
        self.setWindowTitle('User Notes')
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet(app_css)
        self.setWindowIcon(QIcon(get_image('icon')))
        self.setObjectName('dialog')
        self.setFixedSize(300, 300)
        # Fields
        self.notes_edit = QTextEdit()

    def initialize(self, notes):
        """
        Initialize QDialog for UserNotesQDialog

        """

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

        main_layout.addWidget(self.get_user_notes_widget(notes))

    def get_user_notes_widget(self, notes):
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
        self.notes_edit.setText(notes)
        notes_layout.addWidget(self.notes_edit)

        # Accept button
        accept_btn = QPushButton(_('Confirm'), self)
        accept_btn.clicked.connect(self.accept)
        accept_btn.setObjectName('valid')
        accept_btn.setMinimumHeight(30)
        notes_layout.addWidget(accept_btn)

        return notes_widget
