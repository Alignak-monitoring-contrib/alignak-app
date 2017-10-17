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

from PyQt5.Qt import QApplication, QPushButton  # pylint: disable=no-name-in-module
from PyQt5.Qt import QCompleter, QLineEdit, QIcon, QHBoxLayout  # pylint: disable=no-name-in-module
from PyQt5.Qt import QStringListModel, Qt, QVBoxLayout, QWidget  # pylint: disable=no-name-in-module

from alignak_app.core.data_manager import data_manager
from alignak_app.core.utils import get_css, get_image_path
from alignak_app.frames.app_frame import AppQFrame, get_frame_separator
from alignak_app.widgets.panel.services_widget import services_widget
from alignak_app.widgets.panel.host_widget import host_widget
from alignak_app.widgets.panel.dashboard_widget import dashboard_widget

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
        self.app_widget = AppQFrame()
        self.hostnames_list = []

    def initialize(self, dock_width):
        """
        Create the QWidget with its items and layout.

        """

        logger.info('Create Panel View...')
        self.setLayout(self.layout)

        # Dashboard
        self.layout.addWidget(dashboard_widget)
        self.layout.setAlignment(dashboard_widget, Qt.AlignTop)
        self.layout.addWidget(get_frame_separator())

        # Search bar
        search_widget = self.get_search_widget()
        self.layout.addWidget(search_widget)
        self.layout.setAlignment(search_widget, Qt.AlignTop)

        # Host widgets
        self.layout.addWidget(host_widget)
        self.layout.setAlignment(host_widget, Qt.AlignTop)

        # Services widgets
        self.layout.addWidget(services_widget)

        # Align all widgets to Top
        self.layout.setAlignment(Qt.AlignTop)

        # Apply size and position on AppQWidget
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        desktop = QApplication.desktop().availableGeometry(screen)

        self.app_widget.initialize('')
        self.app_widget.add_widget(self)
        self.app_widget.resize(desktop.width() - dock_width, desktop.height())
        self.app_widget.move(0, 0)

        # Hide widgets for first start
        host_widget.hide()
        services_widget.hide()
        dashboard_widget.initialize()

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
        button = QPushButton(_('Search Host'), self)
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
            self.hostnames_list = data_manager.get_all_hostnames()
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
            # Update linesearch if needed
            hostnames_list = data_manager.get_all_hostnames()
            if hostnames_list != self.hostnames_list:
                self.create_line_search(hostnames_list)

            # Update QWidgets
            dashboard_widget.update_dashboard()
            dashboard_widget.show()
            host_widget.update_widget(self.line_search.text())
            host_widget.show()
            services_widget.set_data(self.line_search.text())
            services_widget.update_widget()
            services_widget.show()
        else:
            host_widget.hide()
            services_widget.hide()
