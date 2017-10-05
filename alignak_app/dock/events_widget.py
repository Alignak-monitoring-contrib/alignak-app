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

from alignak_app.core.utils import get_image_path, get_css
from alignak_app.core.data_manager import data_manager

from PyQt5.Qt import QWidget, QAbstractItemView, QListWidget  # pylint: disable=no-name-in-module
from PyQt5.Qt import QListWidgetItem, QSize, QIcon, QTimer  # pylint: disable=no-name-in-module
from PyQt5.Qt import QLabel, QVBoxLayout, Qt  # pylint: disable=no-name-in-module


class EventItem(QListWidgetItem):
    """
        Class who create an event QListWidgetItem
    """

    def initialize(self, event_type, msg):
        """
        Initialize QListWidgetItem

        """

        self.setText("%s" % msg)
        self.setIcon(QIcon(get_image_path(self.get_icon(event_type))))

        self.setSizeHint(QSize(self.sizeHint().width(), 35))

    @staticmethod
    def get_icon(event_type):
        """
        Define and return icon type

        :param event_type: the type of event
        :type event_type: str
        :return: event icon name
        :rtype: str
        """

        icon_types = {
            'valid': ['OK', 'UP'],
            'info': ['UNKNOWN', 'INFO'],
            'warn': ['WARNING', 'UNREACHABLE', 'WARN'],
            'error': ['DOWN', 'CRITICAL', 'ALERT']
        }

        for key, _ in icon_types.items():
            if event_type in icon_types[key]:
                return key

        return ''


class EventsQListWidget(QWidget):
    """
        Class who create QWidget for events
    """

    def __init__(self):
        super(EventsQListWidget, self).__init__()
        self.setStyleSheet(get_css())
        # Fields
        self.events_list = QListWidget()
        self.timer = QTimer()

    def initialize(self):
        """
        Intialize QWidget

        """

        self.timer.setInterval(15000)
        self.timer.start()
        self.timer.timeout.connect(self.send_datamanager_events)

        layout = QVBoxLayout()
        self.setLayout(layout)

        event_title = QLabel("Last events...")
        layout.addWidget(event_title)
        layout.setAlignment(event_title, Qt.AlignCenter)

        self.events_list.setDragDropMode(QAbstractItemView.InternalMove)
        self.events_list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.events_list.doubleClicked.connect(self.remove_event)
        self.events_list.setAcceptDrops(True)
        self.events_list.setSortingEnabled(True)
        self.events_list.setWordWrap(True)

        layout.addWidget(self.events_list)

    def send_datamanager_events(self):
        """
        Add events stored in DataManager

        """

        events = data_manager.get_events()

        if events:
            for event in events:
                self.add_event(event['event_type'], event['message'])

    def add_event(self, event_type, msg):
        """
        Add event to events list

        :param event_type: type of event
        :param msg:
        :return:
        """

        event = EventItem()
        event.initialize(event_type, msg)

        self.events_list.addItem(event)

    def remove_event(self):
        """
        Remove item when user double click on an item

        """

        self.events_list.takeItem(self.events_list.currentRow())


events_widget = EventsQListWidget()
events_widget.initialize()
