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

from logging import getLogger

from alignak_app.core.utils import get_image_path

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
        Display services.

        :param services: services of a specific host from backend
        :type services: dict
        """

        logger.info('Create Services View')

        # Clean all items before
        for i in reversed(range(self.layout.count())):
            logger.debug('Clean: ' + str(self.layout.itemAt(i)))
            self.layout.itemAt(i).widget().setParent(None)

        pos = 0
        for service in services:
            # Icon
            logger.debug('Add item at pos: ' + str(pos))
            self.layout.addWidget(self.get_service_icon(service['ls_state']), pos, 0, 1, 1)

            # row, column, rowSpan, colSPan
            # Service name
            service_name = QLabel(service['name'].title())
            service_name.setObjectName('name')
            service_name.setMinimumHeight(30)
            self.layout.addWidget(service_name, pos, 1, 1, 1)

            # Output
            output_service = QLabel(service['ls_output'])
            self.layout.addWidget(output_service, pos, 2, 1, 3)
            pos += 1

        self.show()

    @staticmethod
    def get_service_icon(state):
        """
        Return QPixmap with the icon corresponding to the status.

        :param state: state of the host.
        :type state: str
        :return: QPixmap with image
        :rtype: QPixmap
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

        logger.debug('Service Icon: ' + icon_name)

        icon = QPixmap(get_image_path(icon_name))
        icon_label = QLabel()
        icon_label.setScaledContents(True)
        icon_label.setFixedSize(16, 16)
        icon_label.setPixmap(icon)

        return icon_label
