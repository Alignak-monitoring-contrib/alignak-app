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
    TODO
"""

from logging import getLogger

from alignak_app.core.utils import get_image_path, get_css
from alignak_app.core.utils import get_time_diff_since_last_timestamp
from alignak_app.core.data_manager import data_manager
from alignak_app.models.item_model import get_icon_item, get_real_host_state_icon
from alignak_app.panel.service_data_widget import ServiceDataQWidget
from alignak_app.dock.events_widget import events_widget

from PyQt5.Qt import QLabel, QWidget, QIcon, Qt  # pylint: disable=no-name-in-module
from PyQt5.Qt import QGridLayout, QVBoxLayout, QHBoxLayout  # pylint: disable=no-name-in-module
from PyQt5.Qt import QTreeWidget, QTreeWidgetItem  # pylint: disable=no-name-in-module

logger = getLogger(__name__)


class ServicesQWidget(QWidget):
    """
        TODO
    """

    def __init__(self, parent=None):
        super(ServicesQWidget, self).__init__(parent)
        self.setStyleSheet(get_css())
        # Fields
        self.services_title = QLabel(_('Choose a host...'))
        self.host_item = None
        self.service_items = None
        self.services_tree_widget = QTreeWidget()
        self.service_data_widget = ServiceDataQWidget()

    def initialize(self):
        """
        TODO
        :return:
        """

        layout = QGridLayout()
        self.setLayout(layout)

        layout.addWidget(self.services_title, 0, 0, 1, 2)

        layout.addWidget(self.services_tree_widget, 1, 0, 1, 1)

        self.service_data_widget.initialize()
        layout.addWidget(self.service_data_widget, 1, 1, 1, 1)

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
            self.services_tree_widget.setParent(None)
            self.services_tree_widget = QTreeWidget()
            self.layout().addWidget(self.services_tree_widget)
            self.service_data_widget.setParent(None)
            self.service_data_widget = ServiceDataQWidget()
            self.service_data_widget.initialize()
            self.layout().addWidget(self.service_data_widget)

        # Make Global aggregation who are empty
        for service in self.service_items:
            if not service.data['aggregation']:
                service.data['aggregation'] = 'Global'

        # Sort list by aggregation
        newlist = sorted(self.service_items, key=lambda s: s.data['aggregation'])
        self.service_items = newlist

        # Get list of aggregations
        aggregations = []
        for service in self.service_items:
            if service.data['aggregation'] not in aggregations:
                aggregations.append(service.data['aggregation'])

        # Add QTreeWidgetItems
        for aggregation in aggregations:
            main_tree = QTreeWidgetItem([aggregation])
            for service in self.service_items:
                if service.data['aggregation'] == aggregation:
                    service_tree = QTreeWidgetItem()
                    icon_name = get_icon_item(
                        'service',
                        service.data['ls_state'],
                        service.data['ls_acknowledged'],
                        service.data['ls_downtimed']
                    )
                    service_tree.setText(0, service.name)
                    service_tree.setIcon(0, QIcon(get_image_path(icon_name)))
                    self.services_tree_widget.doubleClicked.connect(self.update_service_data)
                    main_tree.addChild(service_tree)

            self.services_tree_widget.addTopLevelItem(main_tree)

    def update_service_data(self):
        """
        Update ServiceDataqWidget

        """

        service_name = self.services_tree_widget.currentItem().text(0)
        self.services_title.setText(_('Services of %s' % self.host_item.name))

        if any(service_item.name == service_name for service_item in self.service_items):
            service = data_manager.get_item('service', service_name)

            self.services_tree_widget.setMaximumWidth(self.width() * 0.5)
            self.service_data_widget.setMaximumWidth(self.width() * 0.5)

            if service:
                self.service_data_widget.update_widget(
                    service,
                    self.host_item.item_id
                )
            else:
                self.service_data_widget.update_widget(
                    self.service_data_widget.service_item,
                    self.service_data_widget.host_id
                )


# Create services_widget object
services_widget = ServicesQWidget()
services_widget.initialize()
