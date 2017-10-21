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
    Events QWidgets manage creation of events
"""

from alignak_app.core.config import app_css
from alignak_app.core.data_manager import data_manager

from PyQt5.Qt import QWidget, QAbstractItemView, QListWidget  # pylint: disable=no-name-in-module
from PyQt5.Qt import QListWidgetItem, QSize, QTimer  # pylint: disable=no-name-in-module
from PyQt5.Qt import QVBoxLayout, QColor  # pylint: disable=no-name-in-module


class EventItem(QListWidgetItem):
    """
        Class who create an event QListWidgetItem
    """

    def __init__(self):
        super(EventItem, self).__init__()
        self.timer = None

    def initialize(self, event_type, msg, timer=False):
        """
        Initialize QListWidgetItem

        """

        if timer:
            self.timer = QTimer()

        self.setText("%s" % msg)
        self.setToolTip(msg)
        self.setBackground(QColor(self.get_color_event(event_type)))
        self.setForeground(QColor("#000"))

        self.setSizeHint(QSize(self.sizeHint().width(), 50))

    def close_item(self):
        """

        :return:
        """

        self.setHidden(True)

    @staticmethod
    def get_color_event(event_type):
        """
        Return corresponding color of event type

        :param event_type: the type of event
        :type event_type: str
        :return: the associated color with the event
        :rtype: str
        """

        available_colors = {
            '#27ae60': ['OK', 'UP'],
            '#2980b9': ['UNKNOWN', 'INFO'],
            '#e67e22': ['WARNING', 'UNREACHABLE', 'WARN'],
            '#e74c3c': ['DOWN', 'CRITICAL', 'ALERT'],
            '#f39c12': ['ACK'],
            '#f1c40f': ['DOWN']
        }

        for key, _ in available_colors.items():
            if event_type in available_colors[key]:
                return key

        return ''


class EventsQListWidget(QWidget):
    """
        Class who create QWidget for events
    """

    def __init__(self):
        super(EventsQListWidget, self).__init__()
        self.setStyleSheet(app_css)
        self.setObjectName('events')
        # Fields
        self.events_list = QListWidget()
        self.timer = QTimer()

    def initialize(self):
        """
        Intialize QWidget

        """

        self.timer.setInterval(30000)
        self.timer.start()
        self.timer.timeout.connect(self.send_datamanager_events)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.events_list.setDragDropMode(QAbstractItemView.InternalMove)
        self.events_list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.events_list.doubleClicked.connect(self.remove_event)
        self.events_list.setAcceptDrops(True)
        self.events_list.setWordWrap(True)

        self.add_event(
            'OK',
            _('Welcome %s, you are connected to Alignak Backend') %
            data_manager.database['user'].name,
            timer=True
        )

        layout.addWidget(self.events_list)

    def send_datamanager_events(self):
        """
        Add events stored in DataManager

        """

        events = data_manager.get_events()

        if events:
            for event in events:
                self.add_event(event['event_type'], event['message'])

    def add_event(self, event_type, msg, timer=False):
        """
        Add event to events list

        :param event_type: type of event
        :type event_type: str
        :param msg: event content to display
        :type msg: str
        :param timer: set if event is temporary or not
        :type timer: bool
        """

        event = EventItem()
        event.initialize(event_type, msg, timer=timer)

        self.events_list.addItem(event)
        if timer:
            QTimer.singleShot(
                10000,
                lambda: self.remove_timer_event(event)
            )

    def remove_timer_event(self, event):
        """
        Remove EventItem with timer

        :param event: EventItem with timer
        :type event: EventItem
        """

        self.events_list.takeItem(self.events_list.row(event))

    def remove_event(self):
        """
        Remove item when user double click on an item

        """

        self.events_list.takeItem(self.events_list.currentRow())


events_widget = EventsQListWidget()
events_widget.initialize()


def send_event(event_type, msg, timer=False):
    """
    Access function to simplify code in rest of application

    :param event_type: type of event. Follow the following:
    - 'valid': ['OK', 'UP']
    - 'info': ['UNKNOWN', 'INFO']
    - 'warn': ['WARNING', 'UNREACHABLE', 'WARN']
    - 'problem': ['DOWN', 'CRITICAL', 'ALERT']
    - 'aknowledge': ['ACK']
    - 'downtime': ['DOWNTIME']
    :type event_type: str
    :param msg: event content to display
    :type msg: str
    :param timer: define if event is temporary or not
    :type timer: bool
    """

    events_widget.add_event(event_type, msg, timer)
