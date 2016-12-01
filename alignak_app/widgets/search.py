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
    TODO
"""

import sys
import json

from logging import getLogger

from alignak_app.popup.popup_title import PopupTitle
from alignak_app.backend.alignak_data import AlignakData
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


class AppSearch(QWidget):
    """
    TODO
    """

    def __init__(self, parent=None):
        super(AppSearch, self).__init__(parent)
        self.setMinimumSize(900, 700)
        # Fields
        self.line_edit = QLineEdit()
        self.result_label = QLabel()
        self.alignak_data = AlignakData()
        self.current_hosts = None

    def create_search(self):
        """
        TODO
        """

        set_app_config()

        self.alignak_data.log_to_backend()

        self.current_hosts = self.alignak_data.get_host_states()

        popup_title = self.add_title()
        self.add_search_bar()

        button = QPushButton('Search', self)
        button.clicked.connect(self.handle_button)
        self.line_edit.returnPressed.connect(button.click)

        layout = QGridLayout()
        layout.addWidget(popup_title, 0, 0)
        layout.addWidget(self.line_edit, 1, 0)
        layout.addWidget(button, 1, 1)
        layout.addWidget(self.result_label, 2, 0)

        self.setLayout(layout)
        self.show()

    def handle_button(self):
        """
        TODO
        """

        self.result_label.setWordWrap(True)
        item = self.line_edit.text()

        if item:
            self.result_label.setText(
                self.display_result(item)
            )
        else:
            self.result_label.setText('Not found !')

    def display_result(self, item):
        """
        TODO
        """

        params = {'where': json.dumps({'_is_template': False})}
        all_host = self.alignak_data.backend.get_all(
            self.alignak_data.backend.url_endpoint_root + '/host', params)

        result = 'Not found !'

        for host in all_host['_items']:
            print(host)
            print(host['name'])
            if host['name'] == item:
                result = str(host)

        return result

    def add_search_bar(self):
        """
        TODO
        """

        model = QStringListModel()
        model.setStringList(self.current_hosts)

        completer = QCompleter()
        completer.setModel(model)

        self.line_edit.setCompleter(completer)

    @staticmethod
    def add_title():
        """
        TODO
        """

        title = PopupTitle()
        title.create_title('Synthesis View')

        return title


if __name__ == '__main__':
    app = QApplication(sys.argv)

    app_search = AppSearch()
    app_search.create_search()

    sys.exit(app.exec_())
