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
from alignak_app.qobjects.panel.service_tree_item import ServiceTreeItem
from alignak_app.qobjects.panel.number_services import NumberServicesQWidget
from alignak_app.qobjects.panel.service import ServiceDataQWidget

logger = getLogger(__name__)


class ServicesQWidget(QWidget):
    """
        Class wo create services QWidget
    """

    def __init__(self, parent=None):
        super(ServicesQWidget, self).__init__(parent)
        # Fields
        self.host_item = None
        self.service_items = None
        self.services_tree_widget = QTreeWidget()
        self.service_data_widget = ServiceDataQWidget()
        self.nb_services_widget = NumberServicesQWidget()

    def initialize(self):
        """
        Initialize QWidget

        """

        layout = QGridLayout()
        self.setLayout(layout)

        self.nb_services_widget.initialize()
        layout.addWidget(self.nb_services_widget, 0, 0, 1, 2)
        layout.addWidget(get_frame_separator(), 1, 0, 1, 2)

        self.services_tree_widget.setIconSize(QSize(32, 32))
        layout.addWidget(self.services_tree_widget, 2, 0, 1, 1)

        self.service_data_widget.initialize()
        layout.addWidget(self.service_data_widget, 2, 1, 1, 1)

    def set_data(self, hostname):
        """
        Set data of host and service

        :param hostname: name of host to display
        :type hostname: str
        """

        host_and_services = data_manager.get_host_with_services(hostname)
        self.host_item = host_and_services['host']
        self.service_items = host_and_services['services']

    def update_widget(self):
        """
        Update the service QWidget

        """

        if self.services_tree_widget:
            self.nb_services_widget.setParent(None)
            self.nb_services_widget = NumberServicesQWidget()
            self.nb_services_widget.initialize()
            self.nb_services_widget.update_widget(self.service_items, self.host_item.name)
            self.layout().addWidget(self.nb_services_widget, 0, 0, 1, 2)
            self.services_tree_widget.setParent(None)
            self.services_tree_widget = QTreeWidget()
            self.services_tree_widget.setAlternatingRowColors(True)
            self.services_tree_widget.header().close()
            self.layout().addWidget(self.services_tree_widget, 2, 0, 1, 1)
            self.service_data_widget.setParent(None)
            self.service_data_widget = ServiceDataQWidget()
            self.service_data_widget.initialize()
            self.layout().addWidget(self.service_data_widget, 2, 1, 1, 1)

        # Make Global aggregation who are empty
        for service in self.service_items:
            if not service.data['aggregation']:
                service.data['aggregation'] = 'Global'

        # First sort list by state then by aggregation
        newlist = sorted(
            self.service_items,
            key=lambda s: itemgetter('ls_state', 'ls_acknowledged', 'aggregation')(s.data)
        )
        self.service_items = newlist

        # Get list of aggregations
        aggregations = []
        for service in self.service_items:
            if service.data['aggregation'] not in aggregations:
                aggregations.append(service.data['aggregation'])

        # Add QTreeWidgetItems
        for aggregation in aggregations:
            main_tree = QTreeWidgetItem()
            main_tree.setText(0, aggregation)
            main_tree.setIcon(0, QIcon(settings.get_image('tree')))
            main_tree.setToolTip(0, aggregation)
            for service in self.service_items:
                if service.data['aggregation'] == aggregation:
                    service_tree = ServiceTreeItem()
                    service_tree.initialize(service)
                    service_tree.setToolTip(0, service.get_tooltip())
                    self.services_tree_widget.clicked.connect(self.update_service_data)
                    main_tree.addChild(service_tree)

            self.services_tree_widget.addTopLevelItem(main_tree)

    def update_service_data(self):
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
