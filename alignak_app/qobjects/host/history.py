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

from PyQt5.Qt import QWidget, QVBoxLayout, QLabel, QPixmap, Qt, QGridLayout
from PyQt5.Qt import QTableWidget, QTableWidgetItem, QColor, QAbstractItemView

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
        self.table_headers = [_('Event Type'), _('Message')]
        self.history_title = QLabel()

    def initialize(self):
        """
        Initialize History QWidget

        """

        self.app_widget.initialize(_('History'))
        self.setMinimumSize(700, 500)
        self.app_widget.add_widget(self)

        layout = QGridLayout()
        self.setLayout(layout)

        # History Description
        self.history_title.setObjectName("title")
        layout.addWidget(self.history_title, 0, 0, 1, 1)
        layout.setAlignment(self.history_title, Qt.AlignCenter)

        # History Table
        layout.addWidget(self.history_table, 1, 0, 1, 1)
        self.history_table.verticalHeader().hide()
        self.history_table.verticalHeader().setDefaultSectionSize(40)
        self.history_table.setColumnCount(len(self.table_headers))

        self.history_table.setColumnWidth(1, 500)
        self.history_table.setSortingEnabled(True)
        self.history_table.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.history_table.setHorizontalHeaderLabels(self.table_headers)
        self.history_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.history_table.horizontalHeader().setStretchLastSection(True)
        self.history_table.horizontalHeader().setHighlightSections(False)

        center_widget(self.app_widget)

    @staticmethod
    def get_icon_widget(event):
        """
        Return QWidget with corresponding icon to item state

        :param event: data of an event
        :type event: dict
        :return: icon QWidget
        :rtype: QWidget
        """

        widget_icon = QWidget()
        layout_icon = QVBoxLayout()
        widget_icon.setLayout(layout_icon)

        icon_label = QLabel()
        icon = QPixmap(
            settings.get_image(
                History.get_history_icon_name_from_message(event['message'], event['type'])
            )
        )
        icon_label.setPixmap(icon)
        icon_label.setFixedSize(18, 18)
        icon_label.setScaledContents(True)

        layout_icon.addWidget(icon_label)
        layout_icon.setAlignment(icon_label, Qt.AlignCenter)

        return widget_icon

    def update_history_data(self, hostname, host_history):
        """
        Update data of history QTableWidget

        :param hostname: name of the host
        :type hostname: str
        :param host_history: history of host
        :type host_history: History
        """

        logger.debug('Open History for %s', hostname)

        self.history_table.setRowCount(len(host_history.data) * 2)
        self.history_title.setText(_("The last 25 events for %s") % hostname.capitalize())

        row = 0
        for event in host_history.data:
            # Set Span
            self.history_table.setSpan(row, 0, 2, 1)

            # Icon event
            icon_item = self.get_icon_widget(event)
            self.history_table.setCellWidget(row, 0, icon_item)

            # Event Type (with date)
            local_timestamp = get_local_datetime_from_date(event['_updated'])
            created_since = get_time_diff_since_last_timestamp(local_timestamp.timestamp())

            event_type = self.get_event_type(event, hostname)
            event_type_dated = '%s      (Updated at: %s)' % (event_type, created_since)
            type_item = QTableWidgetItem(event_type_dated)
            type_item.setForeground(
                QColor(History.get_event_color(event['message'], event['type']))
            )
            self.history_table.setItem(row, 1, type_item)

            # Message event
            message_item = QTableWidgetItem(event['message'])
            self.history_table.setItem(row + 1, 1, message_item)

            row += 2

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
        else:
            event_type = _('Host: %s') % hostname.capitalize()
        if not event_type:
            event_type = event['type']

        return event_type
