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

try:
    __import__('PyQt5')
    from PyQt5.QtWidgets import QApplication  # pylint: disable=no-name-in-module
    from PyQt5.QtWidgets import QWidget, QVBoxLayout  # pylint: disable=no-name-in-module
    from PyQt5.QtWidgets import QGridLayout, QLabel  # pylint: disable=no-name-in-module
    from PyQt5.Qt import QPixmap  # pylint: disable=no-name-in-module
except ImportError:  # pragma: no cover
    from PyQt4.Qt import QApplication  # pylint: disable=import-error
    from PyQt4.Qt import QWidget, QVBoxLayout  # pylint: disable=import-error
    from PyQt4.Qt import QGridLayout, QLabel  # pylint: disable=import-error
    from PyQt4.Qt import QPixmap  # pylint: disable=import-error


logger = getLogger(__name__)


class ServicesView(QWidget):
    """
        Class who create the Synthesis QWidget.
    """

    def __init__(self, parent=None):
        super(ServicesView, self).__init__(parent)
        self.layout = QGridLayout()
        self.setLayout(self.layout)

    def display_services(self, services):
        """
        TODO
        """

        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().setParent(None)

        pos = 0
        for service in services:
            # Icon
            self.layout.addWidget(self.create_icon(service['ls_state']), pos, 0, 1, 1)

            # row, column, rowSpan, colSPan
            # Service name
            service_name = QLabel(service['name'].title())
            service_name.setObjectName('name')
            self.layout.addWidget(service_name, pos, 1, 1, 1)

            # Output
            output_service = QLabel(service['ls_output'])
            self.layout.addWidget(output_service, pos, 2, 1, 3)
            pos += 1
            if pos == 1:
                for inf in service:
                    print(inf, service[inf])

        self.show()

    @staticmethod
    def create_icon(state):
        """

        :param state:
        :return:
        """

        if 'OK' in state:
            icon_name = 'services_ok'
        elif 'WARNING' in state:
            icon_name = 'services_warning'
        elif 'CRITICAL' in state:
            icon_name = 'services_critical'
        elif 'UNKNOWN' in state:
            icon_name = 'services_unknown'
        else:
            icon_name = 'services_none'

        icon = QPixmap(get_image_path(icon_name))
        icon_label = QLabel()
        icon_label.setScaledContents(True)
        icon_label.setFixedSize(16, 16)
        icon_label.setPixmap(icon)

        return icon_label


# For Tests
if __name__ == '__main__':
    app = QApplication(sys.argv)

    set_app_config()

    synthesis = ServicesView()
    synthesis.display_services()

    sys.exit(app.exec_())