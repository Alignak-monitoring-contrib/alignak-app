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
import sys
from logging import getLogger

from alignak_app.core.backend import AppBackend
from alignak_app.core.utils import get_image_path, set_app_config
from alignak_app.synthesis.host_view import HostView
from alignak_app.synthesis.services_view import ServicesView
from alignak_app.widgets.title import get_widget_title

try:
    __import__('PyQt5')
    from PyQt5.QtWidgets import QApplication  # pylint: disable=no-name-in-module
    from PyQt5.QtWidgets import QWidget, QPushButton  # pylint: disable=no-name-in-module
    from PyQt5.QtWidgets import QGridLayout  # pylint: disable=no-name-in-module
    from PyQt5.Qt import QStringListModel, QIcon  # pylint: disable=no-name-in-module
    from PyQt5.Qt import QCompleter, QLineEdit  # pylint: disable=no-name-in-module
    from PyQt5.QtCore import Qt  # pylint: disable=no-name-in-module
except ImportError:  # pragma: no cover
    from PyQt4.Qt import QApplication  # pylint: disable=import-error
    from PyQt4.Qt import QWidget, QPushButton  # pylint: disable=import-error
    from PyQt4.Qt import QGridLayout  # pylint: disable=import-error
    from PyQt4.Qt import QStringListModel, QIcon  # pylint: disable=import-error
    from PyQt4.Qt import QCompleter, QLineEdit  # pylint: disable=import-error
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
        # Fields
        self.line_search = QLineEdit()
        self.host_view = None
        self.services_view = None
        self.app_backend = None

    def create_widget(self, app_backend):
        """
        Create the QWidget with its items and layout.

        :param app_backend: app_backend of alignak.
        :type app_backend: AppBackend
        """

        logger.info('Create Synthesis View...')
        # Get app_backend
        self.app_backend = app_backend

        # Title
        popup_title = get_widget_title('host synthesis view', self)

        # Search Line
        self.create_line_search()

        # button
        button = QPushButton('Search / Refresh', self)
        button.setToolTip('Type name of a host to display his data')
        button.clicked.connect(self.handle_button)
        self.line_search.returnPressed.connect(button.click)

        # Create views
        self.host_view = HostView(self)
        self.host_view.init_view(self.app_backend)
        self.services_view = ServicesView(self)

        # Layout
        # row, column, rowSpan, colSPan
        layout = QGridLayout()
        layout.addWidget(popup_title, 0, 0, 1, 4)
        layout.addWidget(self.line_search, 1, 0, 1, 3)
        layout.addWidget(button, 1, 3, 1, 1)
        layout.addWidget(self.host_view, 2, 0, 1, 4)
        layout.setAlignment(self.host_view, Qt.AlignLeft)
        layout.addWidget(self.services_view, 3, 0, 8, 4)

        self.setLayout(layout)

    def show_synthesis(self):
        """
        Show synthesis view for TrayIcon

        """

        self.show()

    def handle_button(self):
        """
        Handle Event when "line_search" is clicked.

        """

        # Get item that is searched
        host_name = str(self.line_search.text()).rstrip()

        logger.debug('Desired host: ' + host_name)

        # Collect host data and associated services
        data = self.app_backend.get_all_host_data(host_name)

        # Write result ot "result_label"
        if data:
            self.host_view.update_view(data)
            self.services_view.display_services(data['services'], data['host']['name'])
        else:
            data = {
                'host': {
                    'name': host_name,
                    'alias': 'NOT FOUND',
                    'ls_state': 'NOT FOUND',
                    'ls_last_check': 'NOT FOUND',
                    'ls_output': 'NOT FOUND',
                    'ls_acknowledged': False,
                    'ls_downtimed': False
                },
                'services': None
            }
            self.host_view.update_view(data)
            self.services_view.display_services(None, 'NOT KNOWN')

    def create_line_search(self):
        """
        Add all hosts to QLineEdit and set QCompleter

        """

        # Create list for QStringModel
        hosts_list = []
        params = {'where': json.dumps({'_is_template': False})}

        all_hosts = self.app_backend.get('host', params)

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


# For Tests
if __name__ == '__main__':
    app = QApplication(sys.argv)

    set_app_config()

    synthesis = Synthesis()
    backend = AppBackend()
    backend.login()
    synthesis.create_widget(backend)
    synthesis.show_synthesis()

    sys.exit(app.exec_())
