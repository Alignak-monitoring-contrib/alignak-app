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
    History
    +++++++
    History manage creation of QWidget to display history of a host
"""


from logging import getLogger

from PyQt5.Qt import QWidget, QScrollArea, QLabel, QPixmap, Qt, QGridLayout

from alignak_app.items.history import History
from alignak_app.utils.config import settings

from alignak_app.qobjects.common.frames import AppQFrame, get_frame_separator
from alignak_app.qobjects.common.widgets import center_widget

logger = getLogger(__name__)


class HistoryQWidget(QWidget):
    """
        Class who create the History QWidget for host
    """

    def __init__(self, parent=None):
        super(HistoryQWidget, self).__init__(parent)
        self.setObjectName("history")
        # Fields
        self.app_widget = AppQFrame()

    def initialize(self, hostname, host_history):
        """
        Initialize History QWidget

        :param hostname: name of the host
        :type hostname: str
        :param host_history: history of host
        :type host_history: History
        """

        logger.debug('Open History for %s', hostname)

        # Create ScrollArea
        scroll = QScrollArea()
        scroll.setWidget(self)
        scroll.setWidgetResizable(True)
        scroll.setMinimumWidth(800)

        self.app_widget.initialize(_('History of %s') % hostname.capitalize())
        self.app_widget.layout().setSpacing(0)
        self.app_widget.add_widget(scroll)

        layout = QGridLayout()
        self.setLayout(layout)

        # History Description
        event_desc = QLabel(_("The last 25 events for %s") % hostname.capitalize())
        event_desc.setObjectName("title")
        layout.addWidget(event_desc, 0, 0, 1, 1)
        layout.setAlignment(event_desc, Qt.AlignCenter)

        # History QWidgets
        line = 1

        for history_event in host_history.data:
            history_widget = self.get_history_widget_model(history_event, hostname)

            layout.addWidget(history_widget, line, 0, 2, 2)
            layout.addWidget(get_frame_separator(), line + 1, 0, 1, 2)

            line += 3

        layout.setAlignment(Qt.AlignTop)
        center_widget(self.app_widget)

    @staticmethod
    def get_history_widget_model(history_event, hostname):
        """
        Create and return event QWidgets

        :param history_event: event of history given by backend
        :type history_event: dict
        :param hostname: name of host
        :type hostname: str
        :return: history Qwidget model with data
        :rtype: QWidget
        """

        history_widget_model = QWidget()
        history_widget_model.setToolTip(history_event['type'])
        history_widget_model.setObjectName("history_event")

        event_layout = QGridLayout()
        history_widget_model.setLayout(event_layout)

        event_name = ''
        if 'service_name' in history_event:
            if history_event['service_name']:
                event_name = _('Service: %s') % history_event['service_name'].capitalize()
        if not event_name:
            event_name = _('Host: %s') % hostname.capitalize()

        icon_name = History.get_history_icon_name_from_message(
            history_event['message'], history_event['type']
        )
        event_label = QLabel(event_name)
        event_label.setObjectName(icon_name)
        event_layout.addWidget(event_label, 0, 0, 1, 1)

        message_label = QLabel('%s' % history_event['message'])
        message_label.setWordWrap(True)
        event_layout.addWidget(message_label, 1, 0, 1, 1)

        icon = QPixmap(settings.get_image(icon_name))
        icon_label = QLabel()
        icon_label.setToolTip(history_event['type'])
        icon_label.setFixedSize(32, 32)
        icon_label.setPixmap(icon)
        icon_label.setScaledContents(True)

        event_layout.addWidget(icon_label, 0, 1, 2, 1)
        event_layout.setAlignment(icon_label, Qt.AlignVCenter)

        return history_widget_model
