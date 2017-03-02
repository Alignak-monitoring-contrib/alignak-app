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
    App Synthesis manage widget for Host Synthesis QWidget.
"""

import json

from logging import getLogger

from alignak_app.core.utils import get_css, get_app_config
from alignak_app.core.action_manager import ActionManager
from alignak_app.synthesis.host_synthesis import HostSynthesis
from alignak_app.widgets.app_widget import AppQWidget

from PyQt5.QtWidgets import QWidget, QPushButton  # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QGridLayout  # pylint: disable=no-name-in-module
from PyQt5.Qt import QStringListModel  # pylint: disable=no-name-in-module
from PyQt5.Qt import QCompleter, QLineEdit, QTimer  # pylint: disable=no-name-in-module
from PyQt5.QtCore import Qt  # pylint: disable=no-name-in-module


logger = getLogger(__name__)


class Synthesis(QWidget):
    """
        Class who create the Synthesis QWidget.
    """

    first_display = True

    def __init__(self, parent=None):
        super(Synthesis, self).__init__(parent)
        self.setStyleSheet(get_css())
        # Fields
        self.line_search = QLineEdit()
        self.app_backend = None
        self.action_manager = None
        self.host_synthesis = None
        self.app_widget = AppQWidget()
        self.old_checkbox_states = {}

    def initialize(self, app_backend):
        """
        Create the QWidget with its items and layout.

        :param app_backend: app_backend of alignak.
        :type app_backend: alignak_app.core.backend.AppBackend
        """

        logger.info('Create Synthesis View...')

        # App_backend
        self.app_backend = app_backend
        self.action_manager = ActionManager(app_backend)

        layout = QGridLayout()
        self.setLayout(layout)

        # button
        button = QPushButton('Search / Refresh Host', self)
        button.setObjectName('search')
        button.setFixedHeight(22)
        button.setToolTip('Search Host')
        button.clicked.connect(self.display_host_synthesis)
        layout.addWidget(button, 0, 4, 1, 1)
        layout.setAlignment(button, Qt.AlignTop)

        self.line_search.setFixedHeight(button.height())
        self.line_search.returnPressed.connect(button.click)
        self.line_search.cursorPositionChanged.connect(button.click)
        layout.addWidget(self.line_search, 0, 0, 1, 4)
        layout.setAlignment(self.line_search, Qt.AlignTop)

        self.app_widget.initialize('Host Synthesis View')
        self.app_widget.add_widget(self)
        self.app_widget.setMinimumSize(1300, 750)

        refresh_interval = int(get_app_config('Alignak-App', 'item_interval'))
        if bool(refresh_interval) and refresh_interval > 0:
            logger.debug('Hosts synthesis will be refresh in %ss', str(refresh_interval))
            refresh_interval *= 1000
        else:
            logger.error(
                '"item_interval" option must be greater than 0. Replace by default: 30s'
            )
            refresh_interval = 30000

        refresh_timer = QTimer(self)
        refresh_timer.start(refresh_interval)
        refresh_timer.timeout.connect(self.display_host_synthesis)

    def create_line_search(self):
        """
        Add all hosts to QLineEdit and set QCompleter

        """

        # Create list for QStringModel
        hosts_list = []
        params = {'where': json.dumps({'_is_template': False})}

        all_hosts = self.app_backend.get('host', params, ['name'])

        if all_hosts:
            for host in all_hosts['_items']:
                hosts_list.append(host['name'])

        model = QStringListModel()
        model.setStringList(hosts_list)

        # Create completer from model
        completer = QCompleter()
        completer.setFilterMode(Qt.MatchContains)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setModel(model)

        # Add completer to "line edit"
        self.line_search.setCompleter(completer)
        self.line_search.setPlaceholderText('Type a host name to display its data')
        self.line_search.setToolTip('Type a host name to display its data')

    def display_host_synthesis(self):
        """
        Display Synthesis QWidget. Remove and delete HostSynthesis if exists

        """

        if self.isVisible():
            # If first display, create line search from hosts list
            if self.first_display:
                self.create_line_search()
                self.first_display = False

            host_name = str(self.line_search.text()).rstrip()
            backend_data = None
            old_row = -1

            if host_name:
                backend_data = self.app_backend.get_host_with_services(host_name)

            # Store old data, remove and delete host_synthesis
            if self.host_synthesis:
                # Store old data
                if self.host_synthesis.services_list:
                    old_row = self.host_synthesis.services_list.currentRow()
                if self.host_synthesis.check_boxes:
                    for key in self.host_synthesis.check_boxes:
                        self.old_checkbox_states[key] = \
                            self.host_synthesis.check_boxes[key].isChecked()

                # Remove and delete QWidget
                self.layout().removeWidget(self.host_synthesis)
                self.host_synthesis.deleteLater()
                self.host_synthesis = None

            # Create the new host_synthesis
            self.host_synthesis = HostSynthesis(self.action_manager)
            self.host_synthesis.initialize(backend_data)

            # Restore old data
            if old_row >= 0 and self.host_synthesis.services_list:
                self.host_synthesis.services_list.setCurrentRow(old_row)
            if self.old_checkbox_states and self.host_synthesis.check_boxes:
                for key, checked in self.old_checkbox_states.items():
                    try:
                        self.host_synthesis.check_boxes[key].setChecked(checked)
                    except KeyError as e:
                        logger.warning('Can\'t reapply filter [%s]: %s', e, checked)

            self.layout().addWidget(self.host_synthesis, 1, 0, 1, 5)
