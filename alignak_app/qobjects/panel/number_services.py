#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015-2018:
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
    Number Services
    +++++++++++++++
    Number Services manage creation of QWidget to display number of host services, for each state
"""

from logging import getLogger

from PyQt5.Qt import QLabel, QWidget, Qt, QPixmap, QHBoxLayout

from alignak_app.items.item import get_icon_name_from_state
from alignak_app.items.service import Service
from alignak_app.utils.config import settings

logger = getLogger(__name__)


class NumberServicesQWidget(QWidget):
    """
        Class who create QWidget number of services of a host
    """

    def __init__(self, parent=None):
        super(NumberServicesQWidget, self).__init__(parent)
        # Fields
        self.services_title = QLabel()
        self.nb_labels = {
            'OK': QLabel(),
            'UNKNOWN': QLabel(),
            'WARNING': QLabel(),
            'UNREACHABLE': QLabel(),
            'CRITICAL': QLabel(),
            'NOT_MONITORED': QLabel(),
            'ACKNOWLEDGE': QLabel(),
            'DOWNTIME': QLabel()
        }

    def initialize(self):
        """
        Initialize QWidget

        """

        layout = QHBoxLayout()
        self.setLayout(layout)

        self.services_title.setObjectName('itemtitle')
        layout.addWidget(self.services_title)
        layout.setAlignment(self.services_title, Qt.AlignLeft)

        icons_widget = QWidget()
        icons_layout = QHBoxLayout()
        icons_widget.setLayout(icons_layout)

        for icon in Service.get_available_icons():
            state = icon.replace('services_', '').upper()
            icon_pixmap = QPixmap(settings.get_image(icon))
            item_icon = QLabel()
            item_icon.setPixmap(icon_pixmap)
            item_icon.setFixedSize(18, 18)
            item_icon.setScaledContents(True)
            item_icon.setToolTip(state)
            icons_layout.addWidget(item_icon)
            self.nb_labels[state].setObjectName(get_icon_name_from_state('service', state))
            icons_layout.addWidget(self.nb_labels[state])

        layout.addWidget(icons_widget)
        layout.setAlignment(icons_widget, Qt.AlignRight)

    def update_widget(self, services_items, host_name):
        """
        Update QWidget

        :param services_items: list of Service items
        :type services_items: list
        :param host_name: name of host attached to services
        :type host_name: str
        """

        services_data = Service.get_service_states_nb()

        services_total = 0
        for service in services_items:
            if not service.data['passive_checks_enabled'] and \
                    not service.data['active_checks_enabled'] and \
                    not service.data['ls_downtimed'] and \
                    not service.data['ls_acknowledged']:
                services_data['NOT_MONITORED'] += 1
            elif service.data['ls_downtimed']:
                services_data['DOWNTIME'] += 1
            elif service.data['ls_acknowledged']:
                services_data['ACKNOWLEDGE'] += 1
            else:
                services_data[service.data['ls_state']] += 1
            services_total += 1

        self.services_title.setText(
            _('<b>Services of %s: </b> %d services') % (host_name, services_total)
        )
        for state in services_data:
            percent = 0.0
            try:
                percent = float(services_data[state]) * 100.0 / float(services_total)
            except ZeroDivisionError as e:
                logger.error(e)
            item_text = '%d (%.01f%%)' % (services_data[state], percent)
            self.nb_labels[state].setText(item_text)
