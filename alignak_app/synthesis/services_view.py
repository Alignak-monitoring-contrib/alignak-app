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
from alignak_app.synthesis.service import Service

try:
    __import__('PyQt5')
    from PyQt5.QtWidgets import QScrollArea  # pylint: disable=no-name-in-module
    from PyQt5.QtWidgets import QWidget, QVBoxLayout  # pylint: disable=no-name-in-module
    from PyQt5.QtWidgets import QGridLayout, QLabel  # pylint: disable=no-name-in-module
    from PyQt5.Qt import QPixmap, Qt  # pylint: disable=no-name-in-module
except ImportError:  # pragma: no cover
    from PyQt4.Qt import QScrollArea  # pylint: disable=import-error
    from PyQt4.Qt import QWidget, QVBoxLayout  # pylint: disable=import-error
    from PyQt4.Qt import QGridLayout, QLabel  # pylint: disable=import-error
    from PyQt4.Qt import QPixmap, Qt  # pylint: disable=import-error


logger = getLogger(__name__)


class ServicesView(QWidget):
    """
        Class who create the Synthesis QWidget.
    """

    def __init__(self, parent=None):
        super(ServicesView, self).__init__(parent)
        self.setToolTip('Services View')
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

    def display_services(self, services, name):  # pylint: disable=too-many-locals
        """
        Display services.

        :param services: services of a specific host from app_backend
        :type services: dict
        :param name: name of host
        :type name: str
        """

        logger.info('Create Services View')

        # Clean all items before
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().setParent(None)

        service_title = QLabel('<b>Services of ' + name + '</b>')
        self.layout.addWidget(service_title, 0)
        self.layout.setAlignment(Qt.AlignCenter)

        widget = QWidget()
        layout = QGridLayout()
        widget.setLayout(layout)

        pos = 0

        if not services:
            logger.warning('Services not Found ! ')

            output_service = QLabel('No services available...')
            layout.addWidget(output_service, 0, 0)
        else:
            for service in services:
                service_widget = Service()
                service_widget.initialize(service)
                layout.addWidget(service_widget, pos, 0)
                pos += 1

        logger.debug('Number of services: ' + str(pos))

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
        elif 'UNREACHABLE' in state:
            icon_name = 'services_unreachable'
        else:
            icon_name = 'services_none'

        icon = QPixmap(get_image_path(icon_name))
        icon_label = QLabel()
        icon_label.setFixedSize(16, 16)
        icon_label.setScaledContents(True)
        icon_label.setPixmap(icon)
        icon_label.setToolTip('Service is ' + state)

        return icon_label
