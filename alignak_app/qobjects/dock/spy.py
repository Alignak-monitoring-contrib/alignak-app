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
    Spy
    +++
    Spy manage creation of QWidget for host items who are spied
"""

from logging import getLogger

from PyQt5.Qt import QVBoxLayout, Qt, QWidget, QAbstractItemView, QListWidget, pyqtSignal

from alignak_app.backend.datamanager import data_manager

from alignak_app.qobjects.dock.events import EventItem

logger = getLogger(__name__)


class SpyQListWidget(QListWidget):
    """
        Class who create QListWidget for spied hosts
    """

    item_dropped = pyqtSignal(EventItem, name="remove_item")
    host_spied = pyqtSignal(str, name="host_spied")

    def __init__(self):
        super(SpyQListWidget, self).__init__()
        self.spied_hosts = []
        self.host_spied.connect(self.add_spy_host)

    def add_spy_host(self, host_id):
        """
        Add a host to spied list and create corresponding EventItem()

        :param host_id: "_id" of host to spy
        :type host_id: str
        """

        if host_id not in self.spied_hosts:
            self.spied_hosts.append(host_id)
            host = data_manager.get_item('host', '_id', host_id)
            item = EventItem()
            item.initialize(
                'INFO',
                _('Host %s is spied by Alignak-app !') % host.name.capitalize()
            )
            item.host = host.item_id
            self.addItem(item)

            logger.info('Spy a new host: %s', host.name)
            logger.debug('... with id: %s', host_id)

    def dragMoveEvent(self, event):
        """
        Override dragMoveEvent.
         Only accept EventItem() objects who are "spied_on" and not already spied

        :param event: event triggered when something move
        """

        if isinstance(event.source().currentItem(), EventItem):
            if event.source().currentItem().spied_on and \
                    (event.source().currentItem().host not in self.spied_hosts):
                event.accept()
            else:
                event.ignore()
        else:
            event.ignore()

    def dropEvent(self, event):
        """
        Override dropEvent.
         Get dropped item data, create a new one, and delete the one who is in EventsQWidget

        :param event: event triggered when something is dropped
        """

        self.add_spy_host(event.source().currentItem().host)

        # Remove the item dropped and original, to let only new one created
        row = self.row(event.source().currentItem())
        self.takeItem(row)
        self.item_dropped.emit(event.source().currentItem())


class SpyQWidget(QWidget):
    """
        Class who create QWidget for spied hosts
    """

    def __init__(self):
        super(SpyQWidget, self).__init__()
        self.spy_list_widget = SpyQListWidget()

    def initialize(self):
        """
        Intialize QWidget

        """

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.spy_list_widget.setDragDropMode(QAbstractItemView.DragDrop)
        self.spy_list_widget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.spy_list_widget.doubleClicked.connect(self.remove_event)
        self.spy_list_widget.setAcceptDrops(True)
        self.spy_list_widget.setWordWrap(True)

        drop_hint_item = EventItem()
        drop_hint_item.setText(_('Drop Events here to spy host...'))
        drop_hint_item.setFlags(Qt.ItemIsDropEnabled)
        self.spy_list_widget.insertItem(0, drop_hint_item)

        layout.addWidget(self.spy_list_widget)

    def remove_event(self):
        """
        Remove item when user double click on an item

        """

        item = self.spy_list_widget.currentItem()
        self.spy_list_widget.spied_hosts.remove(item.host)
        self.spy_list_widget.takeItem(self.spy_list_widget.currentRow())
