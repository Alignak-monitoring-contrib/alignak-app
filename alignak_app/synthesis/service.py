#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015-2017:
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

from alignak_app.core.utils import get_diff_since_last_check, get_css, get_date_from_timestamp
from alignak_app.core.utils import get_image_path, get_app_config

from PyQt5.QtWidgets import QHBoxLayout  # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QWidget, QPushButton, QFrame  # pylint: disable=no-name-in-module
from PyQt5.Qt import QIcon, QPixmap, Qt, QTextEdit  # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QGridLayout, QLabel  # pylint: disable=no-name-in-module
from PyQt5.QtGui import QFont  # pylint: disable=no-name-in-module


logger = getLogger(__name__)


class Service(QFrame):
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
        self.setObjectName('service_widget')
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

        if service['display_name'] != '':
            service_name = service['display_name']
        elif service['alias'] != '':
            service_name = service['alias']
        else:
            service_name = service['name']

        # Service name
        service_label = QLabel()
        if get_app_config('Alignak', 'webui'):
            service_label.setText(
                '<h3><a href="%s" style="color: black; text-decoration: none">%s</a></h3>' % (
                    get_app_config('Alignak', 'webui') + '/service/' + service['_id'],
                    service_name
                )
            )
        else:
            service_label.setText('<h3>%s</h3>' % service_name)
        service_label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        service_label.setOpenExternalLinks(True)
        service_label.setToolTip('Service is %s. See in WebUI ?' % service['ls_state'])
        service_label.setObjectName(service['ls_state'])
        service_label.setMinimumWidth(200)
        service_label.setWordWrap(True)
        layout.addWidget(service_label, 0, 1, 2, 1)
        layout.setAlignment(service_label, Qt.AlignLeft)

        # Buttons
        self.acknowledge_btn = QPushButton()
        self.acknowledge_btn.setIcon(QIcon(get_image_path('services_acknowledge')))
        self.acknowledge_btn.setFixedSize(25, 25)
        self.acknowledge_btn.setToolTip('Acknowledge this service')
        layout.addWidget(self.acknowledge_btn, 0, 2, 1, 1)

        self.downtime_btn = QPushButton()
        self.downtime_btn.setIcon(QIcon(get_image_path('services_downtime')))
        self.downtime_btn.setFixedSize(25, 25)
        self.downtime_btn.setToolTip('Schedule a downtime for this service')
        layout.addWidget(self.downtime_btn, 1, 2, 1, 1)

        # Last check
        since_last_check = get_diff_since_last_check(service['ls_last_state_changed'])
        diff_last_check = get_diff_since_last_check(service['ls_last_check'])

        last_check = QLabel(
            '<b>Since:</b> %s, <b>Last check:</b> %s' % (since_last_check, diff_last_check)
        )
        layout.addWidget(last_check, 0, 3, 1, 2)

        # Output
        date_output = get_date_from_timestamp(service['ls_last_check'])
        output = QTextEdit('<b>Output:</b> [%s] %s' % (date_output, service['ls_output']))
        output.setObjectName('output')
        output.setToolTip(service['ls_output'])
        output.setTextInteractionFlags(Qt.TextSelectableByMouse)
        output.setFont(QFont('Times', 13))
        layout.addWidget(output, 1, 3, 2, 4)

        # Service details
        business_impact = self.get_stars_widget(int(service['business_impact']))
        layout.addWidget(business_impact, 2, 0, 1, 2)
        layout.setAlignment(business_impact, Qt.AlignLeft)

        self.add_services_details(service, layout)

    @staticmethod
    def add_services_details(service, layout):
        """
        Add the service customs actions only if needed

        :param service: service dict data from AppBackend
        :type service: dict
        :param layout: layout of Service
        :type layout: QGridLayout
        """

        detailledesc = False
        impact = False
        fixactions = False

        row = 3
        if '_DETAILLEDESC' in service['customs']:
            desc_label = QLabel('<b>Description:</b> %s' % service['customs']['_DETAILLEDESC'])
            desc_label.setWordWrap(True)
            layout.addWidget(desc_label, row, 0, 1, 4)
            detailledesc = True
            row += 1

        if '_IMPACT' in service['customs']:
            impact_label = QLabel('<b>Impact:</b> %s' % service['customs']['_IMPACT'])
            impact_label.setWordWrap(True)
            layout.addWidget(impact_label, row, 0, 1, 4)
            impact = True
            row += 1

        if '_FIXACTIONS' in service['customs']:
            fixactions_label = QLabel('<b>Fix actions:</b> %s' % service['customs']['_FIXACTIONS'])
            fixactions_label.setWordWrap(True)
            layout.addWidget(fixactions_label, row, 0, 1, 4)
            fixactions = True
            row += 1

        if not detailledesc and not impact and not fixactions:
            layout.addWidget(
                QLabel('<i>No customs actions defined for this service</i>'),
                row, 2, 1, 4
            )

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
        icon_label.setToolTip('Service is ' + state)

        return icon_label

    @staticmethod
    def get_stars_widget(stars_nb):
        """
        Return QWidget with stars icons

        :param stars_nb: number of stars to display
        :type stars_nb: int
        :return: QWidget with stars
        :rtype: QWidget
        """

        stars_widget = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        stars_widget.setLayout(layout)

        importance_label = QLabel('<b>Importance:</b>')
        layout.addWidget(importance_label)
        layout.setAlignment(importance_label, Qt.AlignLeft)

        for _ in range(int(get_app_config('Alignak', 'bi_less')), stars_nb):
            star_label = QLabel()
            star_label.setFixedSize(16, 16)
            star_label.setScaledContents(True)
            star_label.setPixmap(QPixmap(get_image_path('star')))
            layout.addWidget(star_label)

        return stars_widget
