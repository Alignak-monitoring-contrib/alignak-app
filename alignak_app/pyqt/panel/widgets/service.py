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
    Service QWidget manage display of service data
"""

from logging import getLogger

from PyQt5.Qt import QLabel, QWidget, Qt, QPushButton, QPixmap, QVBoxLayout, QGridLayout, QTimer

from alignak_app.core.backend.data_manager import data_manager
from alignak_app.core.models.item import get_icon_name
from alignak_app.core.utils.config import get_image, app_css, get_app_config
from alignak_app.core.utils.time import get_time_diff_since_last_timestamp

from alignak_app.pyqt.common.actions import ActionsQWidget

logger = getLogger(__name__)


class ServiceDataQWidget(QWidget):
    """
        Class who create QWidget with service data
    """

    def __init__(self, parent=None):
        super(ServiceDataQWidget, self).__init__(parent)
        self.setStyleSheet(app_css)
        self.setFixedWidth(200)
        # Fields
        self.refresh_timer = QTimer()
        self.service_item = None
        self.host_id = None
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

        update_service = int(get_app_config('Alignak-app', 'update_service')) * 1000
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

        self.labels['ls_output'].setObjectName('output')
        self.labels['ls_output'].setWordWrap(True)
        self.labels['ls_output'].setTextInteractionFlags(Qt.TextSelectableByMouse)
        layout.addWidget(self.labels['ls_output'], 3, 1, 1, 1)

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

    def update_widget(self, service=None, host_id=None):
        """
        Update ServiceDataQWidget

        :param service: Service item with its data
        :type service: alignak_app.core.models.service.Service
        :param host_id: id of attached host
        :type host_id: str
        """

        logger.info('Update Service Qwidget...')

        if service and host_id:
            self.service_item = service
            self.host_id = host_id

        icon_name = get_icon_name(
            'service',
            self.service_item.data['ls_state'],
            self.service_item.data['ls_acknowledged'],
            self.service_item.data['ls_downtimed'],
            self.service_item.data['passive_checks_enabled'] +
            self.service_item.data['active_checks_enabled']
        )
        icon_pixmap = QPixmap(get_image(icon_name))

        self.labels['service_icon'].setPixmap(QPixmap(icon_pixmap))
        self.labels['service_icon'].setToolTip(self.service_item.get_tooltip())
        self.labels['service_name'].setText('%s' % self.service_item.get_display_name())

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

        if self.service_item and self.host_id:
            updated_service = data_manager.get_item('service', '_id', self.service_item.item_id)
            if updated_service:
                self.service_item = updated_service
            self.update_widget()
