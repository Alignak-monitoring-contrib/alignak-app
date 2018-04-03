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
    Spy manage creation of QWidget to manage spied items
"""

from logging import getLogger

from PyQt5.Qt import QGridLayout, Qt, QWidget, QAbstractItemView, QListWidget, QPixmap, QIcon
from PyQt5.Qt import QTimer, QLabel

from alignak_app.backend.datamanager import data_manager
from alignak_app.utils.config import settings

from alignak_app.qobjects.events.item import EventItem
from alignak_app.qobjects.events.events import get_events_widget
from alignak_app.qobjects.events.spy_list import SpyQListWidget

logger = getLogger(__name__)


class SpyQWidget(QWidget):
    """
        Class who create QWidget for spied hosts
    """

    def __init__(self):
        super(SpyQWidget, self).__init__()
        self.host_services_lbl = QLabel(_('You are not spying on any hosts for now...'))
        self.spy_list_widget = SpyQListWidget()
        self.host_list_widget = QListWidget()
        self.spy_timer = QTimer()

    def initialize(self):
        """
        Intialize Spy QWidget

        """

        layout = QGridLayout()
        self.setLayout(layout)

        spy_icon = QLabel()
        spy_pixmap = QPixmap(settings.get_image('spy'))
        spy_icon.setPixmap(spy_pixmap)
        spy_icon.setScaledContents(True)
        spy_icon.setFixedSize(20, 20)
        layout.addWidget(spy_icon, 0, 0, 1, 1)
        layout.setAlignment(spy_icon, Qt.AlignRight)

        spy_title = QLabel(_('Spy Hosts'))
        spy_title.setObjectName('title')
        spy_title.setMinimumHeight(40)
        layout.addWidget(spy_title, 0, 1, 1, 1)

        hint_lbl = QLabel('Click to refresh, double-click to stop spying')
        hint_lbl.setObjectName('subtitle')
        layout.addWidget(hint_lbl, 1, 0, 1, 1)
        layout.setAlignment(hint_lbl, Qt.AlignCenter)

        self.host_services_lbl.setObjectName('subtitle')
        layout.addWidget(self.host_services_lbl, 1, 1, 1, 1)
        layout.setAlignment(self.host_services_lbl, Qt.AlignCenter)

        self.spy_list_widget.setDragDropMode(QAbstractItemView.DragDrop)
        self.spy_list_widget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.spy_list_widget.doubleClicked.connect(self.remove_event)
        self.spy_list_widget.setAcceptDrops(True)
        self.spy_list_widget.setWordWrap(True)
        self.spy_list_widget.insertItem(0, self.get_hint_item())
        self.spy_list_widget.item_dropped.connect(get_events_widget().remove_event)
        self.spy_list_widget.clicked.connect(
            lambda: self.manage_host_events(self.spy_list_widget.currentRow())
        )
        layout.addWidget(self.spy_list_widget, 2, 0, 1, 1)

        self.host_list_widget.setObjectName('spy')
        # self.host_list_widget.setMinimumWidth(500)
        layout.addWidget(self.host_list_widget, 2, 1, 1, 1)

        spy_interval = int(settings.get_config('Alignak-app', 'spy_interval')) * 1000
        self.spy_timer.setInterval(spy_interval)
        self.spy_timer.start()
        self.spy_timer.timeout.connect(self.send_spy_events)

    @staticmethod
    def get_hint_item():
        """
        Return an EventItem with a hint text

        :return: event item with hint text
        :rtype: EventItem
        """

        drop_hint_item = EventItem()
        drop_hint_item.setText(_('Drop host-related events here to spy on it...'))
        drop_hint_item.setIcon(QIcon(settings.get_image('spy')))
        drop_hint_item.setFlags(Qt.ItemIsDropEnabled)

        return drop_hint_item

    def send_spy_events(self):
        """
        Send event messages for all hosts who are spied

        """

        if self.spy_list_widget.spied_hosts:
            for host_id in self.spy_list_widget.spied_hosts:
                host = data_manager.get_item('host', host_id)

                get_events_widget().add_event(
                    EventItem.get_event_type(host.data),
                    _('Host %s, current state: %s') % (
                        host.get_display_name(), host.data['ls_state']),
                    host=host.item_id
                )

    def manage_host_events(self, row):
        """
        Manage spy events for a host, defined by current row of "spy_list_widget"

        :param row: current row of "spy_list_widget"
        :type row: int
        """

        # Clear QListWidget
        self.host_list_widget.clear()

        # Get Host and its services
        if row < 0:
            item = None
        else:
            item = self.spy_list_widget.item(row)

        if item:
            host = data_manager.get_item('host', item.host)

            if _('(new !)') in item.data(Qt.DisplayRole):
                item.setData(Qt.DisplayRole, item.data(Qt.DisplayRole).replace(_('(new !)'), ''))

            self.host_services_lbl.setText(_('Problems found for %s:') % host.get_display_name())
            services = data_manager.get_host_services(host.item_id)

            if services:
                problems = False
                for service in services:
                    if data_manager.is_problem('service', service.data):
                        problems = True
                        svc_state = _('Service %s is %s') % (
                            service.get_display_name(), service.data['ls_state']
                        )

                        event = EventItem()
                        event.initialize(
                            service.data['ls_state'],
                            svc_state,
                            host=host.item_id
                        )

                        self.host_list_widget.insertItem(0, event)

                if not problems:
                    event = EventItem()
                    event.initialize(
                        host.data['ls_state'],
                        _('%s is %s. Services of host seems managed.') % (
                            host.get_display_name(), host.data['ls_state']),
                        host=host.item_id
                    )
                    self.host_list_widget.insertItem(0, event)
            else:
                no_service_event = EventItem()
                no_service_event.initialize(
                    host.data['ls_state'],
                    _('%s is %s. No services.') % (host.get_display_name(), host.data['ls_state'])
                )
                self.host_list_widget.insertItem(0, no_service_event)

    def remove_event(self):
        """
        Remove item when user double click on an item, update parent tab text

        """

        item = self.spy_list_widget.currentItem()

        self.spy_list_widget.spied_hosts.remove(item.data(Qt.UserRole))
        self.spy_list_widget.takeItem(self.spy_list_widget.currentRow())

        if not self.spy_list_widget.spied_hosts:
            self.host_list_widget.clear()
            self.spy_list_widget.insertItem(0, self.get_hint_item())
            self.spy_list_widget.initialized = False
            self.host_services_lbl.setText(_('You are not spying on any hosts for now...'))

        if not self.spy_list_widget.selectedItems():
            self.manage_host_events(self.spy_list_widget.currentRow())

        self.update_parent_spytab()

    def update_parent_spytab(self):  # pragma: no cover - not testable
        """
        Update the parent spy tab text

        """

        if self.parent():
            if self.spy_list_widget.spied_hosts:
                self.parent().parent().setTabText(
                    self.parent().parent().indexOf(self),
                    _('Spied Hosts (%d)') % self.spy_list_widget.count()
                )
            else:
                # Remove hint item from count
                self.parent().parent().setTabText(
                    self.parent().parent().indexOf(self),
                    _('Spied Hosts (%d)') % (self.spy_list_widget.count() - 1)
                )
