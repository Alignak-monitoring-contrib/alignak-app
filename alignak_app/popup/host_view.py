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
from alignak_app.core.utils import get_diff_since_last_check

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
        Class who create the Host View QWidget.
    """

    def __init__(self, parent=None):
        super(HostView, self).__init__(parent)
        self.setFixedHeight(150)
        self.layout = None
        self.labels = {}

    def init_view(self):
        """
        Init Host View with default values.

        """

        logger.info('Initialize Host View...')

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        # Creates the labels that will be updated
        self.labels = {
            'name': QLabel('<h3>Host Name</h3>'),
            'state_icon': QLabel(),
            'real_state_icon': QLabel(),
            'last_check': QLabel('N/A'),
            'output': QLabel('N/A')
        }

        # Adjust icons and set default icons
        self.labels['state_icon'].setFixedSize(64, 64)
        self.labels['state_icon'].setPixmap(self.get_host_icon(''))
        self.labels['real_state_icon'].setFixedSize(32, 32)
        self.labels['real_state_icon'].setScaledContents(True)
        self.labels['real_state_icon'].setPixmap(self.get_host_icon(''))

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

    def update_view(self, host):
        """
        Update Host view with desired host.

        :param host: host data from backend
        :type host: dict
        """

        logger.info('Update Host View...')
        logger.debug('Host: ' + host['name'] + ' is ' + host['ls_state'])

        if isinstance(host['ls_last_check'], int):
            time_delta = get_diff_since_last_check(host['ls_last_check'])
        else:
            time_delta = 'NOT FOUND'

        self.labels['name'].setText('<h3>' + host['name'].title() + '</h3>')
        self.labels['state_icon'].setPixmap(self.get_host_icon(host['ls_state']))
        self.labels['real_state_icon'].setPixmap(self.get_host_icon(''))
        self.labels['last_check'].setText(str(time_delta))
        self.labels['output'].setText(host['ls_output'])

    @staticmethod
    def get_host_icon(state):
        """
        Return QPixmap with the icon corresponding to the status.

        :param state: state of the host.
        :type state: str
        :return: QPixmap with image
        :rtype: QPixmap
        """

        if 'UP' in state:
            icon_name = 'hosts_up'
        elif 'UNREACHABLE' in state:
            icon_name = 'hosts_unreach'
        elif 'DOWN' in state:
            icon_name = 'hosts_down'
        else:
            icon_name = 'hosts_none'

        logger.debug('Host icon: ' + icon_name)
        icon = QPixmap(get_image_path(icon_name))

        return icon

# For Tests
if __name__ == '__main__':
    app = QApplication(sys.argv)

    set_app_config()

    synthesis = HostView()
    synthesis.init_view()

    sys.exit(app.exec_())
