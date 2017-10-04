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

import sys

from alignak_app.core.utils import get_image_path, init_config, get_css
from alignak_app.core.utils import get_time_diff_since_last_timestamp
from alignak_app.core.data_manager import data_manager
from alignak_app.core.backend import app_backend
from alignak_app.threads.thread_manager import thread_manager
from alignak_app.models.item_model import get_icon_item, get_real_host_state_icon

from PyQt5.Qt import QLabel, QWidget, QGridLayout  # pylint: disable=no-name-in-module
from PyQt5.Qt import QPixmap, QVBoxLayout, QHBoxLayout  # pylint: disable=no-name-in-module
from PyQt5.Qt import QApplication  # pylint: disable=no-name-in-module


class HostQWidget(QWidget):
    """
        TODO
    """

    def __init__(self, host_and_services, parent=None):
        super(HostQWidget, self).__init__(parent)
        self.setStyleSheet(get_css())
        # Fields
        self.host_item = host_and_services['host']
        self.service_items = host_and_services['services']
        self.labels = {
            'host_icon': QLabel(),
            'host_name': QLabel(),
            'state_icon': QLabel(),
            'ls_last_check': QLabel(),
            'ls_output': QLabel(),
            'realm': QLabel(),
            'address': QLabel(),
            'business_impact': QLabel()
        }

    def initialize(self):
        """
        Initialize QWidget

        """

        layout = QHBoxLayout()
        self.setLayout(layout)

        layout.addWidget(self.get_host_icon_widget())

        layout.addWidget(self.get_last_check_widget())

        layout.addWidget(self.get_variables_widget())

    def get_host_icon_widget(self):
        """
        Return QWidget with overall icon state and host name

        :return: widget with host name and icon
        :rtype: QWidget
        """

        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        icon_name = get_real_host_state_icon(self.service_items)

        self.labels['host_icon'].setPixmap(QPixmap(
            get_image_path(icon_name)
        ))
        layout.addWidget(self.labels['host_icon'])

        self.labels['host_name'].setText('%s' % self.host_item.name)
        layout.addWidget(self.labels['host_name'])

        return widget

    def get_last_check_widget(self):
        """
        Return QWidget with last check data

        :return: widget with last check data
        :rtype: QWidget
        """

        widget = QWidget()
        layout = QGridLayout()
        widget.setLayout(layout)

        # Title
        check_title = QLabel('My last check')
        check_title.setStyleSheet('background-color: #607d8b; color: white;')
        layout.addWidget(check_title, 0, 0, 1, 2)

        # State
        state_title = QLabel("<b>State:</b>")
        layout.addWidget(state_title, 1, 0, 1, 1)

        icon_name = get_icon_item(
            'host',
            self.host_item.data['ls_state'],
            self.host_item.data['ls_acknowledged'],
            self.host_item.data['ls_downtimed']
        )
        self.labels['state_icon'].setPixmap(QPixmap(get_image_path(icon_name)))
        layout.addWidget(self.labels['state_icon'], 1, 1, 1, 1)

        # When last check
        when_title = QLabel("<b>When</b>")
        layout.addWidget(when_title, 2, 0, 1, 1)

        since_last_check = get_time_diff_since_last_timestamp(
            self.host_item.data['ls_last_check']
        )
        self.labels['ls_last_check'].setText(since_last_check)
        layout.addWidget(self.labels['ls_last_check'], 2, 1, 1, 1)

        # Output
        output_title = QLabel("Output")
        layout.addWidget(output_title, 3, 0, 1, 1)

        self.labels['ls_output'].setText(self.host_item.data['ls_output'])
        layout.addWidget(self.labels['ls_output'], 3, 1, 1, 1)

        return widget

    def get_variables_widget(self):
        """
        TODO
        :return:
        """

        widget = QWidget()
        layout = QGridLayout()
        widget.setLayout(layout)

        # Title
        check_title = QLabel('My variables')
        check_title.setStyleSheet('background-color: #607d8b; color: white;')
        layout.addWidget(check_title, 0, 0, 1, 2)

        # Realm
        realm_title = QLabel("<b>Realm:</b>")
        layout.addWidget(realm_title, 1, 0, 1, 1)

        self.labels['realm'].setText(self.host_item.data['_realm'])
        layout.addWidget(self.labels['realm'], 1, 1, 1, 1)

        # Address
        address_title = QLabel("<b>Host address:</b>")
        layout.addWidget(address_title, 2, 0, 1, 1)

        self.labels['address'].setText(self.host_item.data['address'])
        layout.addWidget(self.labels['address'], 2, 1, 1, 1)

        # Business impact
        address_title = QLabel("<b>Business impact:</b>")
        layout.addWidget(address_title, 3, 0, 1, 1)

        self.labels['business_impact'].setText(str(self.host_item.data['business_impact']))
        layout.addWidget(self.labels['business_impact'], 3, 1, 1, 1)

        return widget


if __name__ == '__main__':
    app = QApplication(sys.argv)

    init_config()
    app_backend.login()
    thread_manager.start()

    while not data_manager.is_ready():
        continue

    host_services = data_manager.get_host_with_services('denice')

    host = HostQWidget(host_services)

    host.initialize()
    host.show()

    sys.exit(app.exec_())
