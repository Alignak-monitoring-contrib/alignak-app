#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015-2016:
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

from alignak_app.core.utils import get_css
from alignak_app.core.action_manager import ActionManager
from alignak_app.synthesis.host_synthesis import HostSynthesis
from alignak_app.widgets.app_widget import AppQWidget

try:
    __import__('PyQt5')
    from PyQt5.QtWidgets import QWidget, QPushButton  # pylint: disable=no-name-in-module
    from PyQt5.QtWidgets import QGridLayout  # pylint: disable=no-name-in-module
    from PyQt5.Qt import QStringListModel, QIcon  # pylint: disable=no-name-in-module
    from PyQt5.Qt import QCompleter, QLineEdit, QTimer  # pylint: disable=no-name-in-module
    from PyQt5.QtCore import Qt  # pylint: disable=no-name-in-module
except ImportError:  # pragma: no cover
    from PyQt4.Qt import QWidget, QPushButton  # pylint: disable=import-error
    from PyQt4.Qt import QGridLayout  # pylint: disable=import-error
    from PyQt4.Qt import QStringListModel, QIcon  # pylint: disable=import-error
    from PyQt4.Qt import QCompleter, QLineEdit, QTimer  # pylint: disable=import-error
    from PyQt4.QtCore import Qt  # pylint: disable=import-error


logger = getLogger(__name__)


class Synthesis(QWidget):
    """
        Class who create the Synthesis QWidget.
    """

    first_display = True

    def __init__(self, parent=None):
        super(Synthesis, self).__init__(parent)
        self.setMinimumSize(1000, 600)
        self.setStyleSheet(get_css())
        # Fields
        self.line_search = QLineEdit()
        self.app_backend = None
        self.action_manager = None
        self.host_synthesis = None
        self.app_widget = AppQWidget()

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

        # button
        button = QPushButton('Search / Refresh', self)
        button.setToolTip('Type a host name to display its data')
        button.clicked.connect(self.display_host_synthesis)
        self.line_search.returnPressed.connect(button.click)
        self.line_search.cursorPositionChanged.connect(button.click)

        layout = QGridLayout()
        self.setLayout(layout)

        layout.addWidget(self.line_search, 0, 0, 1, 4)
        layout.setAlignment(self.line_search, Qt.AlignTop)
        layout.addWidget(button, 0, 4, 1, 1)
        layout.setAlignment(button, Qt.AlignTop)

        self.app_widget.initialize('Host Synthesis View')
        self.app_widget.add_widget(self)

        refresh_timer = QTimer(self)
        refresh_timer.start(30000)
        refresh_timer.timeout.connect(self.display_host_synthesis)

    def create_line_search(self):
        """
        Add all hosts to QLineEdit and set QCompleter

        """

        # Create list for QStringModel
        hosts_list = []
        params = {'where': json.dumps({'_is_template': False})}

        all_hosts = self.app_backend.get('host', params)

        if all_hosts:
            for host in all_hosts['_items']:
                hosts_list.append(host['name'])

        model = QStringListModel()
        model.setStringList(hosts_list)

        # Create completer from model
        completer = QCompleter()
        try:
            completer.setFilterMode(Qt.MatchContains)
        except AttributeError as e:
            logger.warning('Can\'t use FilterMode : %s', e)

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
            old_checkbox_states = {}
            old_row = -1

            if host_name:
                backend_data = self.app_backend.get_host_with_services(host_name)

            # Remove host_synthesis and delete it
            if self.host_synthesis:
                if self.host_synthesis.services_list:
                    old_row = self.host_synthesis.services_list.currentRow()
                if self.host_synthesis.check_boxes:
                    old_checkbox_states = {
                        'OK': self.host_synthesis.check_boxes['OK'].isChecked(),
                        'UNKNOWN': self.host_synthesis.check_boxes['UNKNOWN'].isChecked(),
                        'WARNING': self.host_synthesis.check_boxes['WARNING'].isChecked(),
                        'UNREACHABLE': self.host_synthesis.check_boxes['UNREACHABLE'].isChecked(),
                        'CRITICAL': self.host_synthesis.check_boxes['CRITICAL'].isChecked(),
                    }
                self.layout().removeWidget(self.host_synthesis)
                self.host_synthesis.deleteLater()
                self.host_synthesis = None

            # Create the new host_synthesis
            self.host_synthesis = HostSynthesis(self.app_backend, self.action_manager)
            self.host_synthesis.initialize(backend_data)
            if old_row >= 0 and self.host_synthesis.services_list:
                self.host_synthesis.services_list.setCurrentRow(old_row)
            if old_checkbox_states and self.host_synthesis.check_boxes:
                self.host_synthesis.check_boxes['OK'].setChecked(
                    old_checkbox_states['OK']
                )
                self.host_synthesis.check_boxes['UNKNOWN'].setChecked(
                    old_checkbox_states['UNKNOWN']
                )
                self.host_synthesis.check_boxes['WARNING'].setChecked(
                    old_checkbox_states['WARNING']
                )
                self.host_synthesis.check_boxes['UNREACHABLE'].setChecked(
                    old_checkbox_states['UNREACHABLE']
                )
                self.host_synthesis.check_boxes['CRITICAL'].setChecked(
                    old_checkbox_states['CRITICAL']
                )
            self.layout().addWidget(self.host_synthesis, 1, 0, 1, 5)
