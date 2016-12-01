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
from logging import getLogger

from alignak_app import __application__
from alignak_app.backend.alignak_data import AlignakData
from alignak_app.core.utils import set_app_config

try:
    __import__('PyQt5')
    from PyQt5.QtWidgets import QWidget, QApplication, QGridLayout  # pylint: disable=no-name-in-module
    from PyQt5.Qt import QStringListModel, QCompleter, QLineEdit
except ImportError:  # pragma: no cover
    from PyQt4.Qt import QWidget  # pylint: disable=import-error


logger = getLogger(__name__)


class AppSearch(QWidget):
    """
    TODO
    """

    def __init__(self, parent=None):
        super(AppSearch, self).__init__(parent)
        self.setWindowTitle(__application__ + ': About')

    def create_search(self):
        """
        TODO
        """

        set_app_config()

        alignak_data = AlignakData()
        alignak_data.log_to_backend()

        current_hosts = alignak_data.get_host_states()

        model = QStringListModel()
        model.setStringList(current_hosts)

        completer = QCompleter()
        completer.setModel(model)

        lineedit = QLineEdit()
        lineedit.setCompleter(completer)

        layout = QGridLayout()

        layout.addWidget(lineedit)

        self.setLayout(layout)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    app_search = AppSearch()
    app_search.create_search()

    sys.exit(app.exec_())