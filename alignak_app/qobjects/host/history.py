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

from PyQt5.Qt import QWidget, QLabel, QPixmap, QTableWidget, QAbstractItemView, QGridLayout
from PyQt5.Qt import QVBoxLayout

from alignak_app.items.history import History
from alignak_app.utils.config import settings
from alignak_app.utils.time import get_local_datetime_from_date, get_time_diff_since_last_timestamp

from alignak_app.qobjects.common.frames import AppQFrame
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
        self.history_table = QTableWidget()
        self.table_headers = ['Events']
        self.history_title = QLabel()

    def initialize(self):
        """
        Initialize History QWidget

        """

        self.app_widget.initialize(_('History'))
        self.setMinimumSize(800, 670)
        self.app_widget.add_widget(self)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # History Table
        layout.addWidget(self.history_table)
        self.history_table.setObjectName('history')
        self.history_table.verticalHeader().hide()
        self.history_table.verticalHeader().setDefaultSectionSize(100)
        self.history_table.setColumnCount(len(self.table_headers))
        self.history_table.setColumnWidth(0, 600)
        self.history_table.setSortingEnabled(True)
        self.history_table.setHorizontalScrollMode(QAbstractItemView.ScrollPerItem)
        self.history_table.setHorizontalHeaderLabels(self.table_headers)
        self.history_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.history_table.horizontalHeader().setStretchLastSection(True)
        self.history_table.horizontalHeader().setMinimumHeight(30)

        center_widget(self.app_widget)

    def update_history_data(self, hostname, host_history):
        """
        Update data of history QTableWidget

        :param hostname: name of the host
        :type hostname: str
        :param host_history: history of host
        :type host_history: History
        """

        logger.debug('Open History for %s', hostname)

        self.history_table.setRowCount(len(host_history.data))
        self.history_table.setHorizontalHeaderLabels(
            [_("The last 25 events for %s") % hostname.capitalize()]
        )

        row = 0
        for event in host_history.data:
            event_widget = self.get_event_widget(hostname, event)
            self.history_table.setCellWidget(row, 0, event_widget)
            row += 1

    def get_event_widget(self, hostname, event):
        """
        Return event QWidget with icon, event text and event message

        :param hostname: name of host attached to event
        :type hostname: str
        :param event: data of an event
        :type event: dict
        :return: widget of event
        :rtype: QWidget
        """

        event_widget = QWidget()
        event_widget.setObjectName('history')
        event_widget.setToolTip(event['type'])
        event_layout = QGridLayout(event_widget)

        # Event icon
        icon_pixmap = self.get_icon_label(event)
        event_layout.addWidget(icon_pixmap, 0, 0, 2, 1)

        # Event type (with date)
        event_title = QLabel()
        event_title.setObjectName(
            History.get_history_icon_name(event['message'], event['type'])
        )
        local_timestamp = get_local_datetime_from_date(event['_updated'])
        created_since = get_time_diff_since_last_timestamp(local_timestamp.timestamp())

        event_type = self.get_event_type(event, hostname)
        event_type_dated = '%s      (%s)' % (event_type, created_since)
        event_title.setText(event_type_dated)
        event_layout.addWidget(event_title, 0, 1, 1, 1)

        # Event message
        event_msg = QLabel()
        event_msg.setText(event['message'])
        event_layout.addWidget(event_msg, 1, 1, 1, 1)

        return event_widget

    @staticmethod
    def get_icon_label(event):
        """
        Return QWidget with corresponding icon to item state

        :param event: data of an event
        :type event: dict
        :return: icon QWidget
        :rtype: QWidget
        """

        icon_label = QLabel()
        icon = QPixmap(
            settings.get_image(
                History.get_history_icon_name(event['message'], event['type'])
            )
        )
        icon_label.setPixmap(icon)
        icon_label.setFixedSize(32, 32)
        icon_label.setScaledContents(True)

        return icon_label

    @staticmethod
    def get_event_type(event, hostname):
        """
        Return event type for history

        :param event: event of history
        :type event: dict
        :param hostname: name of host attached to event
        :type hostname: str
        :return: the event type
        :rtype: str
        """

        event_type = ''

        if 'service_name' in event:
            if event['service_name']:
                event_type = _('Service: %s') % event['service_name'].capitalize()
        if not event_type:
            event_type = _('Host: %s') % hostname.capitalize()

        return event_type
