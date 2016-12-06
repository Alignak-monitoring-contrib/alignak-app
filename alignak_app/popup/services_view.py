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
    from PyQt5.QtWidgets import QScrollArea  # pylint: disable=no-name-in-module
    from PyQt5.QtWidgets import QWidget, QVBoxLayout  # pylint: disable=no-name-in-module
    from PyQt5.QtWidgets import QGridLayout, QLabel  # pylint: disable=no-name-in-module
    from PyQt5.Qt import QPixmap  # pylint: disable=no-name-in-module
except ImportError:  # pragma: no cover
    from PyQt4.Qt import QScrollArea  # pylint: disable=import-error
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
        self.layout = QVBoxLayout()
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
            self.layout.itemAt(i).widget().setParent(None)

        widget = QWidget()
        layout = QGridLayout()

        pos = 0

        if not services:
            logger.warning('Services not Found ! ')

            # Icon
            layout.addWidget(self.get_service_icon(''), pos, 0)

            # row, column, rowSpan, colSPan
            # Service name
            service_name = QLabel('NOT FOUND')
            service_name.setObjectName('name')
            service_name.setMinimumHeight(30)
            layout.addWidget(service_name, pos, 1)

            # Output
            output_service = QLabel('NOT FOUND')
            layout.addWidget(output_service, pos, 2)
        else:
            for service in services:
                # Icon
                layout.addWidget(self.get_service_icon(service['ls_state']), pos, 0)

                # row, column, rowSpan, colSPan
                # Service name
                service_name = QLabel(service['name'].title())
                service_name.setObjectName('name')
                service_name.setMinimumHeight(30)
                layout.addWidget(service_name, pos, 1)

                # Output
                output_service = QLabel(service['ls_output'])
                layout.addWidget(output_service, pos, 2)
                pos += 1

        logger.debug('Number of services: ' + str(pos))

        widget.setLayout(layout)
        scroll = QScrollArea()
        scroll.setWidget(widget)
        scroll.setWidgetResizable(True)

        self.layout.addWidget(scroll)
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

        icon = QPixmap(get_image_path(icon_name))
        icon_label = QLabel()
        icon_label.setScaledContents(True)
        icon_label.setFixedSize(16, 16)
        icon_label.setPixmap(icon)

        return icon_label
