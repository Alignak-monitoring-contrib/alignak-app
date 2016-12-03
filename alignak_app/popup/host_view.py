#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015-2016:
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
    App Synthesis manage widget for Synthesis QWidget.
"""

import sys

from logging import getLogger

from alignak_app.core.utils import get_image_path, set_app_config

try:
    __import__('PyQt5')
    from PyQt5.QtWidgets import QApplication  # pylint: disable=no-name-in-module
    from PyQt5.QtWidgets import QWidget, QVBoxLayout  # pylint: disable=no-name-in-module
    from PyQt5.QtWidgets import QGridLayout, QLabel  # pylint: disable=no-name-in-module
    from PyQt5.Qt import QPixmap  # pylint: disable=no-name-in-module
except ImportError:  # pragma: no cover
    from PyQt4.Qt import QApplication  # pylint: disable=import-error
    from PyQt4.Qt import QWidget, QVBoxLayout  # pylint: disable=import-error
    from PyQt4.Qt import QGridLayout, QLabel  # pylint: disable=import-error
    from PyQt4.Qt import QPixmap  # pylint: disable=import-error


logger = getLogger(__name__)


class HostView(QWidget):
    """
        Class who create the Synthesis QWidget.
    """

    def __init__(self, parent=None):
        super(HostView, self).__init__(parent)
        self.setMaximumHeight(100)
        self.layout = None
        self.labels = {}

    def init_view(self):
        """
        TODO
        """

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        # Creates the labels that will be updated
        self.labels = {
            'name': QLabel(),
            'state_icon': QLabel(),
            'real_state_icon': QLabel(),
            'last_check': QLabel(),
            'output': QLabel()
        }

        # Adjust icons
        self.labels['state_icon'].setFixedSize(64, 64)
        self.labels['real_state_icon'].setFixedSize(32, 32)
        self.labels['real_state_icon'].setScaledContents(True)

        # row, column, rowSpan, colSPan
        self.layout.addWidget(self.labels['state_icon'], 0, 0, 2, 1)
        self.layout.addWidget(self.labels['name'], 2, 0, 1, 1)

        real_state_text = QLabel('Host real state, excluding services')
        real_state_text.setWordWrap(True)
        self.layout.addWidget(real_state_text, 0, 1, 1, 1)
        self.layout.addWidget(self.labels['real_state_icon'], 1, 1, 2, 1)

        self.layout.addWidget(QLabel('My last Check'), 0, 2, 1, 2)
        self.layout.addWidget(QLabel('Last check:'), 1, 2, 1, 1)
        self.layout.addWidget(self.labels['last_check'], 1, 3, 1, 1)
        self.layout.addWidget(QLabel('Output:'), 2, 2, 1, 1)
        self.layout.addWidget(self.labels['output'], 2, 3, 1, 1)

        # self.update_view(host)/

    def update_view(self, host):
        """
        TODO
        :return:
        """

        self.labels['name'].setText(host['name'].title())
        self.labels['state_icon'].setPixmap(self.create_icon(host['ls_state']))
        self.labels['real_state_icon'].setPixmap(self.create_icon(''))
        self.labels['last_check'].setText(str(host['ls_last_check']))
        self.labels['output'].setText(host['ls_output'])

    @staticmethod
    def create_icon(state):
        """

        :param state:
        :return:
        """

        if 'UP' in state:
            icon_name = 'hosts_up'
        elif 'UNREACHABLE' in state:
            icon_name = 'hosts_unreach'
        elif 'DOWN' in state:
            icon_name = 'hosts_down'
        else:
            icon_name = 'hosts_none'

        icon = QPixmap(get_image_path(icon_name))

        return icon


# For Tests
if __name__ == '__main__':
    app = QApplication(sys.argv)

    set_app_config()

    synthesis = HostView()
    synthesis.init_view()

    sys.exit(app.exec_())