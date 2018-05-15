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
    Services
    ++++++++
    Services manage creation of QWidget to display the services
"""

from logging import getLogger
from operator import itemgetter

from PyQt5.Qt import QTreeWidget, QTreeWidgetItem, QWidget, QIcon, QGridLayout, QSize, QListWidget
from PyQt5.Qt import Qt, QListWidgetItem

from alignak_app.backend.datamanager import data_manager
from alignak_app.items.item import get_icon_name
from alignak_app.utils.config import settings

from alignak_app.qobjects.common.frames import get_frame_separator
from alignak_app.qobjects.service.tree_item import ServiceTreeItem
from alignak_app.qobjects.service.services_dashboard import ServicesDashboardQWidget
from alignak_app.qobjects.service.service import ServiceDataQWidget

logger = getLogger(__name__)


class ServicesQWidget(QWidget):
    """
        Class wo create services QWidget
    """

    def __init__(self, parent=None):
        super(ServicesQWidget, self).__init__(parent)
        # Fields
        self.services = None
        self.services_tree_widget = QTreeWidget()
        self.services_list_widget = QListWidget()
        self.service_data_widget = ServiceDataQWidget()
        self.services_dashboard = ServicesDashboardQWidget()

    def initialize(self):
        """
        Initialize QWidget

        """

        layout = QGridLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)

        # Services dashboard
        self.services_dashboard.initialize()
        for state in self.services_dashboard.states_btns:
            self.services_dashboard.states_btns[state].clicked.connect(
                lambda _, s=state: self.filter_services(state=s)
            )
        layout.addWidget(self.services_dashboard, 0, 0, 1, 2)
        layout.addWidget(get_frame_separator(), 1, 0, 1, 2)

        # Services QTreeWidget
        self.services_tree_widget.setIconSize(QSize(32, 32))
        self.services_tree_widget.setAlternatingRowColors(True)
        self.services_tree_widget.header().close()
        layout.addWidget(self.services_tree_widget, 2, 0, 1, 1)

        # Services QListWidget
        self.services_list_widget.clicked.connect(self.update_service_data)
        self.services_list_widget.hide()
        layout.addWidget(self.services_list_widget, 2, 0, 1, 1)

        # Service DataWidget
        self.service_data_widget.initialize()
        layout.addWidget(self.service_data_widget, 2, 1, 1, 1)

    def filter_services(self, state):
        """
        Filter services with the wanted state

        :param state: state of service: OK, WARNING, NOT_MONITORED, DOWNTIME
        :return:
        """

        # Clear QListWidget and update filter buttons of services dashboard
        self.services_list_widget.clear()
        for btn_state in self.services_dashboard.states_btns:
            if btn_state != state:
                self.services_dashboard.states_btns[btn_state].setChecked(False)

        # Update QWidgets
        if self.sender().isChecked():
            self.set_filter_items(state)
            self.services_tree_widget.hide()
            self.services_list_widget.show()
        else:
            self.services_tree_widget.show()
            self.services_list_widget.hide()

    def set_filter_items(self, state):
        """
        Add filter items to QListWidget corresponding to "state"

        :param state: state of service to filter
        :type state: str
        """

        services_added = False
        if state in 'NOT_MONITORED':
            for service in self.services:
                if not service.data['active_checks_enabled'] and \
                        not service.data['passive_checks_enabled']and \
                        not service.data['ls_downtimed'] and \
                        not service.data['ls_acknowledged']:
                    self.add_filter_item(service)
                    services_added = True
        elif state in 'DOWNTIME':
            for service in self.services:
                if service.data['ls_downtimed']:
                    self.add_filter_item(service)
                    services_added = True
        elif state in 'ACKNOWLEDGE':
            for service in self.services:
                if service.data['ls_acknowledged']:
                    self.add_filter_item(service)
                    services_added = True
        else:
            for service in self.services:
                if service.data['ls_state'] in state:
                    self.add_filter_item(service)
                    services_added = True

        if not services_added:
            not_added_item = QListWidgetItem()
            not_added_item.setData(Qt.DecorationRole, QIcon(settings.get_image('services_ok')))
            not_added_item.setData(Qt.DisplayRole, _('No such services to display...'))
            self.services_list_widget.addItem(not_added_item)

    def add_filter_item(self, filter_item):
        """
        Add filter item to QListWidget

        :param filter_item: filter item (service)
        :type filter_item: alignak_app.items.service.Service
        """

        item = QListWidgetItem()
        monitored = \
            filter_item.data['passive_checks_enabled'] + filter_item.data['active_checks_enabled']
        icon_name = get_icon_name(
            filter_item.item_type,
            filter_item.data['ls_state'],
            filter_item.data['ls_acknowledged'],
            filter_item.data['ls_downtimed'],
            monitored
        )
        item.setData(Qt.DecorationRole, QIcon(settings.get_image(icon_name)))
        item.setData(Qt.DisplayRole, filter_item.get_display_name())
        item.setData(Qt.UserRole, filter_item.item_id)
        item.setToolTip(filter_item.get_tooltip())

        self.services_list_widget.addItem(item)

    def update_widget(self, services):
        """
        Update the QTreeWidget and its items

        :param services: list of :class:`Services <alignak_app.items.service.Service>` items
        :type services: list
        """

        self.services = services

        # Update services dashboard
        self.services_dashboard.update_widget(self.services)

        # Clear QTreeWidget
        self.services_tree_widget.clear()
        self.services_tree_widget.setIconSize(QSize(16, 16))

        if self.services:
            # Set as "Global" aggregation who are empty
            for service in self.services:
                if not service.data['aggregation']:
                    service.data['aggregation'] = 'Global'

            # First sort list by state then by aggregation
            newlist = sorted(
                self.services,
                key=lambda s: itemgetter('ls_state', 'ls_acknowledged', 'aggregation')(s.data)
            )
            self.services = newlist

            # Get list of aggregations
            aggregations = []
            for service in self.services:
                if service.data['aggregation'] not in aggregations:
                    aggregations.append(service.data['aggregation'])

            # Add QTreeWidgetItems
            for aggregation in aggregations:
                main_tree = QTreeWidgetItem()
                main_tree.setText(0, aggregation)
                main_tree.setIcon(0, QIcon(settings.get_image('tree')))
                main_tree.setToolTip(0, aggregation)
                for service in self.services:
                    if service.data['aggregation'] == aggregation:
                        service_tree = ServiceTreeItem()
                        service_tree.initialize(service)
                        service_tree.setToolTip(0, service.get_tooltip())
                        self.services_tree_widget.clicked.connect(self.update_service_data)
                        main_tree.addChild(service_tree)

                self.services_tree_widget.addTopLevelItem(main_tree)

            self.service_data_widget.hide()
        else:
            # If no services, reset service item to None and hide data widget
            self.service_data_widget.service_item = None
            self.service_data_widget.hide()

    def update_service_data(self):  # pragma: no cover
        """
        Update ServiceDataqWidget

        """

        service_item = self.sender().currentItem()

        if isinstance(service_item, (ServiceTreeItem, QListWidgetItem)):
            service = None
            # Get service
            if isinstance(service_item, ServiceTreeItem):
                service = data_manager.get_item('service', '_id', service_item.service_id)
            elif isinstance(service_item, QListWidgetItem):
                service = data_manager.get_item('service', '_id', service_item.data(Qt.UserRole))
            if not service:
                service = self.service_data_widget.service_item

            # Update QWidgets
            self.services_tree_widget.setMaximumWidth(self.width() * 0.5)
            self.services_list_widget.setMaximumWidth(self.width() * 0.5)
            self.service_data_widget.setMaximumWidth(self.width() * 0.5)
            self.service_data_widget.update_widget(service)
            self.services_dashboard.update_widget(self.services)
            self.service_data_widget.show()

            # Update Service Items (ServiceTreeItem, QListWidgetItem)
            if isinstance(service_item, ServiceTreeItem):
                service_item.update_item()
            else:
                monitored = \
                    service.data['passive_checks_enabled'] + service.data['active_checks_enabled']
                icon_name = get_icon_name(
                    'service',
                    service.data['ls_state'],
                    service.data['ls_acknowledged'],
                    service.data['ls_downtimed'],
                    monitored
                )

                service_item.setData(Qt.DecorationRole, QIcon(settings.get_image(icon_name)))
                service_item.setData(Qt.DisplayRole, service.get_display_name())
                service_item.setToolTip(service.get_tooltip())
