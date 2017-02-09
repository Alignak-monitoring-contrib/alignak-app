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
    Service manage QWidgets for services.
"""

from logging import getLogger

from alignak_app.core.utils import get_image_path, get_diff_since_last_check, get_css

try:
    __import__('PyQt5')
    from PyQt5.QtWidgets import QScrollArea  # pylint: disable=no-name-in-module
    from PyQt5.QtWidgets import QWidget, QPushButton  # pylint: disable=no-name-in-module
    from PyQt5.Qt import QIcon, QPixmap  # pylint: disable=no-name-in-module
    from PyQt5.QtCore import Qt  # pylint: disable=no-name-in-module
    from PyQt5.Qt import QObject, pyqtSignal  # pylint: disable=no-name-in-module
    from PyQt5.QtWidgets import QGridLayout, QLabel   # pylint: disable=no-name-in-module
except ImportError:  # pragma: no cover
    from PyQt4.Qt import QScrollArea  # pylint: disable=import-error
    from PyQt4.Qt import QWidget, QPushButton, Qt, QIcon  # pylint: disable=import-error
    from PyQt4.QtCore import QObject, pyqtSignal  # pylint: disable=import-error
    from PyQt4.Qt import QGridLayout, QLabel, QPixmap  # pylint: disable=import-error


logger = getLogger(__name__)


class Service(QWidget):
    """
        Class who create the Service QWidget for SynthesisView.
    """

    state_model = {
        'OK': 'services_ok',
        'WARNING': 'services_warning',
        'CRITICAL': 'services_critical',
        'UNKNOWN': 'services_unknown',
        'UNREACHABLE': 'services_unreachable',
        'DEFAULT': 'services_none'
    }

    def __init__(self, parent=None):
        super(Service, self).__init__(parent)
        self.setStyleSheet(get_css())
        # Fields
        self.acknowledge_btn = None
        self.downtime_btn = None

    def initialize(self, service):
        """
        Inititialize Service QWidget

        :param service: service data
        :type service: dict
        """

        layout = QGridLayout()
        self.setLayout(layout)

        layout.addWidget(self.get_service_icon(service['ls_state']), 0, 0, 2, 1)

        # Service name
        service_name = QLabel(service['display_name'])
        service_name.setToolTip('Service is ' + service['ls_state'])
        service_name.setObjectName(service['ls_state'])
        service_name.setMinimumWidth(200)
        service_name.setWordWrap(True)
        layout.addWidget(service_name, 0, 1, 2, 1)
        layout.setAlignment(service_name, Qt.AlignLeft)

        # Buttons
        self.acknowledge_btn = QPushButton()
        self.acknowledge_btn.setIcon(QIcon(get_image_path('acknowledged')))
        self.acknowledge_btn.setFixedSize(25, 25)
        self.acknowledge_btn.setToolTip('Acknowledge this service')
        layout.addWidget(self.acknowledge_btn, 0, 2, 1, 1)

        self.downtime_btn = QPushButton()
        self.downtime_btn.setIcon(QIcon(get_image_path('downtime')))
        self.downtime_btn.setFixedSize(25, 25)
        self.downtime_btn.setToolTip('Schedule a downtime for this service')
        layout.addWidget(self.downtime_btn, 1, 2, 1, 1)

        # Last check
        check_name = QLabel('<b>Last check:</b>')
        layout.addWidget(check_name, 0, 3, 1, 1)
        diff_last_check = get_diff_since_last_check(service['ls_last_check'])

        last_check = QLabel(str(diff_last_check))
        layout.addWidget(last_check, 0, 4, 1, 1)

        # Output
        output_name = QLabel('<b>Output:</b>')
        output_name.setToolTip('Output of %s' % service['display_name'])
        layout.addWidget(output_name, 1, 3, 1, 1)
        output_service = QLabel(service['ls_output'])
        output_service.setObjectName('output')
        output_service.setToolTip(service['ls_output'])
        output_service.setTextInteractionFlags(Qt.TextSelectableByMouse)

        scroll = QScrollArea()
        scroll.setWidget(output_service)
        scroll.setObjectName('output')
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setMaximumHeight(60)
        layout.addWidget(scroll, 1, 4, 2, 1)

    def get_service_icon(self, state):
        """
        Return QPixmap with the icon corresponding to the status.

        :param state: state of the host.
        :type state: str
        :return: QPushButton with QIcon
        :rtype: QPushButton
        """

        try:
            icon_name = self.state_model[state]
        except KeyError:
            state = 'ERROR'
            icon_name = self.state_model['DEFAULT']
        icon = QPixmap(get_image_path(icon_name))

        icon_label = QLabel()
        icon_label.setMaximumSize(32, 32)
        icon_label.setScaledContents(True)
        icon_label.setPixmap(icon)
        icon_label.setObjectName('service')
        icon_label.setToolTip('Service is ' + state)

        return icon_label
