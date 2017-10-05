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

from alignak_app.core.utils import get_css, get_app_config
from alignak_app.core.action_manager import ActionManager
from alignak_app.core.data_manager import data_manager
from alignak_app.widgets.host_widget import host_widget
from alignak_app.widgets.app_widget import AppQWidget

from PyQt5.QtWidgets import QWidget, QPushButton  # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QVBoxLayout, QApplication  # pylint: disable=no-name-in-module
from PyQt5.Qt import QStringListModel, QHBoxLayout  # pylint: disable=no-name-in-module
from PyQt5.Qt import QCompleter, QLineEdit, QTimer  # pylint: disable=no-name-in-module
from PyQt5.QtCore import Qt  # pylint: disable=no-name-in-module


logger = getLogger(__name__)


class PanelQWidget(QWidget):
    """
        TODO
    """

    def __init__(self, parent=None):
        super(PanelQWidget, self).__init__(parent)
        self.setStyleSheet(get_css())
        # Fields
        self.layout = QVBoxLayout()
        self.line_search = QLineEdit()
        self.completer = QCompleter()
        self.app_widget = AppQWidget()

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

        search_widget = self.get_search_widget()
        self.layout.addWidget(search_widget)
        self.layout.setAlignment(search_widget, Qt.AlignTop)

        self.layout.addWidget(host_widget)

    def get_search_widget(self):
        """
        TODO
        :return:
        """

        widget = QWidget()
        layout = QHBoxLayout()
        widget.setLayout(layout)

        # Search button
        button = QPushButton(_('Search / Refresh Host'), self)
        button.setObjectName('search')
        button.setFixedHeight(22)
        button.setToolTip(_('Search Host'))
        button.clicked.connect(self.display_host)
        layout.addWidget(button)

        self.line_search.setFixedHeight(button.height())
        self.line_search.returnPressed.connect(button.click)
        layout.addWidget(self.line_search)

        self.create_line_search()

        return widget

    def create_line_search(self):
        """
        Add all hosts to QLineEdit and set QCompleter

        """

        # Get QStringListModel
        model = self.completer.model()
        if not model:
            model = QStringListModel()

        hosts_list = data_manager.get_all_host_name()
        model.setStringList(hosts_list)

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
        TODO
        :return:
        """

        host_widget.set_data(self.line_search.text())
        host_widget.initialize()


# Initialize PanelQWidget
panel_widget = PanelQWidget()
panel_widget.initialize()
