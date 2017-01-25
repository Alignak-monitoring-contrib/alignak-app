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

from alignak_app.core.utils import get_image_path, get_css
from alignak_app.core.action_manager import ActionManager, ACK, DOWNTIME, PROCESS
from alignak_app.synthesis.host import Host
from alignak_app.synthesis.services_view import ServicesView
from alignak_app.widgets.app_widget import AppQWidget
from alignak_app.widgets.banner import send_banner

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

    def __init__(self, parent=None):
        super(Synthesis, self).__init__(parent)
        self.setMinimumSize(1000, 700)
        self.setWindowTitle('Hosts Synthesis View')
        self.setWindowIcon(QIcon(get_image_path('icon')))
        self.setStyleSheet(get_css())
        # Fields
        self.line_search = QLineEdit()
        self.host_view = None
        self.services_view = None
        self.app_backend = None
        self.action_manager = None
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

        # Search Line
        self.create_line_search()

        # button
        button = QPushButton('Search / Refresh', self)
        button.setToolTip('Type name of a host to display his data')
        button.clicked.connect(self.display_views)
        self.line_search.returnPressed.connect(button.click)

        # Create views
        self.host_view = Host(self)
        self.host_view.init_view(self.app_backend, self.action_manager)
        self.services_view = ServicesView(self.action_manager, self.app_backend)

        # Layout
        # row, column, rowSpan, colSPan
        layout = QGridLayout()
        layout.addWidget(self.line_search, 0, 0, 1, 3)
        layout.addWidget(button, 0, 3, 1, 1)
        layout.addWidget(self.host_view, 1, 0, 1, 4)
        layout.setAlignment(self.host_view, Qt.AlignLeft)

        layout.addWidget(self.services_view, 2, 0, 1, 4)

        self.setLayout(layout)

        self.app_widget.initialize('Host Synthesis View')
        self.app_widget.add_widget(self)

        # Refresh and Action process
        refresh_timer = QTimer(self)
        refresh_timer.start(10000)
        refresh_timer.timeout.connect(self.refresh_all_views)

        action_timer = QTimer(self)
        action_timer.start(10000)
        action_timer.timeout.connect(self.check_action_manager)

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
        completer.setModel(model)

        # Add completer to "line edit"
        self.line_search.setCompleter(completer)
        self.line_search.setPlaceholderText('Type a host name to display its data')
        self.line_search.setToolTip('Type a host name to display its data')

    def display_views(self):  # pragma: no cover
        """
        Handle Event when "line_search" is clicked.

        """

        # Get item that is searched
        host_name = str(self.line_search.text()).rstrip()

        logger.debug('Desired host: ' + host_name)

        # Collect host data and associated services
        data = self.app_backend.get_host_with_services(host_name)

        # Write result ot "result_label"
        if data:
            self.host_view.update_view(data)
            self.services_view.display_services(data['services'], data['host'])
        else:
            data = {
                'host': {
                    'name': host_name,
                    'alias': 'N/A',
                    'ls_state': 'N/A',
                    'ls_last_check': 0.0,
                    'ls_output': 'N/A',
                    'ls_acknowledged': False,
                    'ls_downtimed': False
                },
                'services': None
            }
            self.host_view.update_view(data)
            self.services_view.display_services(None, {'name': 'NO HOST'})

    def refresh_all_views(self):
        """
        Refresh Host and Service QWidgets

        """

        host_name = str(self.line_search.text()).rstrip()

        # Collect host data and associated services
        data = self.app_backend.get_host_with_services(host_name)

        # Refresh
        if data:
            self.host_view.update_view(data)
            self.services_view.update_services()
        else:
            data = {
                'host': {
                    'name': host_name,
                    'alias': 'N/A',
                    'ls_state': 'N/A',
                    'ls_last_check': 0.0,
                    'ls_output': 'N/A',
                    'ls_acknowledged': False,
                    'ls_downtimed': False
                },
                'services': None
            }
            self.host_view.update_view(data)
            self.services_view.display_services(None, {'name': 'NO HOST'})

    def check_action_manager(self):
        """
        Check ActionManager and send banner if items to send

        """

        items_to_send = self.action_manager.check_items()
        actions = [ACK, DOWNTIME]

        if items_to_send:
            # Send ACKs and DOWNTIMEs
            for action in actions:
                title = action.replace('action', '').capitalize()
                # For Hosts
                if items_to_send[action]['hosts']:
                    for item in items_to_send[action]['hosts']:
                        host = self.app_backend.get_host(item['host_id'])
                        send_banner('OK', '%s for %s is done !' % (title, host['name']))
                # For Services
                if items_to_send[action]['services']:
                    for item in items_to_send[action]['services']:
                        service = self.app_backend.get_service(item['host_id'], item['service_id'])
                        send_banner('OK', '%s for %s is done !' % (title, service['name']))

            # Send PROCESS
            if items_to_send[PROCESS]:
                for item in items_to_send[PROCESS]:
                    requested_action = item['post']['_links']['self']['title'].replace('Action', '')
                    action_title = requested_action.capitalize()
                    send_banner('OK', '%s for %s is processed...' % (action_title, item['name']))
