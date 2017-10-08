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
    Panel QWidget manage the creation of Hosts and Services QWidgets
"""

from logging import getLogger

from alignak_app.app_widget import AppQWidget
from alignak_app.core.data_manager import data_manager
from alignak_app.core.utils import get_css, get_image_path
from alignak_app.panel.host_widget import host_widget
from alignak_app.panel.services_widget import services_widget
from alignak_app.items.item_model import get_icon_item

from PyQt5.Qt import QApplication, QPushButton, QLabel, QPixmap  # pylint: disable=no-name-in-module
from PyQt5.Qt import QCompleter, QLineEdit, QIcon, QHBoxLayout  # pylint: disable=no-name-in-module
from PyQt5.Qt import QStringListModel, Qt, QVBoxLayout, QWidget  # pylint: disable=no-name-in-module

logger = getLogger(__name__)


class PanelQWidget(QWidget):
    """
        Class who manage Panel with Host and Services QWidgets
    """

    def __init__(self, parent=None):
        super(PanelQWidget, self).__init__(parent)
        self.setStyleSheet(get_css())
        self.setWindowIcon(QIcon(get_image_path('icon')))
        # Fields
        self.layout = QVBoxLayout()
        self.line_search = QLineEdit()
        self.completer = QCompleter()
        self.app_widget = AppQWidget()
        self.hostnames_list = []

    def initialize(self):
        """
        Create the QWidget with its items and layout.

        """

        logger.info('Create Panel View...')

        self.setLayout(self.layout)

        self.app_widget.initialize('')
        self.app_widget.add_widget(self)

        # Define size and position of HostQWidget
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        desktop = QApplication.desktop().availableGeometry(screen)

        x_size = desktop.width() * 0.76
        y_size = desktop.height()

        pos_x = 0
        pos_y = 0

        self.app_widget.resize(x_size, y_size)
        self.app_widget.move(pos_x, pos_y)

        items_widget = self.get_dashboard_widget()
        self.layout.addWidget(items_widget)
        self.layout.setAlignment(items_widget, Qt.AlignTop)

        search_widget = self.get_search_widget()
        self.layout.addWidget(search_widget)
        self.layout.setAlignment(search_widget, Qt.AlignTop)

        self.layout.addWidget(host_widget)
        self.layout.setAlignment(host_widget, Qt.AlignTop)

        self.layout.addWidget(services_widget)

        self.layout.setAlignment(Qt.AlignTop)

        host_widget.hide()
        services_widget.hide()

    def get_dashboard_widget(self):  # pylint: disable=too-many-locals
        """
        TODO
        :return:
        """

        synthesis = data_manager.get_synthesis_count()

        # Hosts
        host_resume_widget = QWidget()
        host_layout = QHBoxLayout()
        host_resume_widget.setLayout(host_layout)

        hosts_icons = ['hosts_up', 'hosts_unreachable', 'hosts_down', 'acknowledge', 'downtime']
        hosts = synthesis['hosts']

        host_title = QLabel(_('Hosts:'))
        host_title.setObjectName('title')
        host_layout.addWidget(host_title)
        for icon in hosts_icons:
            item_icon = QLabel()
            item_icon.setPixmap(QPixmap(get_image_path(icon)))
            item_icon.setFixedSize(18, 18)
            item_icon.setScaledContents(True)
            item_icon.setToolTip(icon.replace('hosts_', '').upper())
            host_layout.addWidget(item_icon)
            nb_icon = QLabel(str(hosts[icon.replace('hosts_', '')]))
            nb_icon.setObjectName(icon)
            host_layout.addWidget(nb_icon)

        # Services
        service_resume_widget = QWidget()
        service_layout = QHBoxLayout()
        service_resume_widget.setLayout(service_layout)

        services_icons = [
            'services_ok', 'services_warning', 'services_critical', 'services_unknown',
            'services_unreachable', 'acknowledge', 'downtime'
        ]
        services = synthesis['services']

        service_title = QLabel(_('Services:'))
        service_title.setObjectName('title')
        service_layout.addWidget(service_title)
        for icon in services_icons:
            item_icon = QLabel()
            item_icon.setPixmap(QPixmap(get_image_path(icon)))
            item_icon.setFixedSize(18, 18)
            item_icon.setScaledContents(True)
            item_icon.setToolTip(icon.replace('services_', '').upper())
            service_layout.addWidget(item_icon)
            nb_icon = QLabel(str(services[icon.replace('services_', '')]))
            nb_icon.setObjectName(icon)
            service_layout.addWidget(nb_icon)

        widget = QWidget()
        layout = QHBoxLayout()
        widget.setLayout(layout)

        layout.addWidget(host_resume_widget)
        layout.addWidget(service_resume_widget)

        return widget

    def get_search_widget(self):
        """
        Create and return the search QWidget

        :return: search QWidget
        :rtype: QWidget
        """

        widget = QWidget()
        layout = QHBoxLayout()
        widget.setLayout(layout)

        # Search button
        button = QPushButton(_('Search / Refresh Host'), self)
        button.setObjectName('search')
        button.setFixedHeight(25)
        button.setToolTip(_('Search Host'))
        button.clicked.connect(self.display_host)
        layout.addWidget(button)

        self.line_search.setFixedHeight(button.height())
        self.line_search.returnPressed.connect(button.click)
        self.line_search.cursorPositionChanged.connect(button.click)
        layout.addWidget(self.line_search)

        self.create_line_search()

        return widget

    def create_line_search(self, hostnames_list=None):
        """
        Add all hosts to QLineEdit and set QCompleter

        :param hostnames_list: list of host names
        :type hostnames_list: list
        """

        # Get QStringListModel
        model = self.completer.model()
        if not model:
            model = QStringListModel()

        if not hostnames_list:
            self.hostnames_list = data_manager.get_all_host_name()
        else:
            self.hostnames_list = hostnames_list

        model.setStringList(self.hostnames_list)

        # Configure QCompleter from model
        self.completer.setFilterMode(Qt.MatchContains)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setModel(model)

        # Add completer to QLineEdit
        self.line_search.setCompleter(self.completer)
        self.line_search.setPlaceholderText(_('Type a host name to display its data'))
        self.line_search.setToolTip(_('Type a host name to display its data'))

    def display_host(self):
        """
        Display and update HostQWidget

        """

        if self.line_search.text() in self.hostnames_list:
            hostnames_list = data_manager.get_all_host_name()
            if hostnames_list != self.hostnames_list:
                self.create_line_search(hostnames_list)
            host_widget.update_widget(self.line_search.text())
            host_widget.show()
            services_widget.set_data(self.line_search.text())
            services_widget.update_widget()
            services_widget.show()
        else:
            host_widget.hide()
            services_widget.hide()


# Initialize PanelQWidget
panel_widget = PanelQWidget()
panel_widget.initialize()
