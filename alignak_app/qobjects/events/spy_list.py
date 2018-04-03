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
    Spy List
    ++++++++
    Spy List manage creation of custom QListWidget for host items who are spied
"""

from logging import getLogger

from PyQt5.Qt import pyqtSignal, QSize, Qt, QListWidget

from alignak_app.backend.datamanager import data_manager

from alignak_app.qobjects.events.item import EventItem

logger = getLogger(__name__)


class SpyQListWidget(QListWidget):
    """
        Class who create QListWidget for spied hosts
    """

    item_dropped = pyqtSignal(EventItem, name="remove_item")

    def __init__(self):
        super(SpyQListWidget, self).__init__()
        self.setIconSize(QSize(16, 16))
        # Fields
        self.initialized = False
        self.spied_hosts = []

    def add_spy_host(self, host_id):
        """
        Add a host to spied list and create corresponding EventItem()

        :param host_id: "_id" of host to spy
        :type host_id: str
        """

        if self.parent():
            self.parent().host_services_lbl.setText(_('Select spy host to display its problems...'))

        if not self.initialized:
            # Remove Hint item
            self.takeItem(0)
            self.initialized = True

        if host_id not in self.spied_hosts:
            self.spied_hosts.append(host_id)
            host = data_manager.get_item('host', '_id', host_id)
            if host:
                event_item = EventItem()
                event_item.initialize(
                    EventItem.get_event_type(host.data),
                    _('Host %s, current state: %s (new !)') % (
                        host.get_display_name(), host.data['ls_state']),
                    host=host.item_id
                )
                self.insertItem(0, event_item)

                logger.info('Spy a new host: %s', host.name)
                logger.debug('... with id: %s', host_id)

    def dragMoveEvent(self, event):  # pragma: no cover - not testable
        """
        Override dragMoveEvent.
         Only accept EventItem() objects who have a ``Qt.UserRole`` and not already in "spied_hosts"

        :param event: event triggered when something move
        """

        if isinstance(event.source().currentItem(), EventItem):
            if event.source().currentItem().data(Qt.UserRole):
                if event.source().currentItem().data(Qt.UserRole) not in self.spied_hosts:
                    event.accept()
                else:
                    event.ignore()
            else:
                event.ignore()
        else:
            event.ignore()

    def dropEvent(self, event):  # pragma: no cover - not testable
        """
        Override dropEvent.
         Get dropped item data, create a new one, and delete the one who is in EventsQWidget

        :param event: event triggered when something is dropped
        """

        self.add_spy_host(event.source().currentItem().data(Qt.UserRole))

        # Remove the item dropped and original, to let only new one created
        row = self.row(event.source().currentItem())
        self.takeItem(row)
        self.item_dropped.emit(event.source().currentItem())

        self.parent().update_parent_spytab()
