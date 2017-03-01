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

from alignak_app.core.utils import get_diff_since_last_check, get_css
from alignak_app.core.utils import get_image_path, get_app_config

try:
    __import__('PyQt5')
    from PyQt5.QtWidgets import QScrollArea, QHBoxLayout  # pylint: disable=no-name-in-module
    from PyQt5.QtWidgets import QWidget, QPushButton, QFrame  # pylint: disable=no-name-in-module
    from PyQt5.Qt import QIcon, QPixmap, Qt  # pylint: disable=no-name-in-module
    from PyQt5.QtWidgets import QGridLayout, QLabel   # pylint: disable=no-name-in-module
except ImportError:  # pragma: no cover
    from PyQt4.Qt import QScrollArea, QHBoxLayout  # pylint: disable=import-error
    from PyQt4.Qt import QWidget, QPushButton, QFrame  # pylint: disable=import-error
    from PyQt4.Qt import QIcon, QPixmap, Qt  # pylint: disable=import-error
    from PyQt4.Qt import QGridLayout, QLabel  # pylint: disable=import-error


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
        output_service = QLabel('<b>Output:</b> %s' % service['ls_output'])
        output_service.setObjectName('output')
        output_service.setToolTip(service['ls_output'])
        output_service.setTextInteractionFlags(Qt.TextSelectableByMouse)
        output_service.setCursor(Qt.IBeamCursor)

        scroll = QScrollArea()
        scroll.setWidget(output_service)
        scroll.setObjectName('output')
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setMaximumHeight(60)
        layout.addWidget(scroll, 1, 3, 2, 2)

        self.add_services_details(service, layout)

    def add_services_details(self, service, layout):
        """
        Add the service details

        :param service: service dict data from AppBackend
        :type service: dict
        :param layout: layout of Service
        :type layout: QGridLayout
        """

        # Service details
        business_impact = self.get_stars_widget(int(service['business_impact']))
        layout.addWidget(business_impact, 3, 0, 2, 2)
        layout.setAlignment(business_impact, Qt.AlignLeft)

        if '_DETAILLEDESC' in service['customs']:
            description = service['customs']['_DETAILLEDESC']
        else:
            description = ''
        if '_IMPACT' in service['customs']:
            impact = service['customs']['_IMPACT']
        else:
            impact = ''
        if '_FIXACTIONS' in service['customs']:
            fix_actions = service['customs']['_FIXACTIONS']
        else:
            fix_actions = ''

        desc_label = QLabel('<b>Description:</b> %s' % description)
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label, 3, 2, 2, 3)

        impact_label = QLabel('<b>Impact:</b> %s' % impact)
        impact_label.setWordWrap(True)
        layout.addWidget(impact_label, 5, 0, 2, 2)

        fixactions_label = QLabel('<b>Fix actions:</b> %s' % fix_actions)
        fixactions_label.setWordWrap(True)
        layout.addWidget(fixactions_label, 5, 2, 2, 3)

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

        for _ in range(1, stars_nb):
            star_label = QLabel()
            star_label.setFixedSize(16, 16)
            star_label.setScaledContents(True)
            star_label.setPixmap(QPixmap(get_image_path('star')))
            layout.addWidget(star_label)

        return stars_widget
