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
from PyQt5.QtWidgets import QGridLayout  # pylint: disable=no-name-in-module
from PyQt5.Qt import QPixmap  # pylint: disable=no-name-in-module


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
        Initialize QWidget

        :param hostname: name of the host
        :type hostname: str
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
        Create and return event QWidgets

        :param event: event of history given by backend
        :type event: dict
        :return: event Qwidget
        :rtype: QWidget
        """

        event_widget = QWidget()
        event_widget.setToolTip(event['type'])

        event_layout = QGridLayout()
        event_widget.setLayout(event_layout)

        event_label = QLabel('%s' % event['service_name'])
        event_label.setObjectName('eventname')
        event_layout.addWidget(event_label, 0, 0, 1, 1)

        message_label = QLabel('%s' % event['message'])
        message_label.setWordWrap(True)
        event_layout.addWidget(message_label, 1, 0, 1, 1)

        icon = self.get_event_icon(event['message'], event['type'])
        icon_label = QLabel()
        icon_label.setObjectName('message')
        icon_label.setToolTip(event['type'])
        icon_label.setFixedSize(32, 32)
        icon_label.setPixmap(icon)
        icon_label.setScaledContents(True)

        event_layout.addWidget(icon_label, 0, 1, 1, 1)

        return event_widget

    @staticmethod
    def get_event_icon(message, event_type):
        """
        Return icon QPixmap depending of message or event type

        :param message: message of the history event
        :type message: str
        :param event_type: type of event: ack.processed, check.result,...
        :type event_type: str
        :return: QPixmap with the appropriate icon
        :rtype: QPixmap
        """

        if 'ack' in event_type:
            icon_name = 'services_acknowledge'
        elif 'downtime' in event_type:
            icon_name = 'services_downtime'
        else:
            if 'OK' in message or 'UP' in message:
                icon_name = 'valid'
            elif 'UNKNOWN' in message:
                icon_name = 'services_unknown'
            elif 'UNREACHABLE' in message:
                icon_name = 'services_unknown'
            else:
                icon_name = 'error'

        icon = QPixmap(get_image_path(icon_name))

        return icon
