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
    Service
    +++++++
    Service manage creation of QWidget to display service data
"""

from logging import getLogger

from PyQt5.Qt import QLabel, QWidget, Qt, QPushButton, QPixmap, QVBoxLayout, QGridLayout, QTimer
from PyQt5.Qt import QScrollArea

from alignak_app.backend.datamanager import data_manager
from alignak_app.items.item import get_icon_name
from alignak_app.utils.config import settings
from alignak_app.utils.time import get_time_diff_since_last_timestamp

from alignak_app.qobjects.common.actions import ActionsQWidget

logger = getLogger(__name__)


class ServiceDataQWidget(QWidget):
    """
        Class who create QWidget with service data
    """

    def __init__(self, parent=None):
        super(ServiceDataQWidget, self).__init__(parent)
        self.setMinimumSize(460, 230)
        # Fields
        self.refresh_timer = QTimer()
        self.service_item = None
        self.labels = {
            'service_icon': QLabel(),
            'service_name': QLabel(),
            'ls_last_check': QLabel(),
            'ls_output': QLabel(),
            'business_impact': QLabel(),
        }
        self.buttons = {
            'acknowledge': QPushButton(),
            'downtime': QPushButton()
        }
        self.actions_widget = ActionsQWidget()

    def initialize(self):
        """
        Initialize QWidget

        """

        layout = QGridLayout()
        self.setLayout(layout)

        layout.addWidget(self.get_service_icon_widget(), 0, 0, 1, 1)
        layout.addWidget(self.get_actions_widget(), 0, 1, 1, 1)
        layout.addWidget(self.get_last_check_widget(), 1, 0, 1, 2)

        update_service = int(settings.get_config('Alignak-app', 'update_service')) * 1000
        self.refresh_timer.setInterval(update_service)
        self.refresh_timer.start()
        self.refresh_timer.timeout.connect(self.periodic_refresh)

        self.hide()

    def get_service_icon_widget(self):
        """
        Return QWidget with its icon and name

        :return: widget with icon and name
        :rtype: QWidget
        """

        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        # Host Icon
        layout.addWidget(self.labels['service_icon'])
        layout.setAlignment(self.labels['service_icon'], Qt.AlignCenter)

        # Host Name
        self.labels['service_name'].setObjectName('itemname')
        layout.addWidget(self.labels['service_name'])
        layout.setAlignment(self.labels['service_name'], Qt.AlignCenter)

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
        check_title = QLabel(_('My last check'))
        check_title.setObjectName('itemtitle')
        check_title.setFixedHeight(30)
        layout.addWidget(check_title, 0, 0, 1, 2)

        # When last check
        when_title = QLabel(_("When:"))
        when_title.setObjectName('title')
        layout.addWidget(when_title, 2, 0, 1, 1)

        layout.addWidget(self.labels['ls_last_check'], 2, 1, 1, 1)

        # Output
        output_title = QLabel(_("Output"))
        output_title.setObjectName('title')
        layout.addWidget(output_title, 3, 0, 1, 1)

        self.labels['ls_output'].setWordWrap(True)
        self.labels['ls_output'].setTextInteractionFlags(Qt.TextSelectableByMouse)
        output_scrollarea = QScrollArea()
        output_scrollarea.setWidget(self.labels['ls_output'])
        output_scrollarea.setWidgetResizable(True)
        output_scrollarea.setObjectName('output')
        layout.addWidget(output_scrollarea, 3, 1, 1, 1)

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

        self.actions_widget.initialize(self.service_item)
        layout.addWidget(self.actions_widget)

        layout.setAlignment(Qt.AlignCenter)

        return widget

    def update_widget(self, service=None):
        """
        Update ServiceDataQWidget

        :param service: Service item with its data
        :type service: alignak_app.core.models.service.Service
        """

        if service:
            self.service_item = service

        icon_name = get_icon_name(
            'service',
            self.service_item.data['ls_state'],
            self.service_item.data['ls_acknowledged'],
            self.service_item.data['ls_downtimed'],
            self.service_item.data['passive_checks_enabled'] +
            self.service_item.data['active_checks_enabled']
        )
        icon_pixmap = QPixmap(settings.get_image(icon_name))
        icon_pixmap.setDevicePixelRatio(1.0)

        self.labels['service_icon'].setPixmap(QPixmap(icon_pixmap))
        self.labels['service_icon'].setScaledContents(True)
        self.labels['service_icon'].setFixedSize(48, 48)
        self.labels['service_icon'].setToolTip(self.service_item.get_tooltip())
        self.labels['service_name'].setText(self.service_item.get_display_name())

        since_last_check = get_time_diff_since_last_timestamp(
            self.service_item.data['ls_last_check']
        )
        self.labels['ls_last_check'].setText(since_last_check)
        self.labels['ls_output'].setText(self.service_item.data['ls_output'])

        self.labels['business_impact'].setText(str(self.service_item.data['business_impact']))

        self.actions_widget.item = self.service_item
        self.actions_widget.update_widget()

    def periodic_refresh(self):
        """
        Refresh QWidget periodically

        """

        if self.service_item:
            updated_service = data_manager.get_item('service', '_id', self.service_item.item_id)
            if updated_service:
                self.service_item = updated_service
            self.update_widget()
