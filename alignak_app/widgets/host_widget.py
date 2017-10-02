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
    TODO
"""

from alignak_app.core.utils import get_image_path

from PyQt5.Qt import QLabel, QWidget, QGridLayout  # pylint: disable=no-name-in-module
from PyQt5.Qt import QPixmap, QVBoxLayout, QHBoxLayout, Qt  # pylint: disable=no-name-in-module


host_data = {
    'name': 'chazay',
    'alias': "Chazay",
    'ls_state': 'UP',
    '_id': '00011122223333',
    'ls_acknowledged': False,
    'ls_downtimed': False,
    'ls_last_check': '5 days 3h10m45s',
    'ls_output': 'NRPE v2.15',
    'address': '127.0.0.1',
    'business_impact': 2,
    '_realm': 'All',
    'ls_last_state_changed': '2h15m21s',
    'notes': 'Aucune note'
}


class HostQWidget(QWidget):
    """
        TODO
    """

    def initialize(self):
        """
        TODO
        :return:
        """

        layout = QHBoxLayout()
        self.setLayout(layout)

        layout.addWidget(
            self.get_host_icon_widget('all_services_critical', host_data['name'])
        )

        layout.addWidget(self.get_host_resume_widget())

    def get_host_resume_widget(self):
        """
        TODO
        :return:
        """

        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        layout.addWidget(self.get_last_check_widget())

        return widget

    def get_last_check_widget(self):
        """
        TODO
        :return:
        """

        widget = QWidget()
        layout = QGridLayout()
        widget.setLayout(layout)

        check_title = QLabel('My last check')
        check_title.setStyleSheet('background-color: #607d8b; color: white;')
        layout.addWidget(check_title, 0, 0, 1, 2)

        state_title = QLabel("<b>State:</b>")
        layout.addWidget(state_title, 1, 0, 1, 1)

        state_icon = QLabel()
        state_icon.setPixmap(QPixmap(get_image_path('hosts_%s' % host_data['ls_state'].lower())))
        layout.addWidget(state_icon, 1, 1, 1, 1)

        when_title = QLabel("<b>When</b>")
        layout.addWidget(when_title, 2, 0, 1, 1)

        when_data = QLabel(host_data['ls_last_state_changed'])
        layout.addWidget(when_data, 2, 1, 1, 1)

        return widget

    def get_host_icon_widget(self, state, name):
        """
        TODO
        :param state:
        :param name:
        :return:
        """

        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        icon_label = QLabel()
        icon_label.setPixmap(QPixmap(get_image_path(state)))
        layout.addWidget(icon_label)

        name_label = QLabel('<span style="font-size: 14px;">%s</span>' % name)
        layout.addWidget(name_label)

        return widget
