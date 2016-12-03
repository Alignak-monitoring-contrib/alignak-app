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
    App Synthesis manage widget for Synthesis QWidget.
"""

import sys

from logging import getLogger

from alignak_app.core.utils import get_image_path, set_app_config
from alignak_app.popup.title import get_popup_title
from alignak_app.popup.host_view import HostView
from alignak_app.popup.services_view import ServicesView
from alignak_app.backend.backend import AlignakBackend

try:
    __import__('PyQt5')
    from PyQt5.QtWidgets import QApplication  # pylint: disable=no-name-in-module
    from PyQt5.QtWidgets import QWidget, QPushButton  # pylint: disable=no-name-in-module
    from PyQt5.QtWidgets import QGridLayout, QLabel  # pylint: disable=no-name-in-module
    from PyQt5.Qt import QStringListModel, QIcon  # pylint: disable=no-name-in-module
    from PyQt5.Qt import QCompleter, QLineEdit  # pylint: disable=no-name-in-module
    from PyQt5.QtCore import Qt  # pylint: disable=no-name-in-module
except ImportError:  # pragma: no cover
    from PyQt4.Qt import QApplication  # pylint: disable=import-error
    from PyQt4.Qt import QWidget, QPushButton  # pylint: disable=import-error
    from PyQt4.Qt import QGridLayout, QLabel  # pylint: disable=import-error
    from PyQt4.Qt import QStringListModel, QIcon  # pylint: disable=import-error
    from PyQt4.Qt import QCompleter, QLineEdit  # pylint: disable=import-error
    from PyQt4.QtCore import Qt  # pylint: disable=import-error


logger = getLogger(__name__)


class AppSynthesis(QWidget):
    """
        Class who create the Synthesis QWidget.
    """

    def __init__(self, parent=None):
        super(AppSynthesis, self).__init__(parent)
        self.setMinimumSize(900, 700)
        self.setWindowTitle('Synthesis View')
        self.setWindowIcon(QIcon(get_image_path('icon')))
        # Fields
        self.line_search = QLineEdit()
        self.host_view = None
        self.services_view = None
        self.backend = AlignakBackend()

    def create_widget(self, alignak_backend):
        """
        Create the QWidget

        """

        # Get backend
        self.backend = alignak_backend

        # Title
        popup_title = self.add_title()

        # Sums and other info
        sums = self.backend.counts()

        hosts_count = QLabel('Hosts : ' + str(sums['hosts']))
        services_count = QLabel('Services : ' + str(sums['services']))

        # Search Line
        self.create_line_search()

        # button
        button = QPushButton('Search', self)
        button.clicked.connect(self.handle_button)
        self.line_search.returnPressed.connect(button.click)

        # Create views
        self.host_view = HostView()
        self.host_view.init_view()
        self.services_view = ServicesView()

        # Layout
        # row, column, rowSpan, colSPan
        layout = QGridLayout()
        layout.addWidget(popup_title, 0, 0, 1, 4)
        layout.addWidget(hosts_count, 1, 0, 1, 1)
        layout.addWidget(services_count, 1, 2, 1, 1)
        layout.addWidget(self.line_search, 1, 0, 1, 3)
        layout.addWidget(button, 1, 3, 1, 1)
        layout.addWidget(self.host_view, 3, 0, 1, 1)
        layout.setAlignment(self.host_view, Qt.AlignLeft)
        layout.addWidget(self.services_view, 4, 0, 9, 1)

        self.setLayout(layout)

    def show_synthesis(self):
        """
        Show synthesis view for TrayIcon

        """

        self.show()

    def handle_button(self):
        """
        Handle Event when "line_search" is click.
        """

        # Get item that is searched
        host_name = self.line_search.text().rstrip()

        # Collect host data and associated services
        data = self.backend.get_all_host_data(host_name)

        # Write result ot "result_label"
        if data:
            self.host_view.update_view(data['host'])
            self.services_view.display_services(data['services'])
        else:
            self.host_view.setText('Not found !')

    def create_line_search(self):
        """
        All hosts to QLineEdit, with a QCompleter

        """

        # Create list for QStringModel
        hosts_list = []
        all_hosts = self.backend.get('host')
        for host in all_hosts['_items']:
            hosts_list.append(host['name'])

        model = QStringListModel()
        model.setStringList(hosts_list)

        # Create completer from model
        completer = QCompleter()
        completer.setModel(model)

        # Add completer to "line edit"
        self.line_search.setCompleter(completer)

    def add_title(self):
        """
        Add title for QWidget

        """

        title = get_popup_title('Synthesis View', self)

        return title

# For Tests
if __name__ == '__main__':
    app = QApplication(sys.argv)

    set_app_config()

    synthesis = AppSynthesis()
    backend = AlignakBackend()
    backend.login()
    synthesis.create_widget(backend)
    synthesis.show_synthesis()

    sys.exit(app.exec_())
