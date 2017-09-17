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
    History display thehistory of a host
"""


from logging import getLogger

from alignak_app.core.utils import get_css, get_image_path
from alignak_app.widgets.app_widget import AppQWidget

from PyQt5.QtWidgets import QWidget, QScrollArea, QLabel  # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QGridLayout, QVBoxLayout  # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QStackedWidget  # pylint: disable=no-name-in-module
from PyQt5.Qt import QIcon, QPixmap, QListWidget, QDialog  # pylint: disable=no-name-in-module
from PyQt5.Qt import QTimer, Qt, QCheckBox, QTextEdit  # pylint: disable=no-name-in-module
from PyQt5.QtGui import QFont  # pylint: disable=no-name-in-module


logger = getLogger(__name__)


class History(QWidget):
    """
        Class who create the History QWidget for host
    """

    def __init__(self, history, parent=None):
        super(History, self).__init__(parent)
        self.setStyleSheet(get_css())
        # Fields
        self.history = history
        self.app_widget = AppQWidget()

    def initialize(self, hostname):
        """
        TODO
        :param hostname:
        :return:
        """

        self.app_widget.initialize('History of %s' % hostname)

        scroll = QScrollArea()
        scroll.setWidget(self)
        scroll.setWidgetResizable(True)
        scroll.setMinimumSize(1000, 800)
        self.app_widget.add_widget(scroll)

        layout = QGridLayout()
        self.setLayout(layout)

        line = 0

        for event in self.history:
            event_widget = self.get_event_widget(event)

            layout.addWidget(event_widget, line, 0, 2, 2)

            line += 2

    def get_event_widget(self, event):
        """
        TODO
        :param event:
        :return:
        """

        event_widget = QWidget()

        event_layout = QGridLayout()
        event_widget.setLayout(event_layout)

        event_label = QLabel('%s: %s' % (event['service_name'], event['message']))
        event_label.setMinimumHeight(32)

        icon = self.get_event_icon(event['message'])
        icon_label = QLabel()
        icon_label.setFixedSize(32, 32)
        icon_label.setPixmap(icon)
        icon_label.setScaledContents(True)

        event_layout.addWidget(event_label, 0, 0, 1, 2)
        event_layout.addWidget(icon_label, 0, 2, 1, 1)

        return event_widget

    @staticmethod
    def get_event_icon(message):
        """
        TODO
        :param message:
        :return:
        """

        if 'OK' in message or 'UP' in message:
            icon_name = 'valid'
        elif 'UNKNOWN' in message:
            icon_name = 'services_unknown'
        elif 'UNREACHABLE' in message:
            icon_name = 'services_unknown'
        elif 'DOWNTIME' in message or 'downtime' in message:
            icon_name = 'downtime'
        elif 'ACKNOWLEDGE' in message or 'acknowledge' in message:
            icon_name = 'acknowledged'
        else:
            icon_name = 'error'

        icon = QPixmap(get_image_path(icon_name))

        return icon
