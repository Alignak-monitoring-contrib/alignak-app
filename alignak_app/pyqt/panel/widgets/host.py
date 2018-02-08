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
    Host QWidget manage display of host data
"""

from logging import getLogger

from PyQt5.Qt import QLabel, QWidget, QGridLayout, Qt, QPixmap, QVBoxLayout, QHBoxLayout
from PyQt5.Qt import QPushButton, QIcon, QTimer

from alignak_app.core.backend.client import app_backend
from alignak_app.core.backend.data_manager import data_manager
from alignak_app.core.models.item import get_host_msg_and_event_type
from alignak_app.core.models.item import get_icon_name, get_real_host_state_icon
from alignak_app.core.utils.config import get_image, app_css, get_app_config
from alignak_app.core.utils.time import get_time_diff_since_last_timestamp

from alignak_app.pyqt.common.actions import ActionsQWidget
from alignak_app.pyqt.panel.widgets.history import HistoryQWidget

logger = getLogger(__name__)


class HostQWidget(QWidget):
    """
        Class who create QWidget to display host data
    """

    def __init__(self, parent=None):
        super(HostQWidget, self).__init__(parent)
        self.actions_widget = ActionsQWidget()
        self.setStyleSheet(app_css)
        # Fields
        self.host_item = None
        self.service_items = None
        self.labels = {
            'host_icon': QLabel(),
            'host_name': QLabel(),
            'state_icon': QLabel(),
            'ls_last_check': QLabel(),
            'ls_output': QLabel(),
            'realm': QLabel(),
            'address': QLabel(),
            'business_impact': QLabel(),
            'notes': QLabel()
        }
        self.history_btn = QPushButton()
        self.history_widget = None
        self.refresh_timer = QTimer()

    def initialize(self):
        """
        Initialize QWidget

        """

        layout = QHBoxLayout()
        self.setLayout(layout)

        # Add Qwidgets
        layout.addWidget(self.get_host_icon_widget())

        layout.addWidget(self.get_actions_widget())

        layout.addWidget(self.get_last_check_widget())

        layout.addWidget(self.get_variables_widget())

        update_host = int(get_app_config('Alignak-app', 'update_host')) * 1000
        self.refresh_timer.setInterval(update_host)
        self.refresh_timer.start()
        self.refresh_timer.timeout.connect(self.update_host)

    def set_data(self, hostname):
        """
        Set data of host and service

        :param hostname: name of host to display
        :type hostname: str
        """

        host_and_services = data_manager.get_host_with_services(hostname)

        self.host_item = host_and_services['host']
        self.service_items = host_and_services['services']

    def get_host_icon_widget(self):
        """
        Return QWidget with overall icon state and host name

        :return: widget with host name and icon
        :rtype: QWidget
        """

        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        # Host Icon
        layout.addWidget(self.labels['host_icon'])
        layout.setAlignment(self.labels['host_icon'], Qt.AlignCenter)

        # Host Name
        self.labels['host_name'].setObjectName('itemname')
        layout.addWidget(self.labels['host_name'])
        layout.setAlignment(self.labels['host_name'], Qt.AlignCenter)

        return widget

    def get_actions_widget(self):
        """
        Return QWidget with actions buttons

        :return: widget with buttons
        :rtype: QWidget
        """

        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        action_title = QLabel(_('Actions:'))
        action_title.setObjectName('title')
        layout.addWidget(action_title)

        self.actions_widget.initialize(self.host_item)
        layout.addWidget(self.actions_widget)

        self.history_btn.setIcon(QIcon(get_image('time')))
        self.history_btn.clicked.connect(self.show_history)
        layout.addWidget(self.history_btn)

        layout.setAlignment(Qt.AlignCenter)

        return widget

    def show_history(self):
        """
        Create and show HistoryQWidget

        """

        self.history_widget = HistoryQWidget(self)
        self.history_widget.initialize(self.host_item.name, self.host_item.item_id)
        self.history_widget.app_widget.show()

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
        check_title = QLabel(_('My last check'))
        check_title.setObjectName('itemtitle')
        check_title.setFixedHeight(30)
        layout.addWidget(check_title, 0, 0, 1, 2)

        # State
        state_title = QLabel(_("State:"))
        state_title.setObjectName('title')
        layout.addWidget(state_title, 1, 0, 1, 1)

        layout.addWidget(self.labels['state_icon'], 1, 1, 1, 1)

        # When last check
        when_title = QLabel(_("When:"))
        when_title.setObjectName('title')
        layout.addWidget(when_title, 2, 0, 1, 1)

        layout.addWidget(self.labels['ls_last_check'], 2, 1, 1, 1)

        # Output
        output_title = QLabel(_("Output"))
        output_title.setObjectName('title')
        layout.addWidget(output_title, 3, 0, 1, 1)

        self.labels['ls_output'].setObjectName('output')
        self.labels['ls_output'].setWordWrap(True)
        self.labels['ls_output'].setTextInteractionFlags(Qt.TextSelectableByMouse)
        layout.addWidget(self.labels['ls_output'], 3, 1, 1, 1)

        return widget

    def get_variables_widget(self):
        """
        Return QWidget with host variables

        :return: widget with host variables
        :rtype: QWidget
        """

        widget = QWidget()
        layout = QGridLayout()
        widget.setLayout(layout)

        # Title
        check_title = QLabel(_('My variables'))
        check_title.setObjectName('itemtitle')
        check_title.setFixedHeight(30)
        layout.addWidget(check_title, 0, 0, 1, 2)

        # Realm
        realm_title = QLabel(_("Realm:"))
        realm_title.setObjectName('title')
        layout.addWidget(realm_title, 1, 0, 1, 1)

        layout.addWidget(self.labels['realm'], 1, 1, 1, 1)

        # Address
        address_title = QLabel(_("Host address:"))
        address_title.setObjectName('title')
        layout.addWidget(address_title, 2, 0, 1, 1)

        layout.addWidget(self.labels['address'], 2, 1, 1, 1)

        # Business impact
        address_title = QLabel(_("Business impact:"))
        address_title.setObjectName('title')
        layout.addWidget(address_title, 3, 0, 1, 1)

        layout.addWidget(self.labels['business_impact'], 3, 1, 1, 1)

        # Notes
        notes_title = QLabel(_("Notes:"))
        notes_title.setObjectName('title')
        layout.addWidget(notes_title, 4, 0, 1, 1)

        self.labels['notes'].setWordWrap(True)
        layout.addWidget(self.labels['notes'], 4, 1, 1, 1)

        return widget

    def update_host(self, hostname=None):
        """
        Update HostQWidget data and QLabels

        :param hostname: name of host who is display
        :type hostname: str
        """

        logger.info('Update Host QWidget...')

        if self.host_item and not hostname:
            self.set_data(self.host_item.name)
        if hostname:
            self.set_data(hostname)

        if self.host_item or hostname:
            icon_name = get_real_host_state_icon(self.service_items)
            icon_pixmap = QPixmap(get_image(icon_name))

            self.labels['host_icon'].setPixmap(QPixmap(icon_pixmap))
            self.labels['host_icon'].setToolTip(
                get_host_msg_and_event_type(
                    {'host': self.host_item, 'services': self.service_items}
                )['message']
            )
            self.labels['host_name'].setText('%s' % self.host_item.get_display_name())

            icon_name = get_icon_name(
                'host',
                self.host_item.data['ls_state'],
                self.host_item.data['ls_acknowledged'],
                self.host_item.data['ls_downtimed'],
                self.host_item.data['passive_checks_enabled'] +
                self.host_item.data['active_checks_enabled']
            )
            pixmap_icon = QPixmap(get_image(icon_name))
            final_icon = pixmap_icon.scaled(32, 32, Qt.KeepAspectRatio)
            self.labels['state_icon'].setPixmap(final_icon)
            self.labels['state_icon'].setToolTip(self.host_item.get_tooltip())

            since_last_check = get_time_diff_since_last_timestamp(
                self.host_item.data['ls_last_check']
            )
            self.labels['ls_last_check'].setText(since_last_check)
            self.labels['ls_output'].setText(self.host_item.data['ls_output'])

            self.labels['realm'].setText(
                app_backend.get_realm_name(self.host_item.data['_realm'])
            )
            self.labels['address'].setText(self.host_item.data['address'])
            self.labels['business_impact'].setText(str(self.host_item.data['business_impact']))
            self.labels['notes'].setText(self.host_item.data['notes'])

            self.actions_widget.item = self.host_item
            self.actions_widget.update_widget()

            if any(
                    history_item.item_id == self.host_item.item_id for
                    history_item in data_manager.database['history']):
                self.history_btn.setEnabled(True)
                self.history_btn.setToolTip(_('History is available'))
            else:
                self.history_btn.setToolTip(_('History is not available, please wait...'))
                self.history_btn.setEnabled(False)
