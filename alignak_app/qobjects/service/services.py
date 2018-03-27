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

from PyQt5.Qt import QTreeWidget, QTreeWidgetItem, QWidget, QIcon, QGridLayout, QSize

from alignak_app.backend.datamanager import data_manager
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
        self.host = None
        self.services = None
        self.services_tree_widget = QTreeWidget()
        self.service_data_widget = ServiceDataQWidget()
        self.services_dashboard = ServicesDashboardQWidget()

    def initialize(self):
        """
        Initialize QWidget

        """

        layout = QGridLayout()
        self.setLayout(layout)

        self.services_dashboard.initialize()
        layout.addWidget(self.services_dashboard, 0, 0, 1, 2)
        layout.addWidget(get_frame_separator(), 1, 0, 1, 2)

        self.services_tree_widget.setIconSize(QSize(32, 32))
        self.services_tree_widget.setAlternatingRowColors(True)
        self.services_tree_widget.header().close()
        layout.addWidget(self.services_tree_widget, 2, 0, 1, 1)

        self.service_data_widget.initialize()
        layout.addWidget(self.service_data_widget, 2, 1, 1, 1)

    def update_widget(self, host, services):
        """
        Update the QTreeWidget and its items

        :param host: the Host item
        :type host: alignak_app.items.host.Host
        :param services: list of :class:`Services <alignak_app.items.service.Service>` items
        :type services: list
        """

        self.host = host
        self.services = services

        # Update services dashboard
        self.services_dashboard.update_widget(self.services, self.host.name)

        # Clear QTreeWidget
        self.services_tree_widget.clear()
        self.services_tree_widget.setIconSize(QSize(16, 16))

        if self.services:
            # Make Global aggregation who are empty
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

        service_tree_item = self.services_tree_widget.currentItem()

        if isinstance(service_tree_item, ServiceTreeItem):
            service = data_manager.get_item('service', '_id', service_tree_item.service_id)

            self.services_tree_widget.setMaximumWidth(self.width() * 0.5)
            self.service_data_widget.setMaximumWidth(self.width() * 0.5)

            if service:
                self.service_data_widget.update_widget(service)
            else:
                self.service_data_widget.update_widget(self.service_data_widget.service_item)

            self.service_data_widget.show()
            service_tree_item.update_item()
