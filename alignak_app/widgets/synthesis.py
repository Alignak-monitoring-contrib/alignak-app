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

from alignak_app.popup.popup_title import PopupTitle
from alignak_app.backend.backend import AlignakBackend
from alignak_app.core.utils import set_app_config

try:
    __import__('PyQt5')
    from PyQt5.QtWidgets import QApplication  # pylint: disable=no-name-in-module
    from PyQt5.QtWidgets import QWidget, QPushButton  # pylint: disable=no-name-in-module
    from PyQt5.QtWidgets import QGridLayout, QLabel  # pylint: disable=no-name-in-module
    from PyQt5.Qt import QStringListModel  # pylint: disable=no-name-in-module
    from PyQt5.Qt import QCompleter, QLineEdit  # pylint: disable=no-name-in-module
except ImportError:  # pragma: no cover
    from PyQt4.Qt import QApplication  # pylint: disable=import-error
    from PyQt4.Qt import QWidget, QPushButton  # pylint: disable=import-error
    from PyQt4.Qt import QGridLayout, QLabel  # pylint: disable=import-error
    from PyQt4.Qt import QStringListModel  # pylint: disable=import-error
    from PyQt4.Qt import QCompleter, QLineEdit  # pylint: disable=import-error


logger = getLogger(__name__)


class AppSynthesis(QWidget):
    """
        Class who create the Synthesis QWidget.
    """

    def __init__(self, parent=None):
        super(AppSynthesis, self).__init__(parent)
        self.setMinimumSize(900, 700)
        self.setWindowTitle('Synthesis View')
        # Fields
        self.line_search = QLineEdit()
        self.result_label = None
        self.backend = AlignakBackend()

    def create_widget(self):
        """
        Create the QWidget

        """

        popup_title = self.add_title()
        self.create_search_bar()

        button = QPushButton('Search', self)
        button.clicked.connect(self.handle_button)
        self.line_search.returnPressed.connect(button.click)

        self.result_label = QLabel()
        self.result_label.setWordWrap(True)

        layout = QGridLayout()
        layout.addWidget(popup_title, 0, 0)
        layout.addWidget(self.line_search, 1, 0)
        layout.addWidget(button, 1, 1)
        layout.addWidget(self.result_label, 2, 0)

        self.setLayout(layout)
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
            services = ''
            for service in data['services']:
                services += '<p>' + str(service) + '</p>'
            if host_name:
                self.result_label.setText(
                    '<p>' +
                    str(data['host']) +
                    '</p>' +
                    services
                )
        else:
            self.result_label.setText('Not found !')

    def create_search_bar(self):
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

    @staticmethod
    def add_title():
        """
        Add title for QWidget

        """

        title = PopupTitle()
        title.create_title('Synthesis View')

        return title

# For Tests
if __name__ == '__main__':
    app = QApplication(sys.argv)

    set_app_config()

    synthesis = AppSynthesis()
    synthesis.backend.login()
    synthesis.create_widget()

    sys.exit(app.exec_())
