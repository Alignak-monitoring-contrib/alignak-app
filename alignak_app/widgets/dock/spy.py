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
    Spy QWidgets manage host items who are spied
"""

from PyQt5.Qt import QLabel, QVBoxLayout, Qt  # pylint: disable=no-name-in-module
from PyQt5.Qt import QWidget, QAbstractItemView, QListWidget  # pylint: disable=no-name-in-module

from alignak_app.widgets.dock.events import EventItem


class SpyQListWidget(QWidget):
    """
        Class who create QWidget for spied hosts
    """

    def __init__(self):
        super(SpyQListWidget, self).__init__()
        self.spied_list = QListWidget()

    def initialize(self):
        """
        Intialize QWidget

        """

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.spied_list.setDragDropMode(QAbstractItemView.DragDrop)
        self.spied_list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.spied_list.doubleClicked.connect(self.remove_event)
        self.spied_list.setAcceptDrops(True)
        self.spied_list.setWordWrap(True)

        drop_hint_item = EventItem()
        drop_hint_item.setText("Drop Events here...")
        drop_hint_item.setFlags(Qt.ItemIsDropEnabled)
        self.spied_list.insertItem(0, drop_hint_item)

        layout.addWidget(self.spied_list)

    def add_event(self, event_type, msg):
        """
        Add event to events list

        :param event_type: type of event
        :param msg:
        :return:
        """

        event = EventItem()
        event.initialize(event_type, msg)

        self.spied_list.addItem(event)

    def remove_event(self):
        """
        Remove item when user double click on an item

        """

        self.spied_list.takeItem(self.spied_list.currentRow())
