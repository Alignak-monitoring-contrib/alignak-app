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
    Buttons
    +++++++
    Buttons manage global QPushButtons
"""

from PyQt5.Qt import QWidget, QPushButton, QHBoxLayout

from alignak_app.utils.config import settings


class ToggleQWidgetButton(QWidget):
    """
        Class who create QWidget with "toggle" QPushButton inside.
    """

    def __init__(self, parent=None):
        super(ToggleQWidgetButton, self).__init__(parent)
        self.toggle_btn = QPushButton()

    def initialize(self):
        """
        Initialize QWidget

        """

        layout = QHBoxLayout()
        self.setLayout(layout)

        self.toggle_btn.setText('ON')
        self.toggle_btn.setFixedSize(80, 20)
        self.toggle_btn.setCheckable(True)
        self.toggle_btn.setChecked(True)
        self.toggle_btn.setObjectName("True")
        self.toggle_btn.clicked.connect(self.update_btn_state)
        layout.addWidget(self.toggle_btn)

    def update_btn_state(self, state):
        """
        Update QPushButton state, ObjectName and StyleSheet

        :param state: current state of QPushButton
        :type state: bool
        """

        states = {
            True: "ON",
            False: "OFF"
        }

        self.toggle_btn.setChecked(state)
        self.toggle_btn.setText(states[state])
        self.toggle_btn.setObjectName(str(state))
        self.toggle_btn.setStyleSheet(settings.css_style)

    def get_btn_state(self):
        """
        Return "toggle_btn" state

        :return: QPushButton state
        :rtype: bool
        """

        return self.toggle_btn.isChecked()
